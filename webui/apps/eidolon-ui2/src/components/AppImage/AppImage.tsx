import { FunctionComponent } from 'react';
import NextImage, { ImageProps } from 'next/image';

interface AppImageProps extends Omit<ImageProps, 'alt'> {
  alt?: string; // Make property optional as it was before NextJs v13
}

/**
 * Application wrapper around NextJS image with some default props
 * @component AppImage
 */
const AppImage: FunctionComponent<AppImageProps> = ({
  title, // Note: value has be destructed before usage as default value for other property
  alt = title ?? 'Image',
  height = 256,
  width = 256,
  ...restOfProps
}) => {
  // Uses custom loader + unoptimized="true" to avoid NextImage warning https://nextjs.org/docs/api-reference/next/image#unoptimized
  return <NextImage alt={alt} height={height} title={title} unoptimized={true} width={width} {...restOfProps} />;
};

export default AppImage;
