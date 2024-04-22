'use client';
import {ComponentType, createContext, Dispatch, FunctionComponent, PropsWithChildren, useContext, useReducer,} from 'react';
// import useMediaQuery from '@mui/material/useMediaQuery';
import AppReducer from './AppReducer';
import {IS_SERVER, localStorageGet} from '../utils';

/**
 * AppState data structure and initial values
 */
export interface AppStoreState {
  darkMode: boolean;
  themeMode: string
  isAuthenticated: boolean;
  currentUser?: object | undefined;
  userUsageSeed: number
}
const INITIAL_APP_STATE: AppStoreState = {
  darkMode: false, // Overridden by useMediaQuery('(prefers-color-scheme: dark)') in AppStore
  themeMode: "system",
  isAuthenticated: false, // Overridden in AppStore by checking auth token
  userUsageSeed: 0
};

/**
 * Instance of React Context for global AppStore
 */
export type AppContextReturningType = [AppStoreState, Dispatch<any>];
const AppContext = createContext<AppContextReturningType>([INITIAL_APP_STATE, () => null]);

/**
 * Main global Store as HOC with React Context API
 * @component AppStoreProvider
 * import {AppStoreProvider} from './store'
 * ...
 * <AppStoreProvider>
 *  <App/>
 * </AppStoreProvider>
 */
const AppStoreProvider: FunctionComponent<PropsWithChildren> = ({ children }) => {
  // const prefersDarkMode = IS_SERVER ? false : useMediaQuery('(prefers-color-scheme: dark)'); // Note: Conditional hook is bad idea :(
  const prefersDarkMode = IS_SERVER ? false : window.matchMedia('(prefers-color-scheme: dark)').matches;
  const previousDarkMode = IS_SERVER ? "system" : localStorageGet('darkMode', "light");
  // const tokenExists = Boolean(loadToken());

  const initialState: AppStoreState = {
    ...INITIAL_APP_STATE,
    darkMode: previousDarkMode === "system" ? prefersDarkMode : previousDarkMode === "dark",
    themeMode: previousDarkMode,
    userUsageSeed: 0
    // isAuthenticated: tokenExists,
  };
  const value: AppContextReturningType = useReducer(AppReducer, initialState);

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

/**
 * Hook to use the AppStore in functional components
 * @hook useAppStore
 * import {useAppStore} from './store'
 * ...
 * const [state, dispatch] = useAppStore();
 *   OR
 * const [state] = useAppStore();
 */
const useAppStore = (): AppContextReturningType => useContext(AppContext);

/**
 * HOC to inject the AppStore to class component, also works for functional components
 * @hok withAppStore
 * import {withAppStore} from './store'
 * ...
 * class MyComponent
 *
 * render () {
 *   const [state, dispatch] = this.props.appStore;
 *   ...
 * }
 * ...
 * export default withAppStore(MyComponent)
 */
interface WithAppStoreProps {
  appStore: AppContextReturningType;
}
const withAppStore = (Component: ComponentType<WithAppStoreProps>): FunctionComponent =>
  function ComponentWithAppStore(props) {
    return <Component {...props} appStore={useAppStore()} />;
  };

export { AppStoreProvider, useAppStore, withAppStore };
