/**
 * Components configuration
 */

/**
 * AppAlert and AppSnackBarAlert components
 */
export const APP_ALERT_SEVERITY = 'error'; // 'error' | 'info'| 'success' | 'warning'
export const APP_ALERT_VARIANT = 'filled'; // 'filled' | 'outlined' | 'standard'

/**
 * AppButton component
 */
export const APP_BUTTON_VARIANT = 'contained'; // | 'text' | 'outlined'
export const APP_BUTTON_MARGIN = 1;

/**
 * AppIcon component
 */
export const APP_ICON_SIZE = 24;

/**
 * AppLink component
 */
export const APP_LINK_COLOR = 'textSecondary'; // 'primary' // 'secondary'
export const APP_LINK_UNDERLINE = 'hover'; // 'always

/**
 * AppSection component
 */
export const APP_SECTION_VARIANT = 'subtitle2'; // 'subtitle1' | 'body1' | 'h6'

/**
 * AppSnackBar and AppSnackBarProvider components
 */
export const APP_SNACKBAR_MAX_COUNT = 5; // Used in AppSnackBarProvider from notistack npm
export const APP_SNACKBAR_AUTO_HIDE_DURATION = 3000; // Set to null if want to disable AutoHide feature
export const APP_SNACKBAR_ANCHOR_ORIGIN_VERTICAL = 'bottom'; // 'bottom | 'top'
export const APP_SNACKBAR_ANCHOR_ORIGIN_HORIZONTAL = 'center'; // 'center' | 'left' | 'right'
