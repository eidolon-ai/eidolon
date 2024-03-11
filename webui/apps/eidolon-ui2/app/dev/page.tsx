import { NextPage } from 'next';
import { redirect } from 'next/navigation';
import { Stack, Typography } from '@mui/material';
import DemoAppAlert from './components/DemoAppAlerts';
import DemoAppButton from './components/DemoAppButton';
import DemoAppIcon from './components/DemoAppIcon';
import DemoAppIconButton from './components/DemoAppIconButton';
import DemoAppImage from './components/DemoAppImage';

/**
 * Renders Development tools when env.NEXT_PUBLIC_DEBUG is true
 * @page Dev
 */
const DevPage: NextPage = () => {
  if (!process.env.NEXT_PUBLIC_DEBUG) {
    redirect('/');
    return null; // Hide this page on when env.NEXT_PUBLIC_DEBUG is not set
  }

  return (
    <Stack spacing={2} padding={2}>
      <Stack>
        <Typography variant="h3">DevTools page</Typography>
        <Typography variant="body1">This page is not visible on production.</Typography>
      </Stack>

      <Stack alignItems="center" spacing={1}>
        <DemoAppIcon />
        <DemoAppIconButton />
        <DemoAppImage />
        <DemoAppAlert />
        <DemoAppButton />
      </Stack>
    </Stack>
  );
};

export default DevPage;
