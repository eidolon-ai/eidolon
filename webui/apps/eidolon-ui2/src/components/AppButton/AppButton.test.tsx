import { FunctionComponent } from 'react';
import { render, screen, within } from '@testing-library/react';
import { ThemeProvider } from '../../theme';
import AppButton, { AppButtonProps } from './AppButton';
import DefaultIcon from '@mui/icons-material/MoreHoriz';
import { randomText, capitalize } from '../../utils';

/**
 * AppButton wrapped with Theme Provider
 */
const ComponentToTest: FunctionComponent<AppButtonProps> = (props) => (
  <ThemeProvider>
    <AppButton {...props} />
  </ThemeProvider>
);

/**
 * Test specific color for AppButton
 * @param {string} colorName - name of the color, one of ColorName type
 * @param {string} [expectedClassName] - optional value to be found in className (color "true" may use "success" class name)
 * @param {boolean} [ignoreClassName] - optional flag to ignore className (color "inherit" doesn't use any class name)
 */
function testButtonColor(colorName: string, ignoreClassName = false, expectedClassName = colorName) {
  it(`supports "${colorName}" color`, () => {
    const testId = randomText(8);
    let text = `${colorName} button`;
    render(
      <ComponentToTest
        color={colorName}
        data-testid={testId}
        variant="contained" // Required to get correct CSS class name
      >
        {text}
      </ComponentToTest>
    );

    let button = screen.getByTestId(testId);
    expect(button).toBeDefined();
    // console.log('button.className:', button?.className);
    if (!ignoreClassName) {
      expect(button?.className?.includes('MuiButton-root')).toBeTruthy();
      expect(button?.className?.includes('MuiButton-contained')).toBeTruthy();
      expect(button?.className?.includes(`MuiButton-contained${capitalize(expectedClassName)}`)).toBeTruthy(); // Check for "MuiButton-contained[Primary| Secondary |...]" class
    }
  });
}

describe('<AppButton/> component', () => {
  //   beforeEach(() => {});

  it('renders itself', () => {
    let text = 'sample button';
    const testId = randomText(8);
    render(<ComponentToTest data-testid={testId}>{text}</ComponentToTest>);
    const button = screen.getByTestId(testId);
    expect(button).toBeDefined();
    expect(button).toHaveAttribute('role', 'button');
    expect(button).toHaveAttribute('type', 'button'); // not "submit" or "input" by default
  });

  it('has .margin style by default', () => {
    let text = 'button with default margin';
    const testId = randomText(8);
    render(<ComponentToTest data-testid={testId}>{text}</ComponentToTest>);
    const button = screen.getByTestId(testId);
    expect(button).toBeDefined();
    expect(button).toHaveStyle('margin: 8px'); // Actually it is theme.spacing(1) value
  });

  it('supports .className property', () => {
    let text = 'button with specific class';
    let className = 'someClassName';
    const testId = randomText(8);
    render(
      <ComponentToTest data-testid={testId} className={className}>
        {text}
      </ComponentToTest>
    );
    const button = screen.getByTestId(testId);
    expect(button).toBeDefined();
    expect(button).toHaveClass(className);
  });

  it('supports .label property', () => {
    let text = 'button with label';
    render(<ComponentToTest label={text} />);
    let span = screen.getByText(text);
    expect(span).toBeDefined();
    let button = span.closest('button'); // parent <button> element
    expect(button).toBeDefined();
  });

  it('supports .text property', () => {
    let text = 'button with text';
    render(<ComponentToTest text={text} />);
    let span = screen.getByText(text);
    expect(span).toBeDefined();
    let button = span.closest('button'); // parent <button> element
    expect(button).toBeDefined();
  });

  it('supports .startIcon property as <svg/>', () => {
    let text = 'button with start icon';
    render(<ComponentToTest text={text} startIcon={<DefaultIcon data-testid="startIcon" />} />);
    let button = screen.getByText(text);
    let icon = within(button).getByTestId('startIcon');
    expect(icon).toBeDefined();
    let span = icon.closest('span');
    expect(span).toHaveClass('MuiButton-startIcon');
  });

  it('supports .endIcon property', () => {
    let text = 'button with end icon as <svg/>';
    render(<ComponentToTest text={text} endIcon={<DefaultIcon data-testid="endIcon" />} />);
    let button = screen.getByText(text);
    let icon = within(button).getByTestId('endIcon');
    expect(icon).toBeDefined();
    let span = icon.closest('span');
    expect(span).toHaveClass('MuiButton-endIcon');
  });

  it('supports .startIcon property as string', () => {
    let text = 'button with start icon';
    render(<ComponentToTest text={text} startIcon="default" />);
    let button = screen.getByText(text);
    let icon = within(button).getByTestId('MoreHorizIcon'); //Note: this is valid only when "default" icon is <MoreHorizIcon />
    expect(icon).toBeDefined();
    let span = icon.closest('span');
    expect(span).toHaveClass('MuiButton-startIcon');
  });

  it('supports .endIcon property', () => {
    let text = 'button with end icon as string';
    render(<ComponentToTest text={text} endIcon="default" />);
    let button = screen.getByText(text);
    let icon = within(button).getByTestId('MoreHorizIcon'); //Note: this is valid only when "default" icon is <MoreHorizIcon />
    expect(icon).toBeDefined();
    let span = icon.closest('span');
    expect(span).toHaveClass('MuiButton-endIcon');
  });

  // MUI colors
  testButtonColor('inherit');
  testButtonColor('primary');
  testButtonColor('secondary');
  testButtonColor('error');
  testButtonColor('warning');
  testButtonColor('info');
  testButtonColor('success');

  // Non-MUI colors
  testButtonColor('green', true);
  testButtonColor('#FF00FF', true);
  testButtonColor('rgba(255, 0, 0, 0.5)', true);
});
