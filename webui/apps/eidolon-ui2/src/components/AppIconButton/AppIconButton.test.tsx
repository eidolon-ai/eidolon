import { fireEvent, render, screen } from '@testing-library/react';
import AppIconButton, { MUI_ICON_BUTTON_COLORS } from './AppIconButton';
import { APP_ICON_SIZE } from '../config';
import { ObjectPropByName, capitalize, randomColor, randomText } from '../../utils';
import { ICONS } from '../AppIcon/AppIcon';

const ComponentToTest = AppIconButton;

function randomPropertyName(obj: object): string {
  const objectProperties = Object.keys(obj);
  const propertyName = objectProperties[Math.floor(Math.random() * objectProperties.length)];
  return propertyName;
}

function randomPropertyValue(obj: object): unknown {
  const propertyName = randomPropertyName(obj);
  return (obj as ObjectPropByName)[propertyName];
}

/**
 * Tests for <AppIconButton/> component
 */
describe('<AppIconButton/> component', () => {
  it('renders itself', () => {
    const testId = randomText(8);
    render(<ComponentToTest data-testid={testId} />);

    // Button
    const button = screen.getByTestId(testId);
    expect(button).toBeDefined();
    expect(button).toHaveAttribute('role', 'button');
    expect(button).toHaveAttribute('type', 'button');

    // Icon
    const svg = button.querySelector('svg');
    expect(svg).toBeDefined();
    expect(svg).toHaveAttribute('data-icon', 'default'); // default icon
    expect(svg).toHaveAttribute('size', String(APP_ICON_SIZE)); // default size
    expect(svg).toHaveAttribute('height', String(APP_ICON_SIZE)); // default size when .size is not set
    expect(svg).toHaveAttribute('width', String(APP_ICON_SIZE)); // default size when .size is not se
  });

  it('supports .color property', () => {
    for (const color of [...MUI_ICON_BUTTON_COLORS, randomColor(), randomColor(), randomColor()]) {
      const testId = randomText(8);
      const icon = randomPropertyName(ICONS) as string;
      render(<ComponentToTest data-testid={testId} color={color} icon={icon} />);

      // Button
      const button = screen.getByTestId(testId);
      expect(button).toBeDefined();

      if (color == 'default') {
        return; // Nothing to test for default color
      }

      if (MUI_ICON_BUTTON_COLORS.includes(color)) {
        expect(button).toHaveClass(`MuiIconButton-color${capitalize(color)}`);
      } else {
        expect(button).toHaveStyle({ color: color });
      }
    }
  });

  it('supports .disable property', () => {
    const testId = randomText(8);
    const title = randomText(16);
    render(<ComponentToTest data-testid={testId} disabled />);

    // Button
    const button = screen.getByTestId(testId);
    expect(button).toBeDefined();
    expect(button).toHaveAttribute('aria-disabled', 'true');
    expect(button).toHaveClass('Mui-disabled');
  });

  it('supports .icon property', () => {
    // Verify that all icons are supported
    for (const icon of Object.keys(ICONS)) {
      const testId = randomText(8);
      render(<ComponentToTest data-testid={testId} icon={icon} />);

      // Button
      const button = screen.getByTestId(testId);
      expect(button).toBeDefined();

      // Icon
      const svg = button.querySelector('svg');
      expect(button).toBeDefined();
      expect(svg).toHaveAttribute('data-icon', icon.toLowerCase());
    }
  });

  it('supports .size property', () => {
    const sizes = ['small', 'medium', 'large'] as const; //  as IconButtonProps['size'][];
    for (const size of sizes) {
      const testId = randomText(8);
      render(<ComponentToTest data-testid={testId} size={size} />);

      // Button
      const button = screen.getByTestId(testId);
      expect(button).toBeDefined();
      expect(button).toHaveClass(`MuiIconButton-size${capitalize(size)}`); // MuiIconButton-sizeSmall | MuiIconButton-sizeMedium | MuiIconButton-sizeLarge
    }
  });

  it('supports .title property', async () => {
    const testId = randomText(8);
    const title = randomText(16);
    render(<ComponentToTest data-testid={testId} title={title} />);

    // Button
    const button = screen.getByTestId(testId);
    expect(button).toBeDefined();
    expect(button).toHaveAttribute('aria-label', title);

    // Emulate mouseover event to show tooltip
    await fireEvent(button, new MouseEvent('mouseover', { bubbles: true }));

    // Tooltip is rendered in a separate div, so we need to find it by role
    const tooltip = await screen.findByRole('tooltip');
    expect(tooltip).toBeDefined();
    expect(tooltip).toHaveTextContent(title);
    expect(tooltip).toHaveClass('MuiTooltip-popper');
  });
});
