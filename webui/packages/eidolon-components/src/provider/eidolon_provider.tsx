'use client'

import {
  createContext,
  useContext,
  useReducer
} from "react";

type Reducer<S, A> = (prevState: S, action: A) => S;

type PropsWithChildren<P = unknown> = P & { children?: ReactNode | undefined };

interface DO_NOT_USE_OR_YOU_WILL_BE_FIRED_EXPERIMENTAL_REACT_NODES {}

interface ReactPortal extends ReactElement {
  children: ReactNode;
}

interface ErrorInfo {
  /**
   * Captures which component contained the exception, and its ancestors.
   */
  componentStack?: string | null;
  digest?: string | null;
}

interface DeprecatedLifecycle<P, S> {
  /**
   * Called immediately before mounting occurs, and before {@link Component.render}.
   * Avoid introducing any side-effects or subscriptions in this method.
   *
   * Note: the presence of {@link NewLifecycle.getSnapshotBeforeUpdate getSnapshotBeforeUpdate}
   * or {@link StaticLifecycle.getDerivedStateFromProps getDerivedStateFromProps} prevents
   * this from being invoked.
   *
   * @deprecated 16.3, use {@link ComponentLifecycle.componentDidMount componentDidMount} or the constructor instead; will stop working in React 17
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#initializing-state}
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#gradual-migration-path}
   */
  componentWillMount?(): void;
  /**
   * Called immediately before mounting occurs, and before {@link Component.render}.
   * Avoid introducing any side-effects or subscriptions in this method.
   *
   * This method will not stop working in React 17.
   *
   * Note: the presence of {@link NewLifecycle.getSnapshotBeforeUpdate getSnapshotBeforeUpdate}
   * or {@link StaticLifecycle.getDerivedStateFromProps getDerivedStateFromProps} prevents
   * this from being invoked.
   *
   * @deprecated 16.3, use {@link ComponentLifecycle.componentDidMount componentDidMount} or the constructor instead
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#initializing-state}
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#gradual-migration-path}
   */
  UNSAFE_componentWillMount?(): void;
  /**
   * Called when the component may be receiving new props.
   * React may call this even if props have not changed, so be sure to compare new and existing
   * props if you only want to handle changes.
   *
   * Calling {@link Component.setState} generally does not trigger this method.
   *
   * Note: the presence of {@link NewLifecycle.getSnapshotBeforeUpdate getSnapshotBeforeUpdate}
   * or {@link StaticLifecycle.getDerivedStateFromProps getDerivedStateFromProps} prevents
   * this from being invoked.
   *
   * @deprecated 16.3, use static {@link StaticLifecycle.getDerivedStateFromProps getDerivedStateFromProps} instead; will stop working in React 17
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#updating-state-based-on-props}
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#gradual-migration-path}
   */
  componentWillReceiveProps?(nextProps: Readonly<P>, nextContext: any): void;
  /**
   * Called when the component may be receiving new props.
   * React may call this even if props have not changed, so be sure to compare new and existing
   * props if you only want to handle changes.
   *
   * Calling {@link Component.setState} generally does not trigger this method.
   *
   * This method will not stop working in React 17.
   *
   * Note: the presence of {@link NewLifecycle.getSnapshotBeforeUpdate getSnapshotBeforeUpdate}
   * or {@link StaticLifecycle.getDerivedStateFromProps getDerivedStateFromProps} prevents
   * this from being invoked.
   *
   * @deprecated 16.3, use static {@link StaticLifecycle.getDerivedStateFromProps getDerivedStateFromProps} instead
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#updating-state-based-on-props}
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#gradual-migration-path}
   */
  UNSAFE_componentWillReceiveProps?(nextProps: Readonly<P>, nextContext: any): void;
  /**
   * Called immediately before rendering when new props or state is received. Not called for the initial render.
   *
   * Note: You cannot call {@link Component.setState} here.
   *
   * Note: the presence of {@link NewLifecycle.getSnapshotBeforeUpdate getSnapshotBeforeUpdate}
   * or {@link StaticLifecycle.getDerivedStateFromProps getDerivedStateFromProps} prevents
   * this from being invoked.
   *
   * @deprecated 16.3, use getSnapshotBeforeUpdate instead; will stop working in React 17
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#reading-dom-properties-before-an-update}
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#gradual-migration-path}
   */
  componentWillUpdate?(nextProps: Readonly<P>, nextState: Readonly<S>, nextContext: any): void;
  /**
   * Called immediately before rendering when new props or state is received. Not called for the initial render.
   *
   * Note: You cannot call {@link Component.setState} here.
   *
   * This method will not stop working in React 17.
   *
   * Note: the presence of {@link NewLifecycle.getSnapshotBeforeUpdate getSnapshotBeforeUpdate}
   * or {@link StaticLifecycle.getDerivedStateFromProps getDerivedStateFromProps} prevents
   * this from being invoked.
   *
   * @deprecated 16.3, use getSnapshotBeforeUpdate instead
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#reading-dom-properties-before-an-update}
   * @see {@link https://legacy.reactjs.org/blog/2018/03/27/update-on-async-rendering.html#gradual-migration-path}
   */
  UNSAFE_componentWillUpdate?(nextProps: Readonly<P>, nextState: Readonly<S>, nextContext: any): void;
}

interface NewLifecycle<P, S, SS> {
  /**
   * Runs before React applies the result of {@link Component.render render} to the document, and
   * returns an object to be given to {@link componentDidUpdate}. Useful for saving
   * things such as scroll position before {@link Component.render render} causes changes to it.
   *
   * Note: the presence of this method prevents any of the deprecated
   * lifecycle events from running.
   */
  getSnapshotBeforeUpdate?(prevProps: Readonly<P>, prevState: Readonly<S>): SS | null;
  /**
   * Called immediately after updating occurs. Not called for the initial render.
   *
   * The snapshot is only present if {@link getSnapshotBeforeUpdate} is present and returns non-null.
   */
  componentDidUpdate?(prevProps: Readonly<P>, prevState: Readonly<S>, snapshot?: SS): void;
}

interface ComponentLifecycle<P, S, SS = any> extends NewLifecycle<P, S, SS>, DeprecatedLifecycle<P, S> {
  /**
   * Called immediately after a component is mounted. Setting state here will trigger re-rendering.
   */
  componentDidMount?(): void;
  /**
   * Called to determine whether the change in props and state should trigger a re-render.
   *
   * `Component` always returns true.
   * `PureComponent` implements a shallow comparison on props and state and returns true if any
   * props or states have changed.
   *
   * If false is returned, {@link Component.render}, `componentWillUpdate`
   * and `componentDidUpdate` will not be called.
   */
  shouldComponentUpdate?(nextProps: Readonly<P>, nextState: Readonly<S>, nextContext: any): boolean;
  /**
   * Called immediately before a component is destroyed. Perform any necessary cleanup in this method, such as
   * cancelled network requests, or cleaning up any DOM elements created in `componentDidMount`.
   */
  componentWillUnmount?(): void;
  /**
   * Catches exceptions generated in descendant components. Unhandled exceptions will cause
   * the entire component tree to unmount.
   */
  componentDidCatch?(error: Error, errorInfo: ErrorInfo): void;
}

interface Component<P = {}, S = {}, SS = any> extends ComponentLifecycle<P, S, SS> {}

type JSXElementConstructor<P> =
    | ((
    props: P,
    /**
     * @deprecated
     *
     * @see {@link https://legacy.reactjs.org/docs/legacy-context.html#referencing-context-in-stateless-function-components React Docs}
     */
    deprecatedLegacyContext?: any,
) => ReactNode)
    | (new(
    props: P,
    /**
     * @deprecated
     *
     * @see {@link https://legacy.reactjs.org/docs/legacy-context.html#referencing-context-in-lifecycle-methods React Docs}
     */
    deprecatedLegacyContext?: any,
) => Component<any, any>);

interface ReactElement<
    P = any,
    T extends string | JSXElementConstructor<any> = string | JSXElementConstructor<any>,
> {
  type: T;
  props: P;
  key: string | null;
}

export interface EidolonProviderState {
    usageSeed: number
}

const INITIAL_STATE: EidolonProviderState = {
    usageSeed: 0
}

type ReactNode =
    | ReactElement
    | string
    | number
    | Iterable<ReactNode>
    | ReactPortal
    | boolean
    | null
    | undefined
    | DO_NOT_USE_OR_YOU_WILL_BE_FIRED_EXPERIMENTAL_REACT_NODES[
    keyof DO_NOT_USE_OR_YOU_WILL_BE_FIRED_EXPERIMENTAL_REACT_NODES
    ];

interface FunctionComponent<P = {}> {
  (
      props: P,
      /**
       * @deprecated
       *
       * @see {@link https://legacy.reactjs.org/docs/legacy-context.html#referencing-context-in-lifecycle-methods React Docs}
       */
      deprecatedLegacyContext?: any,
  ): ReactNode;
}

type Dispatch<A> = (value: A) => void;

export type EidolonContextReturningType = [EidolonProviderState, Dispatch<EidolonEvent>];
const EidolonContext = createContext<EidolonContextReturningType>([INITIAL_STATE, () => null]);

export const EidolonProvider: FunctionComponent<PropsWithChildren> = ({ children }) => {
  const initialState: EidolonProviderState = {
    ...INITIAL_STATE
  };
  const value: EidolonContextReturningType = useReducer(EidolonReducer, initialState);
  // @ts-ignore
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