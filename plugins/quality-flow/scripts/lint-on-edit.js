#!/usr/bin/env node
// Hook PostToolUse: revisa con el linter de su lenguaje el archivo que Claude
// acaba de escribir o editar. Solo usa herramientas que el proyecto o el equipo
// ya tienen (el plugin no incluye linters) y las prueba en orden hasta encontrar una:
//
//   JS/TS/Vue  -> ESLint local del proyecto (node_modules, subiendo desde el archivo)
//   Python     -> ruff (.venv del proyecto o PATH) -> flake8 -> python -m py_compile
//   Go         -> gofmt -e (errores de sintaxis)
//   PHP        -> php -l
//   Ruby       -> ruby -wc
//   Shell      -> shellcheck -> bash -n
//   JSON       -> parseo interno
//
// El código de salida 2 le devuelve los problemas a Claude. Cualquier otro caso
// (lenguaje desconocido, herramienta no instalada o que falla, entrada inválida)
// termina con 0 en silencio, para que el hook nunca estorbe.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const IS_WIN = process.platform === 'win32';
const TIMEOUT_MS = 25000;

function readStdin() {
  try {
    return JSON.parse(fs.readFileSync(0, 'utf8'));
  } catch {
    return null;
  }
}

// Sube desde `startDir` y devuelve la primera ruta de `relPaths` que exista.
function findUp(startDir, relPaths) {
  let dir = startDir;
  for (;;) {
    for (const rel of relPaths) {
      const candidate = path.join(dir, rel);
      if (fs.existsSync(candidate)) return { file: candidate, root: dir };
    }
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

// Se ejecuta sin shell para que las rutas con espacios o "&" funcionen en cualquier SO.
// Devuelve null si la herramienta no está instalada, falló o superó el tiempo límite.
function run(cmd, args, cwd) {
  const res = spawnSync(cmd, args, { cwd, encoding: 'utf8', timeout: TIMEOUT_MS, windowsHide: true });
  if (res.error) return null;
  return { status: res.status, output: `${res.stdout || ''}${res.stderr || ''}`.trim() };
}

// Cada comprobador devuelve { tool, output } si encontró problemas, false si el
// archivo está limpio, o null si no pudo ejecutarse (y entonces se prueba el siguiente).
const checkers = {
  eslint(file, dir) {
    const found = findUp(dir, [path.join('node_modules', 'eslint', 'bin', 'eslint.js')]);
    if (!found) return null;
    const res = run(process.execPath, [found.file, '--no-warn-ignored', file], found.root);
    if (!res || res.status === 2) return null; // 2 = error de config/fallo de ESLint, no del archivo
    return res.status === 1 ? { tool: 'ESLint', output: res.output } : false;
  },
  ruff(file, dir) {
    const venv = findUp(dir, IS_WIN
      ? [path.join('.venv', 'Scripts', 'ruff.exe'), path.join('venv', 'Scripts', 'ruff.exe')]
      : [path.join('.venv', 'bin', 'ruff'), path.join('venv', 'bin', 'ruff')]);
    const res = run(venv ? venv.file : 'ruff', ['check', '--quiet', file], venv ? venv.root : dir);
    if (!res || res.status > 1) return null;
    return res.status === 1 ? { tool: 'ruff', output: res.output } : false;
  },
  flake8(file, dir) {
    const res = run('flake8', [file], dir);
    if (!res || res.status > 1) return null;
    return res.status === 1 ? { tool: 'flake8', output: res.output } : false;
  },
  pyCompile(file, dir) {
    for (const py of IS_WIN ? ['python', 'py'] : ['python3', 'python']) {
      const res = run(py, ['-m', 'py_compile', file], dir);
      if (res) return res.status === 0 ? false : { tool: 'python -m py_compile', output: res.output };
    }
    return null;
  },
  gofmt(file, dir) {
    const res = run('gofmt', ['-e', '-l', file], dir);
    if (!res) return null;
    return res.status === 0 ? false : { tool: 'gofmt', output: res.output };
  },
  php(file, dir) {
    const res = run('php', ['-l', file], dir);
    if (!res) return null;
    return res.status === 0 ? false : { tool: 'php -l', output: res.output };
  },
  ruby(file, dir) {
    const res = run('ruby', ['-wc', file], dir);
    if (!res) return null;
    return res.status === 0 ? false : { tool: 'ruby -wc', output: res.output };
  },
  shellcheck(file, dir) {
    const res = run('shellcheck', [file], dir);
    if (!res || res.status > 1) return null;
    return res.status === 1 ? { tool: 'shellcheck', output: res.output } : false;
  },
  bashN(file, dir) {
    const res = run('bash', ['-n', file], dir);
    if (!res) return null;
    return res.status === 0 ? false : { tool: 'bash -n', output: res.output };
  },
  json(file) {
    try {
      JSON.parse(fs.readFileSync(file, 'utf8').replace(/^﻿/, ''));
      return false;
    } catch (e) {
      return { tool: 'JSON parse', output: e.message };
    }
  },
};

const BY_EXTENSION = {
  '.js': ['eslint'], '.jsx': ['eslint'], '.mjs': ['eslint'], '.cjs': ['eslint'],
  '.ts': ['eslint'], '.tsx': ['eslint'], '.mts': ['eslint'], '.cts': ['eslint'], '.vue': ['eslint'],
  '.py': ['ruff', 'flake8', 'pyCompile'],
  '.go': ['gofmt'],
  '.php': ['php'],
  '.rb': ['ruby'],
  '.sh': ['shellcheck', 'bashN'], '.bash': ['shellcheck', 'bashN'],
  '.json': ['json'],
};

const input = readStdin();
const rawPath = input && input.tool_input && input.tool_input.file_path;
if (!rawPath) process.exit(0);

const file = path.resolve(rawPath);
const chain = BY_EXTENSION[path.extname(file).toLowerCase()];
if (!chain || !fs.existsSync(file)) process.exit(0);
// Omitir los JSON que admiten comentarios o comas finales.
if (/(^|[\\/])(tsconfig[^\\/]*|jsconfig|\.eslintrc|devcontainer)\.json$/i.test(file) || file.includes(`${path.sep}.vscode${path.sep}`)) {
  process.exit(0);
}

for (const name of chain) {
  const result = checkers[name](file, path.dirname(file));
  if (result === null) continue; // herramienta no disponible, probar la siguiente
  if (result) {
    process.stderr.write(`${result.tool} encontró problemas en ${rawPath}:\n${result.output}\n`);
    process.exit(2);
  }
  break; // limpio
}
process.exit(0);
