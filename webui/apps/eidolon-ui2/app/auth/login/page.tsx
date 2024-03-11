'use client';
import { NextPage } from 'next';
import Head from 'next/head';
import { Stack } from '@mui/material';
import { AppButton } from '@/components';
import { useAppStore } from '@/store';
import { useRouter } from 'next/navigation';
import { useEventLogout } from '@/hooks';
import { sessionStorageSet } from '@/utils/sessionStorage';

/**
 * User Login page
 * @page Login
 */
const Login: NextPage = () => {
  const router = useRouter();
  const [, dispatch] = useAppStore();
  const onLogout = useEventLogout();

  const onLogin = () => {
    // TODO: AUTH: Sample of access token store, replace next line in real application
    sessionStorageSet('access_token', 'save-real-access-token-here');

    dispatch({ type: 'LOG_IN' });
    router.push('/');
  };

  return (
    <>
      <Head>
        <title>Login - _TITLE_</title>
      </Head>

      <Stack alignItems="center" spacing={2} padding={2}>
        <Stack>Put form controls or add social login buttons here...</Stack>

        <Stack direction="row">
          <AppButton color="success" onClick={onLogin}>
            Emulate User Login
          </AppButton>
          <AppButton color="warning" onClick={onLogout}>
            Logout User
          </AppButton>
        </Stack>
      </Stack>
    </>
  );
};

export default Login;
