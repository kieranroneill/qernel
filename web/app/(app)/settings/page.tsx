'use client';

import { useAuth } from '@/hooks/useAuth';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

// components
import ColorSchemeToggle from '@/components/common/ColorSchemeToggle';

// hooks
import useStore from '@/hooks/useStore';

export default function SettingsPage() {
  const { user } = useAuth();
  // hooks
  const colorScheme = useStore(({ appearanceSettings }) => appearanceSettings.colorScheme);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-light tracking-tight text-foreground">Settings</h1>
        <p className="mt-1 text-sm text-muted-foreground">Manage your preferences and account settings</p>
      </div>

      {/* Appearance Section */}
      <Card>
        <CardHeader>
          <CardTitle>Appearance</CardTitle>
          <CardDescription>Customize how Qernel looks on your device</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-foreground">Theme</label>
            <p className="mb-3 text-xs text-muted-foreground">Choose between light, dark, or system theme</p>
            <ColorSchemeToggle />
            <p className="mt-2 text-xs text-muted-foreground">
              Current theme: <span className="capitalize">{colorScheme}</span>
              {colorScheme === 'system' && (
                <span> (displaying as {localStorage.getItem('theme') === 'system' ? 'system default' : 'custom'})</span>
              )}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Account Section */}
      <Card>
        <CardHeader>
          <CardTitle>Account</CardTitle>
          <CardDescription>Your GitHub account information</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {user ? (
            <>
              <div className="flex items-start gap-4">
                {user.avatarUrl && (
                  <img
                    src={user.avatarUrl}
                    alt={user.username}
                    className="h-16 w-16 rounded-full border border-border"
                  />
                )}
                <div>
                  <p className="text-sm font-medium text-foreground">{user.username}</p>
                  <p className="text-sm text-muted-foreground">{user.email}</p>

                  <p className="mt-2 text-xs text-muted-foreground">GitHub ID: {user.githubId}</p>
                </div>
              </div>
            </>
          ) : (
            <p className="text-sm text-muted-foreground">Loading account information...</p>
          )}
        </CardContent>
      </Card>

      {/* About Section */}
      <Card>
        <CardHeader>
          <CardTitle>About</CardTitle>
          <CardDescription>Information about Qernel</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="text-sm font-medium text-foreground">Qernel</p>
            <p className="text-sm text-muted-foreground">Local-first software generation workspace</p>
            <p className="mt-2 text-xs text-muted-foreground">Version 1.0.0</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
