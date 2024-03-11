/**
 * Disables "Back" button for current page
 * Usage: Call function in useEffect(  ,[]) or directly
 */
export function disableBackNavigation() {
  window.history.pushState(null, '', window.location.href);
  window.onpopstate = function () {
    window.history.go(1);
  };
}

/**
 * Navigates to the specified URL with options
 */
export function navigateTo(url: string, replaceInsteadOfPush = false, optionalTitle = '') {
  if (replaceInsteadOfPush) {
    window.history.replaceState(null, optionalTitle, url);
  } else {
    window.history.pushState(null, optionalTitle, url);
  }
}
