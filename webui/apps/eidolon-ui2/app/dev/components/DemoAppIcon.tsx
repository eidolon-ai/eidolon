'use client';
import { useState } from 'react';
import copyToClipboard from 'copy-to-clipboard';
import { Box, Card, CardContent, CardHeader, Snackbar } from '@mui/material';
import { AppIconButton } from '@/components';
import { ICONS } from '@/components/AppIcon/AppIcon';

/**
 * Renders "Demo Section" for AppIcon component
 * @component DemoAppIcon
 */
const DemoAppIcon = () => {
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  return (
    <Card>
      <CardHeader title="AppIcon" subheader="A sample of each registered AppIcon. Click to copy the JSX code." />
      <CardContent sx={{ px: 1, py: 0 }}>
        <Box>
          {Object.keys(ICONS).map((icon) => (
            <AppIconButton
              key={icon}
              icon={icon}
              title={icon}
              onClick={() => {
                copyToClipboard(`<AppIcon icon="${icon}" />`);
                setSnackbarOpen(true); // Show snackbar
                setTimeout(() => setSnackbarOpen(false), 3000); // Hide snackbar after small delay
              }}
            />
          ))}
        </Box>
        <Snackbar
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          ContentProps={{
            sx: { display: 'block', textAlign: 'center' },
          }}
          open={snackbarOpen}
          message="JSX code copied to Clipboard"
        />
      </CardContent>
    </Card>
  );
};

export default DemoAppIcon;
