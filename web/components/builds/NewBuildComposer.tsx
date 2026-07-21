'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { apiService } from '@/services/api';
import type { ApiError } from '@/types';
import { Card } from '@/components/ui/card';

interface NewBuildComposerProps {
  onClose: () => void;
}

export function NewBuildComposer({ onClose }: NewBuildComposerProps) {
  const router = useRouter();
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!prompt.trim()) {
      setError({ message: 'Please enter a prompt' });
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const { data, error } = await apiService.createBuild(prompt);

      if (error) {
        setError(error);
      } else if (data) {
        // Navigate to the new build
        router.push(`/dashboard/build/${data.id}`);
      }
    } catch (err) {
      setError({
        message: err instanceof Error ? err.message : 'Failed to create build',
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className="w-full max-w-2xl">
      <div className="border-b border-border p-6">
        <h2 className="text-lg font-medium">Create a New Build</h2>
        <p className="mt-1 text-sm text-muted-foreground">Describe the software you want to generate</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 p-6">
        <div className="space-y-2">
          <label htmlFor="prompt" className="block text-sm font-medium">
            Project Description
          </label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe the project you want to build. Include details about features, technology preferences, and any specific requirements..."
            rows={6}
            className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm placeholder-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>

        {error && (
          <div className="rounded-lg border border-destructive/20 bg-destructive/5 p-3 text-sm text-destructive">
            {error.message}
          </div>
        )}

        <div className="flex gap-3">
          <Button type="button" variant="outline" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button type="submit" disabled={loading || !prompt.trim()} className="gap-2">
            {loading ? (
              <>
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                Creating...
              </>
            ) : (
              'Create Build'
            )}
          </Button>
        </div>
      </form>
    </Card>
  );
}
