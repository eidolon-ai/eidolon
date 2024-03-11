'use client';
import { FunctionComponent, useCallback, MouseEvent } from 'react';
import { Stack, Divider, Drawer, DrawerProps, FormControlLabel, Switch, Tooltip } from '@mui/material';
import { AppIconButton } from '../../components';
import { useAppStore } from '../../store/AppStore';
import { LinkToPage } from '../../utils/type';
import { useEventLogout, useEventSwitchDarkMode, useOnMobile } from '../../hooks';
import SideBarNavList from './SideBarNavList';
import { SIDEBAR_WIDTH, TOP_BAR_DESKTOP_HEIGHT } from '../config';

interface Props extends Pick<DrawerProps, 'anchor' | 'className' | 'open' | 'variant' | 'onClose'> {
  items: Array<LinkToPage>;
}

/**
 * Renders SideBar with Menu and User details
 * Actually for Authenticated users only, rendered in "Private Layout"
 * @component SideBar
 * @param {string} anchor - 'left' or 'right'
 * @param {boolean} open - the Drawer is visible when true
 * @param {string} variant - variant of the Drawer, one of 'permanent', 'persistent', 'temporary'
 * @param {function} onClose - called when the Drawer is closing
 */
const SideBar: FunctionComponent<Props> = ({ anchor, open, variant, items, onClose, ...restOfProps }) => {
  const [state] = useAppStore();
  const onMobile = useOnMobile();

  const onSwitchDarkMode = useEventSwitchDarkMode();
  const onLogout = useEventLogout();

  const handleAfterLinkClick = useCallback(
    (event: MouseEvent) => {
      if (variant === 'temporary' && typeof onClose === 'function') {
        onClose(event, 'backdropClick');
      }
    },
    [variant, onClose]
  );

  return (
    <Drawer
      anchor={anchor}
      open={open}
      variant={variant}
      PaperProps={{
        sx: {
          width: SIDEBAR_WIDTH,
          marginTop: onMobile ? 0 : variant === 'temporary' ? 0 : TOP_BAR_DESKTOP_HEIGHT,
          height: onMobile ? '100%' : variant === 'temporary' ? '100%' : `calc(100% - ${TOP_BAR_DESKTOP_HEIGHT})`,
        },
      }}
      onClose={onClose}
    >
      <Stack
        sx={{
          height: '100%',
          padding: 2,
        }}
        {...restOfProps}
        onClick={handleAfterLinkClick}
      >
        <SideBarNavList items={items} showIcons />

        <Divider />

        <Stack
          sx={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-evenly',
            alignItems: 'center',
            marginTop: 2,
          }}
        >
          <Tooltip title={state.darkMode ? 'Switch to Light mode' : 'Switch to Dark mode'}>
            <FormControlLabel
              label={!state.darkMode ? 'Light mode' : 'Dark mode'}
              control={<Switch checked={state.darkMode} onChange={onSwitchDarkMode} />}
            />
          </Tooltip>

          {state.isAuthenticated && <AppIconButton icon="logout" title="Logout Current User" onClick={onLogout} />}
        </Stack>
      </Stack>
    </Drawer>
  );
};

export default SideBar;
