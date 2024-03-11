import { redirect } from 'next/navigation';
/**
 * Redirects to default Auth page
 * @page Auth
 * @redirect /auth/login
 */
const AuthPage = () => {
  redirect('/auth/login');
};

export default AuthPage;
