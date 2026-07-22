'use client';

import type { NextPage } from 'next';
import { useT } from 'next-i18next/client';
import { useRouter, useSearchParams } from 'next/navigation';
import { useCallback, useEffect, useState } from 'react';

// constants
import { GITHUB_OAUTH_ERROR_EVENT_TYPE, GITHUB_OAUTH_SUCCESS_EVENT_TYPE } from '@/constants';

// errors
import { InternalServerError } from '@/errors/network';

// hooks
import useStore from '@/hooks/useStore';

// services
import AuthAPIService from '@/services/AuthAPIService';

// selectors
import { useLogger } from '@/selectors';

// types
import type { BaseError } from '@/errors/_base';

const GitHubCallbackPage: NextPage = () => {
  const { t } = useT();
  const router = useRouter();
  const searchParams = useSearchParams();
  // selectors
  const logger = useLogger();
  // hooks
  const meAction = useStore(({ meAction }) => meAction);
  const resetAuthAction = useStore(({ resetAuthAction }) => resetAuthAction);
  // states
  const [error, setError] = useState<BaseError | null>(null);
  // callbacks
  const handleCallback = useCallback(async () => {
    const __functionName = 'handleCallback';
    const code = searchParams.get('code');
    const state = searchParams.get('state');
    const authAPIService = new AuthAPIService({ logger });
    let _error: string;

    if (!code || !state) {
      _error = `failed to get authentication code or state from github oauth callback - ${searchParams.toString()}`;

      logger.error(`${GitHubCallbackPage.displayName}#${__functionName}:`, _error);

      return setError(new InternalServerError(_error));
    }

    try {
      await authAPIService.completeGitHubAuth({
        code,
        state,
      });

      // if this is a pop-up, pass the success to the login page to complete authentication
      if (window.opener) {
        window.opener.postMessage(
          {
            type: GITHUB_OAUTH_SUCCESS_EVENT_TYPE,
          },
          window.origin
        );

        return window.close();
      }

      // ... otherwise, fetch user details
      await meAction();

      resetAuthAction();

      // redirect to dashboard
      return router.push('/dashboard');
    } catch (error) {
      // if this is a pop-up, pass the error to the main page
      if (window.opener) {
        window.opener.postMessage(
          {
            type: GITHUB_OAUTH_ERROR_EVENT_TYPE,
          },
          window.origin
        );

        return window.close();
      }

      setError(error as BaseError);
    }
  }, [logger, router, searchParams]);

  useEffect(() => {
    void handleCallback();
  }, [searchParams, router]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="flex flex-col items-center space-y-4">
        <div className="h-14 w-14 animate-spin rounded-full border-2 border-primary border-t-transparent" />

        <p className="text-sm text-muted-foreground">{t('auth:captions.completingAuthentication')}...</p>
      </div>
    </div>
  );
};

GitHubCallbackPage.displayName = 'GitHubCallbackPage';

export default GitHubCallbackPage;
