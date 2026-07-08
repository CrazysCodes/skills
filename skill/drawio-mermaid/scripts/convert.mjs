#!/usr/bin/env node
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const scriptDir = path.dirname(scriptPath);

const candidates = [
  process.env.DRAWIO_MERMAID_CLI,
  path.resolve(scriptDir, '..', '..', '..', 'src', 'cli.mjs'),
  path.resolve(scriptDir, '..', '..', '..', '..', 'drawio-mermaid', 'src', 'cli.mjs'),
  path.resolve(process.cwd(), 'src', 'cli.mjs'),
].filter(Boolean);

const cliPath = candidates.find((candidate) => fs.existsSync(candidate));
if (!cliPath) {
  console.error('未找到 drawio-mermaid CLI。请在项目根目录运行，或设置 DRAWIO_MERMAID_CLI=/path/to/src/cli.mjs');
  process.exit(1);
}

// wrapper 可能被复制到 skill 仓库，也可能在项目内；以 CLI 所在目录作为工作目录更稳。
const projectRoot = path.resolve(path.dirname(cliPath), '..');
const result = spawnSync(process.execPath, [cliPath, ...process.argv.slice(2)], {
  cwd: projectRoot,
  stdio: 'inherit',
});

process.exit(result.status ?? 1);
