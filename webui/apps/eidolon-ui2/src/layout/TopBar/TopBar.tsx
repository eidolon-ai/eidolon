import {AppBar, Toolbar} from '@mui/material';
import * as React from 'react';
import {FunctionComponent} from 'react';
import {HEADER_BG_COLOR_DARK, HEADER_BG_COLOR_LIGHT, TOP_BAR_DESKTOP_HEIGHT, TOP_BAR_MOBILE_HEIGHT} from "../config";
import {useOnMobile} from "../../hooks/index";
import {useAppStore} from "../../store/index";

interface Props {
  endNode?: JSX.Element;
  startNode?: JSX.Element;
  title?: string;
  goToApp: (app: string) => void
}

/**
 * Renders TopBar composition
 * @component TopBar
 */
const TopBar: FunctionComponent<Props> = ({goToApp, endNode, startNode, title = '', ...restOfProps}) => {
  const onMobile = useOnMobile();
  const [state, dispatch] = useAppStore();
  // const {data: session} = useServerSession()

  return (
    <AppBar
      component="div"
      sx={
        {
          zIndex: (theme) => theme.zIndex.drawer + 1 ,
          justifyContent: 'center',
          height: onMobile ? TOP_BAR_MOBILE_HEIGHT : TOP_BAR_DESKTOP_HEIGHT,
          bgcolor: state.darkMode ? HEADER_BG_COLOR_DARK : HEADER_BG_COLOR_LIGHT,
          // boxShadow: 'none', // Uncomment to hide shadow
        }
      }
      {...restOfProps}
    >
      <Toolbar variant={"dense"} disableGutters sx={{
        paddingX: 1,
        justifyContent: 'space-between',
        alignItems: 'center',
        height: "77px"
      }}
      >
        {startNode}
        {endNode}
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
