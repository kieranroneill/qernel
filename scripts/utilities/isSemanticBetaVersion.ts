/**
 * Checks whether a version string represents a beta pre-release.
 *
 * Valid beta versions must start with a semantic version in the form
 * `major.minor.patch` and include the `-beta` suffix immediately after it.
 * Additional characters after `-beta` are allowed by this check.
 *
 * Examples of matching values:
 * - `1.0.0-beta`
 * - `2.3.4-beta1`
 * - `10.12.0-beta.2`
 *
 * Examples of non-matching values:
 * - `1.0.0`
 * - `1.0.0-alpha`
 * - `v1.0.0-beta`
 *
 * @param version - The version string to check.
 * @returns `true` if the version is a beta pre-release; otherwise `false`.
 */
function isSemanticBetaVersion(version: string): boolean {
  return /^[0-9]+\.[0-9]+\.[0-9]+-beta/.test(version);
}

export default isSemanticBetaVersion;
