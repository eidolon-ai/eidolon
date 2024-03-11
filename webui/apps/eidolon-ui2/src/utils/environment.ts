export const IS_SERVER = typeof window === 'undefined';
export const IS_BROWSER = typeof window !== 'undefined' && typeof window?.document !== 'undefined';
/* eslint-disable no-restricted-globals */
export const IS_WEBWORKER =
  typeof self === 'object' && self.constructor && self.constructor.name === 'DedicatedWorkerGlobalScope';
/* eslint-enable no-restricted-globals */

export function getCurrentVersion(): string {
  return process.env?.npm_package_version ?? process.env.REACT_APP_VERSION ?? 'unknown';
}

export function getCurrentEnvironment(): string {
  return process.env?.NODE_ENV ?? 'development';
}
