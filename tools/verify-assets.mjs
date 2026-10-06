import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const projects = (await fs.readdir(root, { withFileTypes: true }))
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .filter((name) => existsSync(path.join(root, name, 'video', 'assets.json')))
  .sort();
const cwdProject = path.relative(root, process.cwd()).split(path.sep)[0];
const project = process.argv[2] || cwdProject;

if (!projects.includes(project)) {
  process.stderr.write('Indica el proyecto desde su carpeta video o como argumento.\n');
  process.exit(2);
}

const videoRoot = path.join(root, project, 'video');
const manifestPath = path.join(videoRoot, 'assets.json');
const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
if (!Array.isArray(manifest.assets)) {
  throw new Error(manifestPath + ': "assets" debe ser una lista.');
}

const manifestPaths = new Set();
const missing = new Set();
for (const asset of manifest.assets) {
  const target = path.resolve(videoRoot, asset.path);
  if (!target.startsWith(videoRoot + path.sep)) {
    throw new Error(manifestPath + ': ruta fuera del proyecto: ' + asset.path);
  }
  manifestPaths.add(asset.path);
  try {
    const stat = await fs.stat(target);
    if (!stat.isFile() || stat.size === 0) missing.add(asset.path);
  } catch {
    missing.add(asset.path);
  }
}

const compositionDir = path.join(videoRoot, 'compositions');
const imageRefs = new Set();
for (const filename of await fs.readdir(compositionDir)) {
  if (!filename.endsWith('.html')) continue;
  const content = await fs.readFile(path.join(compositionDir, filename), 'utf8');
  for (const match of content.matchAll(/(?:src|href)=["'](assets\/img\/[^"']+)["']/g)) {
    imageRefs.add(match[1]);
  }
}

const unregistered = [...imageRefs].filter((imagePath) => !manifestPaths.has(imagePath));
if (unregistered.length > 0) {
  process.stderr.write('Hay imágenes de composición sin entrada en ' + project + '/video/assets.json:\n');
  for (const imagePath of unregistered) process.stderr.write('  - ' + imagePath + '\n');
  process.exit(1);
}

for (const imagePath of imageRefs) {
  const target = path.resolve(videoRoot, imagePath);
  try {
    const stat = await fs.stat(target);
    if (!stat.isFile() || stat.size === 0) missing.add(imagePath);
  } catch {
    missing.add(imagePath);
  }
}

if (missing.size > 0) {
  process.stderr.write(
    'No se puede renderizar ' + project + ': faltan ' + missing.size +
    ' imágenes o tienen tamaño cero:\n',
  );
  for (const imagePath of [...missing].sort()) process.stderr.write('  - ' + imagePath + '\n');
  process.stderr.write(
    'Descarga las URL directas con «node tools/fetch-assets» y consigue manualmente las demás ' +
    'según la fuente indicada en ' + project + '/video/assets.json.\n',
  );
  process.exit(1);
}

process.stdout.write('Imágenes presentes: ' + project + ' (' + imageRefs.size + ' referencias).\n');
