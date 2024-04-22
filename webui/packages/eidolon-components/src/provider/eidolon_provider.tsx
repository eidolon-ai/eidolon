'use client'

import {createContext, Dispatch, FunctionComponent, PropsWithChildren, Reducer, useContext, useReducer} from "react";

export interface EidolonProviderState {
    usageSeed: number
}

const INITIAL_STATE: EidolonProviderState = {
    usageSeed: 0
}

export type EidolonContextReturningType = [EidolonProviderState, Dispatch<EidolonEvent>];
const EidolonContext = createContext<EidolonContextReturningType>([INITIAL_STATE, () => null]);

export const EidolonProvider: FunctionComponent<PropsWithChildren> = ({ children }) => {
  const initialState: EidolonProviderState = {
    ...INITIAL_STATE
  };
  const value: EidolonContextReturningType = useReducer(EidolonReducer, initialState);

  return <EidolonContext.Provider value={value}>{children}</EidolonContext.Provider>;
}

const EidolonReducer: Reducer<EidolonProviderState, EidolonEvent> = (state, action) => {
  switch (action.event_type) {
    case "CLEAR_USAGE":
      return {
        ...state,
        usageSeed: state.usageSeed + 1,
      };
    default:
      return state;
  }
}

export const useEidolonContext = (): EidolonContextReturningType => useContext(EidolonContext);

export interface EidolonEvent {
  event_type: "CLEAR_USAGE"
}

export const RecordUsage = {
  event_type: "CLEAR_USAGE",
} as EidolonEvent