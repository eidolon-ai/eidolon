import { Stack, Typography } from '@mui/material';
import { NextPage } from 'next';

/**
 * Renders About Application page
 * @page About
 */
const AboutPage: NextPage = () => {
  return (
    <Stack spacing={2} padding={2}>
      <Stack>
        <Typography variant="h3">About application</Typography>
      </Stack>
      <Stack>
        <Typography variant="h4">Reusable components</Typography>
      </Stack>
    </Stack>
  );
};

export default AboutPage;
