import { ComponentType, FunctionComponent, SVGAttributes } from 'react';
import { APP_ICON_SIZE } from '../config';
// SVG assets
import LogoIcon from './icons/LogoIcon';
// MUI Icons
import DefaultIcon from '@mui/icons-material/MoreHoriz';
import SettingsIcon from '@mui/icons-material/Settings';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import DayNightIcon from '@mui/icons-material/Brightness4';
import NightIcon from '@mui/icons-material/Brightness3';
import DayIcon from '@mui/icons-material/Brightness5';
import SearchIcon from '@mui/icons-material/Search';
import InfoIcon from '@mui/icons-material/Info';
import HomeIcon from '@mui/icons-material/Home';
import AccountCircle from '@mui/icons-material/AccountCircle';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import PersonIcon from '@mui/icons-material/Person';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import NotificationsIcon from '@mui/icons-material/NotificationsOutlined';

/**
 * How to use:
 * 1. Import all required MUI or other SVG icons into this file.
 * 2. Add icons with "unique lowercase names" into ICONS object.
 * 3. Use icons everywhere in the App by their names in <AppIcon icon="xxx" /> component
 * Important: properties of ICONS object MUST be lowercase!
 * Note: You can use camelCase or UPPERCASE in the <AppIcon icon="someIconByName" /> component
 */
export const ICONS: Record<string, ComponentType> = {
  default: DefaultIcon,
  logo: LogoIcon,
  close: CloseIcon,
  menu: MenuIcon,
  settings: SettingsIcon,
  visibilityon: VisibilityIcon,
  visibilityoff: VisibilityOffIcon,
  daynight: DayNightIcon,
  night: NightIcon,
  day: DayIcon,
  search: SearchIcon,
  info: InfoIcon,
  home: HomeIcon,
  account: AccountCircle,
  signup: PersonAddIcon,
  login: PersonIcon,
  logout: ExitToAppIcon,
  notifications: NotificationsIcon,
};

export interface AppIconProps extends SVGAttributes<SVGElement> {
  color?: string;
  icon?: string;
  size?: string | number;
  title?: string;
}

/**
 * Renders SVG icon by given Icon name
 * @component AppIcon
 * @param {string} [color] - color of the icon as a CSS color value
 * @param {string} [icon] - name of the Icon to render
 * @param {string} [title] - title/hint to show when the cursor hovers the icon
 * @param {string | number} [size] - size of the icon, default is ICON_SIZE
 */
const AppIcon: FunctionComponent<AppIconProps> = ({
  color,
  icon = 'default',
  size = APP_ICON_SIZE,
  style,
  ...restOfProps
}) => {
  const iconName = (icon || 'default').trim().toLowerCase();

  let ComponentToRender = ICONS[iconName];
  if (!ComponentToRender) {
    console.warn(`AppIcon: icon "${iconName}" is not found!`);
    ComponentToRender = DefaultIcon;
  }

  const propsToRender = {
    height: size,
    color,
    fill: color && 'currentColor',
    size,
    style: { ...style, color },
    width: size,
    ...restOfProps,
  };

  return <ComponentToRender data-icon={iconName} {...propsToRender} />;
};

export default AppIcon;
