import { Reducer } from 'react';
import { localStorageSet } from '../utils/localStorage';
import { AppStoreState } from './AppStore';

/**
 * Reducer for global AppStore using "Redux styled" actions
 * @function AppReducer
 * @param {object} state - current/default state
 * @param {string} action.type - unique name of the action
 * @param {string} action.action - alternate to action.type property, unique name of the action
 * @param {*} [action.payload] - optional data object or the function to get data object
 */
const AppReducer: Reducer<AppStoreState, any> = (state, action) => {
  // console.log('AppReducer() - action:', action);
  switch (action.type || action.action) {
    case 'CURRENT_USER':
      return {
        ...state,
        currentUser: action?.currentUser || action?.payload,
      };
    case 'SIGN_UP':
    case 'LOG_IN':
      return {
        ...state,
        isAuthenticated: true,
      };
    case 'LOG_OUT':
      return {
        ...state,
        isAuthenticated: false,
        currentUser: undefined, // Also reset previous user data
      };
    case 'DARK_MODE': {
      const darkMode = action?.darkMode ?? action?.payload;
      localStorageSet('darkMode', darkMode);
      return {
        ...state,
        darkMode,
      };
    }
    default:
      return state;
  }
};

export default AppReducer;
