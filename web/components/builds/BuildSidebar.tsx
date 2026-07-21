'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Plus, LogOut, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { StageBadge } from '@/components/planning/StageBadge';
import { apiService } from '@/services/api';
import type { BuildSummary } from '@/types';
import { useAuth } from '@/hooks/useAuth';

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [builds, setBuilds] = useState<BuildSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBuilds();
  }, []);

  async function fetchBuilds() {
    try {
      setLoading(true);
      const { data } = await apiService.getBuildSessions();
      if (data) {
        setBuilds(data);
      }
    } catch (err) {
      console.error('Failed to fetch builds:', err);
    } finally {
      setLoading(false);
    }
  }

  const isCurrentBuild = (id: string) => pathname === `/dashboard/build/${id}`;

  return (
    <div className="flex h-full flex-col overflow-hidden bg-sidebar text-sidebar-foreground">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-sidebar-border px-4 py-4">
        <h2 className="font-light text-sidebar-foreground">Qernel</h2>
        <Button size="sm" variant="ghost" className="h-8 w-8 p-0" asChild>
          <Link href="/dashboard?new=true" title="New Build">
            <Plus size={16} />
          </Link>
        </Button>
      </div>

      {/* User Info */}
      <div className="border-b border-sidebar-border px-4 py-3">
        {user && (
          <div className="flex items-center gap-3">
            {user.avatarUrl && <img src={user.avatarUrl} alt={user.username} className="h-8 w-8 rounded-full" />}
            <div className="flex-1 overflow-hidden">
              <p className="truncate text-sm font-medium">{user.username}</p>
              <p className="truncate text-xs text-sidebar-accent-foreground">{user.email}</p>
            </div>
          </div>
        )}
      </div>

      {/* Builds List */}
      <div className="flex-1 overflow-auto">
        {loading ? (
          <div className="space-y-2 px-2 py-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-12 rounded bg-sidebar-accent/50 animate-pulse" />
            ))}
          </div>
        ) : builds.length === 0 ? (
          <div className="px-4 py-6 text-center text-sm text-sidebar-accent-foreground">
            No builds yet. Create one to get started.
          </div>
        ) : (
          <div className="space-y-1 px-2 py-2">
            {builds.map((build) => (
              <Link
                key={build.id}
                href={`/dashboard/build/${build.id}`}
                className={`block rounded-lg p-3 transition-colors ${
                  isCurrentBuild(build.id)
                    ? 'bg-sidebar-primary/20 text-sidebar-primary-foreground'
                    : 'hover:bg-sidebar-accent/50'
                }`}
              >
                <div className="flex items-start gap-2">
                  <div className="flex-1 overflow-hidden">
                    <p className="truncate text-sm font-medium">{build.title || 'Untitled Build'}</p>
                    <p className="truncate text-xs text-sidebar-accent-foreground">
                      {build.prompt.substring(0, 40)}...
                    </p>
                    <div className="mt-2">
                      <StageBadge stage={build.stage} />
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-sidebar-border space-y-1 px-2 py-3">
        <Button
          size="sm"
          variant="ghost"
          className="w-full justify-start gap-2 text-sidebar-accent-foreground hover:text-sidebar-foreground"
          asChild
        >
          <Link href="/settings">
            <Settings size={16} />
            Settings
          </Link>
        </Button>
        <Button
          onClick={logout}
          size="sm"
          variant="ghost"
          className="w-full justify-start gap-2 text-sidebar-accent-foreground hover:text-sidebar-foreground"
        >
          <LogOut size={16} />
          Logout
        </Button>
      </div>
    </div>
  );
}
