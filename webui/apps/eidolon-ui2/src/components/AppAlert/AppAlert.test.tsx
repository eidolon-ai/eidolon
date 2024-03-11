import { render, screen } from '@testing-library/react';
import AppAlert from './AppAlert';
import { capitalize, randomText } from '../../utils';
import { AlertProps } from '@mui/material';

const ComponentToTest = AppAlert;

/**
 * Tests for <AppAlert/> component
 */
describe('<AppAlert/> component', () => {
  it('renders itself', () => {
    const testId = randomText(8);
    render(<ComponentToTest data-testid={testId} />);
    const alert = screen.getByTestId(testId);
    expect(alert).toBeDefined();
    expect(alert).toHaveAttribute('role', 'alert');
    expect(alert).toHaveClass('MuiAlert-root');
  });

  it('supports .severity property', () => {
    const SEVERITIES = ['error', 'info', 'success', 'warning'];
    for (const severity of SEVERITIES) {
      const testId = randomText(8);
      const severity = 'success';
      render(
        <ComponentToTest
          data-testid={testId}
          severity={severity}
          variant="filled" // Needed to verify exact MUI classes
        />
      );
      const alert = screen.getByTestId(testId);
      expect(alert).toBeDefined();
      expect(alert).toHaveClass(`MuiAlert-filled${capitalize(severity)}`);
    }
  });

  it('supports .variant property', () => {
    const VARIANTS = ['filled', 'outlined', 'standard'];
    for (const variant of VARIANTS) {
      const testId = randomText(8);
      render(
        <ComponentToTest
          data-testid={testId}
          variant={variant as AlertProps['variant']}
          severity="warning" // Needed to verify exact MUI classes
        />
      );
      const alert = screen.getByTestId(testId);
      expect(alert).toBeDefined();
      expect(alert).toHaveClass(`MuiAlert-${variant}Warning`);
    }
  });
});
