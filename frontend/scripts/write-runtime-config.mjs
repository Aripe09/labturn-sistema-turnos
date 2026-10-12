import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const apiUrl = (process.env.LABTURN_API_URL || '').replace(/\/+$/, '');
const target = join(process.cwd(), 'src', 'assets', 'runtime-config.js');

mkdirSync(dirname(target), { recursive: true });
writeFileSync(
  target,
  `window.__LABTURN_CONFIG__ = {\n  apiUrl: ${JSON.stringify(apiUrl)}\n};\n`,
  'utf8'
);
