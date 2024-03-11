import { ElementType, FunctionComponent, ReactNode, useMemo } from 'react';
import Button, { ButtonProps } from '@mui/material/Button';
import AppIcon from '../AppIcon';
import AppLink from '../AppLink';
import { APP_BUTTON_VARIANT } from '../config';

const MUI_BUTTON_COLORS = ['inherit', 'primary', 'secondary', 'success', 'error', 'info', 'warning'];

const DEFAULT_SX_VALUES = {
  margin: 1, // By default the AppButton has theme.spacing(1) margin on all sides
};

export interface AppButtonProps extends Omit<ButtonProps, 'color' | 'endIcon' | 'startIcon'> {
  color?: string; // Not only 'inherit' | 'primary' | 'secondary' | 'success' | 'error' | 'info' | 'warning',
  endIcon?: string | ReactNode;
  label?: string; // Alternate to .text
  text?: string; // Alternate to .label
  startIcon?: string | ReactNode;
  // Missing props
  component?: ElementType; // Could be RouterLink, AppLink, <a>, etc.
  to?: string; // Link prop
  href?: string; // Link prop
  openInNewTab?: boolean; // Link prop
  underline?: 'none' | 'hover' | 'always'; // Link prop
}

/**
 * Application styled Material UI Button with Box around to specify margins using props
 * @component AppButton
 * @param {string} [color] - when passing MUI value ('primary', 'secondary', and so on), it is color of the button body, otherwise it is color of text and icons
 * @param {string} [children] - content to render, overrides .label and .text props
 * @param {string | ReactNode} [endIcon] - name of AppIcon or ReactNode to show after the button label
 * @param {string} [href] - external link URI
 * @param {string} [label] - text to render, alternate to .text
 * @param {boolean} [openInNewTab] - link will be opened in new tab when true
 * @param {string | ReactNode} [startIcon] - name of AppIcon or ReactNode to show before the button label
 * @param {Array<func| object| bool> | func | object} [sx] - additional CSS styles to apply to the button
 * @param {string} [text] - text to render, alternate to .label
 * @param {string} [to] - internal link URI
 * @param {string} [underline] - controls underline style when button used as link, one of 'none', 'hover', or 'always'
 * @param {string} [variant] - MUI variant of the button, one of 'text', 'outlined', or 'contained'
 */
export const AppButton: FunctionComponent<AppButtonProps> = ({
  children,
  color: propColor = 'inherit',
  component: propComponent,
  endIcon,
  label,
  startIcon,
  sx: propSx = DEFAULT_SX_VALUES,
  text,
  underline = 'none',
  variant = APP_BUTTON_VARIANT,
  ...restOfProps
}: AppButtonProps) => {
  const iconStart: ReactNode = useMemo(
    () => (!startIcon ? undefined : typeof startIcon === 'string' ? <AppIcon icon={String(startIcon)} /> : startIcon),
    [startIcon]
  );

  const iconEnd: ReactNode = useMemo(
    () => (!endIcon ? undefined : typeof endIcon === 'string' ? <AppIcon icon={String(endIcon)} /> : endIcon),
    [endIcon]
  );

  const isMuiColor = useMemo(() => MUI_BUTTON_COLORS.includes(propColor), [propColor]);

  const componentToRender =
    !propComponent && (restOfProps?.href || restOfProps?.to) ? AppLink : propComponent ?? Button;

  const colorToRender = isMuiColor ? (propColor as ButtonProps['color']) : 'inherit';
  const sxToRender = {
    ...propSx,
    ...(isMuiColor ? {} : { color: propColor }),
  };

  return (
    <Button
      component={componentToRender}
      color={colorToRender}
      endIcon={iconEnd}
      startIcon={iconStart}
      sx={sxToRender}
      variant={variant}
      {...{ ...restOfProps, underline }}
    >
      {children || label || text}
    </Button>
  );
};

export default AppButton;
