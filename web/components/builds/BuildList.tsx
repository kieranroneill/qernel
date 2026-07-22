'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Calendar, ArrowRight } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { StageBadge } from '@/components/planning/StageBadge';
import { apiService } from '@/services/api';
import type { BuildSummary } from '@/types';

// components
import Button from '@/components/ui/Button';

export function BuildList() {
  const [builds, setBuilds] = useState<BuildSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBuilds();
  }, []);

  async function fetchBuilds() {
    try {
      setLoading(true);
      const { data, error } = await apiService.getBuildSessions();

      if (error) {
        setError(error.message);
      } else if (data) {
        setBuilds(data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch builds');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="p-6 md:p-8">
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-32 rounded-lg bg-muted/50 animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 md:p-8">
        <Card className="border-destructive/20 bg-destructive/5">
          <div className="p-6">
            <h3 className="font-medium text-destructive">Error</h3>
            <p className="mt-2 text-sm text-destructive/80">{error}</p>
            <Button onClick={fetchBuilds} variant="outline" size="sm" className="mt-4">
              Try Again
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  if (builds.length === 0) {
    return (
      <div className="flex h-full items-center justify-center p-6 md:p-8">
        <div className="max-w-md text-center">
          <h3 className="text-lg font-medium">No builds yet</h3>
          <p className="mt-2 text-sm text-muted-foreground">Create your first build to get started with Qernel</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 md:p-8">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {builds.map((build) => (
          <Link key={build.id} href={`/dashboard/build/${build.id}`}>
            <Card className="group h-full transition-colors hover:bg-muted">
              <div className="flex h-full flex-col p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1 overflow-hidden">
                    <h3 className="font-medium group-hover:text-primary">{build.title || 'Untitled Build'}</h3>
                    <p className="mt-1 line-clamp-2 text-sm text-muted-foreground">{build.prompt}</p>
                  </div>
                </div>

                <div className="mt-4 flex items-end justify-between">
                  <div className="flex flex-col gap-2">
                    <StageBadge stage={build.stage} />
                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                      <Calendar size={12} />
                      {new Date(build.createdAt).toLocaleDateString()}
                    </div>
                  </div>
                  <ArrowRight className="h-4 w-4 opacity-0 transition-opacity group-hover:opacity-100" />
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
