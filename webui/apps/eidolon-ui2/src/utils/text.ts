export const CHARS_NUMERIC = '0123456789';
export const CHARS_ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz';
export const CHARS_ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
export const CHARS_ALPHA_NUMERIC = CHARS_NUMERIC + CHARS_ALPHA_LOWER + CHARS_ALPHA_UPPER;

/**
 * Generate a random string of a given length using a given set of characters
 * @param {number} length - the length of the string to generate
 * @param {string} [allowedChars] - the set of characters to use in the string, defaults to all alphanumeric characters in upper and lower case + numbers
 * @returns {string} - the generated string
 */
export function randomText(length: number, allowedChars = CHARS_ALPHA_NUMERIC) {
  let result = '';
  const charLength = allowedChars.length;
  let counter = 0;
  while (counter < length) {
    result += allowedChars.charAt(Math.floor(Math.random() * charLength));
    counter += 1;
  }
  return result;
}
/**
 * Compare two strings including null and undefined values
 * @param {string} a - the first string to compare
 * @param {string} b - the second string to compare
 * @returns {boolean} - true if the strings are the same or both null or undefined, false otherwise
 */
export function compareTexts(a: string | null | undefined, b: string | null | undefined) {
  if (a === undefined || a === null || a === '') {
    return b === undefined || b === null || b === '';
  }
  return a === b;
}

/**
 * Capitalize the first letter of a string
 * @param {string} s - the string to capitalize
 * @returns {string} - the capitalized string
 */
export const capitalize = (s: string): string => s.charAt(0).toUpperCase() + s.substring(1);

/**
 * Generate a random color as #RRGGBB value
 * @returns {string} - the generated color
 */
export function randomColor() {
  const color = Math.floor(Math.random() * 16777215).toString(16);
  return '#' + color;
}
