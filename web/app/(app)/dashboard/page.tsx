'use client';

import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { NewBuildComposer } from '@/components/builds/NewBuildComposer';
import { BuildList } from '@/components/builds/BuildList';

export default function DashboardPage() {
  const searchParams = useSearchParams();
  const [showNewBuild, setShowNewBuild] = useState(searchParams.get('new') === 'true');

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="border-b border-border bg-card px-6 py-4 md:py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-light tracking-tight">Builds</h1>
            <p className="mt-1 text-sm text-muted-foreground">Manage your software generation projects</p>
          </div>
          <Button onClick={() => setShowNewBuild(!showNewBuild)} className="gap-2">
            <Plus size={16} />
            New Build
          </Button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        {showNewBuild ? (
          <div className="p-6 md:p-8">
            <NewBuildComposer onClose={() => setShowNewBuild(false)} />
          </div>
        ) : (
          <BuildList />
        )}
      </div>
    </div>
  );
}
