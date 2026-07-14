import chalk from 'chalk';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import * as process from 'node:process';
import { parse, stringify, TomlTable } from 'smol-toml';

// utilities
import { isSemanticVersionValid } from './utilities';

/**
 * Updates the version in `pyproject.toml` if a supported static version field
 * is present and the requested version differs from the current value.
 *
 * The function validates the supplied semantic version, reads `pyproject.toml`,
 * and updates one of the `project.version` field.
 *
 * If `project.dynamic` includes `"version"`, the file is treated as using
 * dynamic version metadata and is not modified directly.
 *
 * @param version - The semantic version to write to `pyproject.toml`.
 *
 * @example
 * main('1.2.3');
 */
function main(version: string): void {
  let filePath: string;
  let pyproject: TomlTable;
  let source: string;

  if (!version) {
    console.error(
      `${chalk.red('[ERROR]')}: no version specified, use: "tsx scripts/update-pyproject-version.ts [version]"`
    );
    process.exit(1);
  }

  if (!isSemanticVersionValid(version)) {
    console.error(
      `${chalk.red('[ERROR]')}: invalid semantic version, got '${version}', but should be in the format '1.0.0'`
    );
    process.exit(1);
  }

  filePath = resolve(process.cwd(), 'pyproject.toml');
  source = readFileSync(filePath, 'utf8');

  try {
    pyproject = parse(source);
  } catch (error) {
    console.error(`${chalk.red('[ERROR]')}: failed to parse "${filePath}"`, error);
    process.exit(1);
  }

  if (pyproject.project.version === version) {
    console.info(`${chalk.yellow('[INFO]')}: version "${version}" already set in "${filePath}"`);
    process.exit(0);
  }

  pyproject.project.version = version;

  try {
    writeFileSync(filePath, stringify(pyproject), 'utf8');
  } catch (error) {
    console.error(`${chalk.red('[ERROR]')}: failed to write "${filePath}"`, error);
    process.exit(1);
  }

  console.info(`${chalk.yellow('[INFO]')}: updated version to "${version}" in "${filePath}"`);

  process.exit(0);
}

main(process.argv[2]);
