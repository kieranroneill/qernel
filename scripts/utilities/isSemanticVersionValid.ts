/**
 * Checks whether a version string matches a basic semantic version format.
 *
 * Valid versions must be in the form `major.minor.patch`, with or without pre-release, where each segment
 * contains one or more digits and no build metadata is allowed.
 *
 * Examples of valid values:
 * - `1.0.0`
 * - `12.4.7`
 * - `1.0.0-beta`
 *
 * Examples of invalid values:
 * - `1.0`
 * - `v1.0.0`
 *
 * @param version - The version string to validate.
 * @returns `true` if the version matches `major.minor.patch`; otherwise `false`.
 */
function isSemanticVersionValid(version: string): boolean {
  return /^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$/.test(
    version
  );
}

export default isSemanticVersionValid;
