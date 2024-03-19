/**
 * Delays code executions for specific amount of time. Must be called with await!
 * @param {number} interval - number of milliseconds to wait for
 */
export async function sleep(interval = 1000) {
  return new Promise((resolve) => setTimeout(resolve, interval));
}

export default sleep;
