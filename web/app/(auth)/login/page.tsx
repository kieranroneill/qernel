'use client';

import type { NextPage } from 'next';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

// components
import { Button } from '@/components/ui/button';
import ColorSchemeToggle from '@/components/common/ColorSchemeToggle';

// errors
import type { BaseError } from '@/errors/_base';

// services
import AuthAPIService from '@/services/AuthAPIService';
import { apiService } from '@/services/api';

// types
import type { GitHubAuthStartResponseBody } from '@/types/auth';

const LoginPage: NextPage = () => {
  const router = useRouter();
  // states
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<BaseError | null>(null);

  useEffect(() => {
    // Check if user is already authenticated
    const checkAuth = async () => {
      const { data } = await apiService.getCurrentUser();
      if (data) {
        router.push('/dashboard');
      }
    };
    void checkAuth();
  }, [router]);

  const handleGithubLogin = async () => {
    const authAPIService = new AuthAPIService();
    let result: GitHubAuthStartResponseBody;

    try {
      setLoading(true);
      setError(null);

      result = await authAPIService.startGitHubAuth();

      window.location.href = result.authorizeUrl;
    } catch (_error) {
      setError(_error as BaseError);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      {/* Theme Toggle - Top Right */}
      <div className="absolute right-4 top-4">
        <ColorSchemeToggle />
      </div>

      <div className="flex w-full max-w-md flex-col items-center justify-center px-4">
        <div className="mb-8 space-y-2 text-center">
          <h1 className="text-3xl font-light tracking-tight text-foreground">Qernel</h1>
          <p className="text-sm text-muted-foreground">Local-first software generation workspace</p>
        </div>

        <div className="w-full space-y-4">
          <Button onClick={handleGithubLogin} disabled={loading} size="lg" className="w-full gap-2" variant="outline">
            {loading ? (
              <>
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-foreground border-t-transparent" />
                Redirecting...
              </>
            ) : (
              <>
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v 3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                </svg>
                Continue with GitHub
              </>
            )}
          </Button>

          {error && (
            <div className="rounded-lg border border-destructive/20 bg-destructive/5 p-3 text-sm text-destructive">
              {error.message}
            </div>
          )}
        </div>

        <div className="mt-8 text-center text-xs text-muted-foreground">
          <p>
            By logging in, you agree to our{' '}
            <a href="#" className="underline hover:text-foreground">
              Terms of Service
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

LoginPage.displayName = 'LoginPage';

export default LoginPage;
