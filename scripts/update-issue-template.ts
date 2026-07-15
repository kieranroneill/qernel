import chalk from 'chalk';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import * as process from 'node:process';
import { type Document, isMap, isSeq, parseDocument, type Scalar, type YAMLMap, type YAMLSeq } from 'yaml';

// utilities
import { isSemanticBetaVersion, isSemanticVersionValid } from './utilities';

/**
 * Adds a release version to the bug report issue template if it is not already
 * present in the version dropdown options.
 *
 * The function validates the provided version string, skips beta pre-releases,
 * parses the YAML issue template document, locates the `body` item with the
 * `version` id, and prepends the version to `attributes.options` when missing.
 *
 * The process exits immediately with a non-zero status when validation fails,
 * the YAML document contains parse errors, or the expected YAML structure
 * cannot be found.
 *
 * @param version - The semantic version to add to the issue template.
 *
 * @example
 * main('1.2.3');
 */
function main(version: string): void {
  let bodySequence: YAMLSeq | unknown;
  let document: Document.Parsed;
  let filePath: string;
  let source: string;
  let versionItem: YAMLMap | undefined;
  let versionOptionsSequence: YAMLSeq | unknown;

  if (!version) {
    console.error(
      `${chalk.red('[ERROR]')}: no version specified, use: "tsx scripts/update-issue-templates.js [version]"`
    );
    process.exit(1);
  }

  if (!isSemanticVersionValid(version)) {
    console.error(
      `${chalk.red('[ERROR]')}: invalid semantic version, got '${version}', but should be in the format '1.0.0'`
    );
    process.exit(1);
  }

  if (isSemanticBetaVersion(version)) {
    console.info(`${chalk.yellow('[INFO]')}: pre-release versions should not be added, skipping`);
    process.exit(0);
  }

  filePath = resolve(process.cwd(), '.github/ISSUE_TEMPLATE/bug_report_template.yml');
  source = readFileSync(filePath, 'utf8');
  document = parseDocument(source);

  if (document.errors.length > 0) {
    for (const error of document.errors) {
      console.error(`${chalk.red('[ERROR]')}: ${error.message}`);
    }

    process.exit(1);
  }

  bodySequence = document.get('body', true);

  if (!isSeq(bodySequence)) {
    console.error(`${chalk.red('[ERROR]')}: could not find "body" sequence in "${filePath}"`);
    process.exit(1);
  }

  versionItem = (bodySequence as YAMLSeq).items.find(
    (item) => isMap(item) && item.get('id', true)?.value === 'version'
  ) as YAMLMap | undefined;

  if (!versionItem) {
    console.error(`${chalk.red('[ERROR]')}: could not find "version" item in the "body" sequence in the "${filePath}"`);
    process.exit(1);
  }

  versionOptionsSequence = (versionItem as YAMLMap).getIn(['attributes', 'options'], true);

  if (!isSeq(versionOptionsSequence)) {
    console.error(`${chalk.red('[ERROR]')}: could not find "version" options array in the "${filePath}"`);
    process.exit(1);
  }

  // if the version is already included
  if ((versionOptionsSequence as YAMLSeq).items.some((node: Scalar) => node.value === version)) {
    console.info(`${chalk.yellow('[INFO]')}: version "${version}" already added to "${filePath}"`);
    process.exit(0);
  }

  (versionOptionsSequence as YAMLSeq).items.unshift(document.createNode(version));

  writeFileSync(filePath, String(document), 'utf8');

  console.info(`${chalk.yellow('[INFO]')}: added version "${version}" to "${filePath}"`);

  process.exit(0);
}

main(process.argv[2]);
