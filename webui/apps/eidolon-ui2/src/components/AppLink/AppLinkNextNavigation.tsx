'use client';
// See: https://github.com/mui-org/material-ui/blob/6b18675c7e6204b77f4c469e113f62ee8be39178/examples/nextjs-with-typescript/src/Link.tsx
/* eslint-disable jsx-a11y/anchor-has-content */
import { AnchorHTMLAttributes, forwardRef } from 'react';
import clsx from 'clsx';
import { usePathname } from 'next/navigation';
import NextLink, { LinkProps as NextLinkProps } from 'next/link';
import MuiLink, { LinkProps as MuiLinkProps } from '@mui/material/Link';
import { APP_LINK_COLOR, APP_LINK_UNDERLINE } from '../config';

export const EXTERNAL_LINK_PROPS = {
  target: '_blank',
  rel: 'noopener noreferrer',
};

/**
 * Props for NextLinkComposed component
 */
interface NextLinkComposedProps
  extends Omit<AnchorHTMLAttributes<HTMLAnchorElement>, 'href'>,
    Omit<NextLinkProps, 'href' | 'as' | 'onClick' | 'onMouseEnter'> {
  to: NextLinkProps['href'];
  linkAs?: NextLinkProps['as'];
  href?: NextLinkProps['href'];
}

/**
 * NextJS composed link to use with Material UI
 * @NextLinkComposed NextLinkComposed
 */
const NextLinkComposed = forwardRef<HTMLAnchorElement, NextLinkComposedProps>(function NextLinkComposed(
  { to, linkAs, href, replace, scroll, passHref, shallow, prefetch, ...restOfProps },
  ref
) {
  return (
    <NextLink
      legacyBehavior={true} // TODO: Remove when MUI become compatible with NextJs 13+
      href={to}
      prefetch={prefetch}
      as={linkAs}
      replace={replace}
      scroll={scroll}
      shallow={shallow}
      passHref={passHref}
    >
      <a ref={ref} {...restOfProps} />
    </NextLink>
  );
});

/**
 * Props for AppLinkForNext component
 */
export type AppLinkForNextProps = {
  activeClassName?: string;
  as?: NextLinkProps['as'];
  href?: string | NextLinkProps['href'];
  noLinkStyle?: boolean;
  to?: string | NextLinkProps['href'];
  openInNewTab?: boolean;
} & Omit<NextLinkComposedProps, 'to' | 'linkAs' | 'href'> &
  Omit<MuiLinkProps, 'href'>;

/**
 * Material UI link for NextJS
 * A styled version of the Next.js Link component: https://nextjs.org/docs/#with-link
 * @component AppLinkForNext
 * @param {string} [activeClassName] - class name for active link, applied when the router.pathname matches .href or .to props
 * @param {string} [as] - passed to NextJS Link component in .as prop
 * @param {string} [className] - class name for <a> tag or NextJS Link component
 * @param {object|function} children - content to wrap with <a> tag
 * @param {string} [color] - color of the link
 * @param {boolean} [noLinkStyle] - when true, link will not have MUI styles
 * @param {string} [to] - internal link URI
 * @param {string} [href] - external link URI
 * @param {boolean} [openInNewTab] - link will be opened in new tab when true
 * @param {string} [underline] - controls "underline" style of the MUI link: 'hover' | 'always' | 'none'
 */
const AppLinkForNext = forwardRef<HTMLAnchorElement, AppLinkForNextProps>(function Link(props, ref) {
  const {
    activeClassName = 'active', // This class is applied to the Link component when the router.pathname matches the href/to prop
    as: linkAs,
    className: classNameProps,
    href,
    noLinkStyle,
    role, // Link don't have roles, so just exclude it from ...restOfProps
    color = APP_LINK_COLOR,
    underline = APP_LINK_UNDERLINE,
    to,
    sx,
    openInNewTab = Boolean(href), // Open external links in new Tab by default
    ...restOfProps
  } = props;
  const currentPath = usePathname();
  const destination = to ?? href ?? '';
  const pathname = typeof destination === 'string' ? destination : destination.pathname;
  const className = clsx(classNameProps, {
    [activeClassName]: pathname == currentPath && activeClassName,
  });

  const isExternal =
    typeof destination === 'string' && (destination.startsWith('http') || destination.startsWith('mailto:'));

  const propsToRender = {
    color,
    underline, // 'hover' | 'always' | 'none'
    ...(openInNewTab && EXTERNAL_LINK_PROPS),
    ...restOfProps,
  };

  if (isExternal) {
    if (noLinkStyle) {
      return <a className={className} href={destination as string} ref={ref as any} {...propsToRender} />;
    }

    return <MuiLink className={className} href={destination as string} ref={ref} sx={sx} {...propsToRender} />;
  }

  if (noLinkStyle) {
    return <NextLinkComposed className={className} ref={ref as any} to={destination} {...propsToRender} />;
  }

  return (
    <MuiLink
      component={NextLinkComposed}
      linkAs={linkAs}
      className={className}
      ref={ref}
      to={destination}
      sx={sx}
      {...propsToRender}
    />
  );
});

export default AppLinkForNext;
