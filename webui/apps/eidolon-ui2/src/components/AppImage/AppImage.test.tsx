import { render, screen } from '@testing-library/react';
import { randomText } from '../../utils';
import AppImage from './AppImage';

const ComponentToTest = AppImage;

/**
 * Tests for <AppImage/> component
 */
describe('<AppImage/> component', () => {
  const src = 'https:/domain.com/image.jpg';

  it('renders itself', () => {
    const testId = randomText(8);
    render(<ComponentToTest data-testid={testId} src={src} />);
    const image = screen.getByTestId(testId);
    expect(image).toBeDefined();
    expect(image).toHaveAttribute('src', src);
    expect(image).toHaveAttribute('alt', 'Image'); // Default prop value
    expect(image).toHaveAttribute('height', '256'); // Default prop value
    expect(image).toHaveAttribute('width', '256'); // Default prop value
  });

  it('supports .width and .height props', () => {
    const testId = randomText(8);
    const height = 345;
    const width = 123;
    render(<ComponentToTest data-testid={testId} height={height} src={src} width={width} />);
    const image = screen.getByTestId(testId);
    expect(image).toBeDefined();
    expect(image).toHaveAttribute('height', String(height));
    expect(image).toHaveAttribute('width', String(width));
  });

  it('supports .title property', () => {
    const testId = randomText(8);
    const title = randomText(16);
    render(<ComponentToTest data-testid={testId} src={src} title={title} />);
    const image = screen.getByTestId(testId);
    expect(image).toBeDefined();
    expect(image).toHaveAttribute('title', title);
    expect(image).toHaveAttribute('alt', title); // When title is provided, it is used as alt
  });

  it('supports .alt property even when .title is provided', () => {
    const testId = randomText(8);
    const title = randomText(16);
    const alt = randomText(32);
    render(<ComponentToTest alt={alt} data-testid={testId} src={src} title={title} />);
    const image = screen.getByTestId(testId);
    expect(image).toBeDefined();
    expect(image).toHaveAttribute('alt', alt);
    expect(image).toHaveAttribute('title', title);
  });
});
