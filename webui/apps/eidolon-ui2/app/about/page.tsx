import { Stack, Typography } from '@mui/material';
import { NextPage } from 'next';
import { AppLink } from '@/components';

/**
 * Renders About Application page
 * @page About
 */
const AboutPage: NextPage = () => {
  return (
    <Stack spacing={2} padding={2}>
      <Stack>
        <Typography variant="h3">About application</Typography>
        <Typography variant="body1">
          This application is a mix of{' '}
          <AppLink href="https://nextjs.org/docs/api-reference/create-next-app">Create Next App</AppLink> and{' '}
          <AppLink href="https://mui.com/">MUI</AppLink> with set of reusable components and utilities to build
          professional <AppLink href="https://nextjs.org/">NextJS</AppLink> application faster.
        </Typography>
      </Stack>
      <Stack>
        <Typography variant="h4">Reusable components</Typography>
        <Typography variant="body1">
          Demo of reusable components is available on <AppLink to="/dev">DevTools page</AppLink>
        </Typography>
      </Stack>
    </Stack>
  );
};

export default AboutPage;
