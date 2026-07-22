'use client';

import type { NextPage } from 'next';
import { Trans, useT } from 'next-i18next/client';
import { useRouter } from 'next/navigation';
import { useCallback, useEffect, useRef } from 'react';

// components
import Button from '@/components/ui/Button';
import ColorSchemeToggle from '@/components/common/ColorSchemeToggle';
import GitHubIcon from '@/components/social/GitHubIcon';

// constants
import { GITHUB_OAUTH_ERROR_EVENT_TYPE, GITHUB_OAUTH_SUCCESS_EVENT_TYPE, GITHUB_OAUTH_WINDOW_ID } from '@/constants';

// hooks
import useStore from '@/hooks/useStore';

// providers
import LoginRouteProvider from '@/providers/LoginRouteProvider';

// selectors
import { useLogger } from '@/selectors/logging';

const LoginPage: NextPage = () => {
  const { t } = useT();
  const router = useRouter();
  // refs
  const githubOAuthWindowRef = useRef<Window>(null);
  // selectors
  const logger = useLogger();
  // hooks
  const authenticating = useStore(({ authenticating }) => authenticating);
  const authenticationError = useStore(({ authenticationError }) => authenticationError);
  const githubOAuthHandshake = useStore(({ githubOAuthHandshake }) => githubOAuthHandshake);
  const meAction = useStore(({ meAction }) => meAction);
  const resetAuthAction = useStore(({ resetAuthAction }) => resetAuthAction);
  const startGitHubOAuthAction = useStore(({ startGitHubOAuthAction }) => startGitHubOAuthAction);
  // callbacks
  const handleCancelLoginClick = useCallback(() => {
    // close the github oauth window if it is open
    if (githubOAuthWindowRef.current) {
      githubOAuthWindowRef.current.close();
    }

    resetAuthAction();
  }, [githubOAuthWindowRef.current, resetAuthAction]);
  const handleGitHubLoginClick = useCallback(() => {
    void startGitHubOAuthAction();
  }, []);
  const onGitHubOAuthWindowMessage = useCallback(
    async (event: MessageEvent) => {
      const __functionName = 'onGitHubOAuthWindowMessage';

      if (event.origin !== window.origin) {
        return;
      }

      if (event.data?.type === GITHUB_OAUTH_SUCCESS_EVENT_TYPE) {
        window.removeEventListener('message', onGitHubOAuthWindowMessage);
        githubOAuthWindowRef.current?.close();

        logger.debug(`${LoginPage.displayName}#${__functionName}: successfully logged in via github, redirecting`);

        // fetch the user details
        await meAction();

        return resetAuthAction();
      }

      if (event.data?.type === GITHUB_OAUTH_ERROR_EVENT_TYPE) {
        window.removeEventListener('message', onGitHubOAuthWindowMessage);
        githubOAuthWindowRef.current?.close();

        logger.error(`${LoginPage.displayName}#${__functionName}:`, event.data.error);

        // TODO: set authentication error
      }
    },
    [githubOAuthWindowRef.current, logger, router]
  );

  useEffect(() => {
    if (!githubOAuthWindowRef.current && githubOAuthHandshake) {
      // attempt to open a pop-up
      githubOAuthWindowRef.current = window.open(
        githubOAuthHandshake.authorizeUrl,
        GITHUB_OAUTH_WINDOW_ID,
        'width=600,height=700,resizable=yes,scrollbars=yes'
      );

      // fallback to a hard redirect
      if (!githubOAuthWindowRef.current) {
        window.location.assign(githubOAuthHandshake.authorizeUrl);

        return;
      }

      window.addEventListener('message', onGitHubOAuthWindowMessage);
    }

    return () => window.removeEventListener('message', onGitHubOAuthWindowMessage);
  }, [githubOAuthHandshake]);

  return (
    <LoginRouteProvider>
      <div className="flex min-h-screen items-center justify-center bg-background">
        {/* color scheme toggle - top right */}
        <div className="absolute right-4 top-4">
          <ColorSchemeToggle />
        </div>

        <div className="flex w-full max-w-md flex-col items-center justify-center px-4">
          <div className="mb-8 space-y-2 text-center">
            <h1 className="text-3xl font-light tracking-tight text-foreground">{process.env.NEXT_PUBLIC_APP_TITLE}</h1>
            <p className="text-sm text-muted-foreground">{process.env.NEXT_PUBLIC_APP_DESCRIPTION}</p>
          </div>

          {authenticating ? (
            <div className="w-full space-y-4">
              <div className="flex flex-col items-center space-y-4">
                <div className="h-14 w-14 animate-spin rounded-full border-2 border-primary border-t-transparent" />
                <p className="text-sm text-muted-foreground">{t('auth:captions.authenticating')}...</p>
              </div>

              <Button className="w-full gap-2" onClick={handleCancelLoginClick} size="lg" variant="default">
                {t('common:labels.cancel')}
              </Button>
            </div>
          ) : (
            <div className="w-full space-y-4">
              <Button className="w-full gap-2" onClick={handleGitHubLoginClick} size="lg" variant="default">
                <GitHubIcon size={5} />

                {t('auth:labels.continueWithGitHub')}
              </Button>

              {authenticationError && (
                <div className="rounded-lg border border-destructive/20 bg-destructive/5 p-3 text-sm text-destructive">
                  {`${authenticationError.code}: ${authenticationError.message}`}
                </div>
              )}
            </div>
          )}

          <div className="mt-8 text-center text-xs text-muted-foreground">
            <p>
              <Trans
                components={[<a className="underline hover:text-foreground" href="/terms-of-service" key="tos" />]}
                i18nKey="auth:captions.agreeToTerms"
                t={t}
              />
            </p>
          </div>
        </div>
      </div>
    </LoginRouteProvider>
  );
};

LoginPage.displayName = 'LoginPage';

export default LoginPage;
