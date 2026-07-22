'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '@/components/ui/card';
import { StageTimeline } from '@/components/planning/StageTimeline';
import { FollowUpForm } from '@/components/planning/FollowUpForm';
import { PlanSummaryCard } from '@/components/planning/PlanSummaryCard';
import { StageBadge } from '@/components/planning/StageBadge';
import { apiService } from '@/services/api';
import type { Build, FollowUpAnswers, FollowUpQuestion } from '@/types';
import { ChevronLeft, AlertCircle } from 'lucide-react';
import Link from 'next/link';

// components
import Button from '@/components/ui/Button';

interface BuildWorkspaceProps {
  buildId: string;
}

export function BuildWorkspace({ buildId }: BuildWorkspaceProps) {
  const [build, setBuild] = useState<Build | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submittingAnswers, setSubmittingAnswers] = useState(false);
  const [confirmingPlan, setConfirmingPlan] = useState(false);

  useEffect(() => {
    fetchBuild();
  }, [buildId]);

  async function fetchBuild() {
    try {
      setLoading(true);
      const { data, error } = await apiService.getBuild(buildId);

      if (error) {
        setError(error.message);
      } else if (data) {
        setBuild(data);
        setError(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch build');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmitAnswers(answers: FollowUpAnswers) {
    try {
      setSubmittingAnswers(true);
      const { data, error } = await apiService.submitFollowUpAnswers(buildId, answers);

      if (error) {
        throw new Error(error.message);
      }

      if (data) {
        setBuild(data);
      }
    } finally {
      setSubmittingAnswers(false);
    }
  }

  async function handleConfirmPlan() {
    try {
      setConfirmingPlan(true);
      const { data, error } = await apiService.confirmPlan(buildId);

      if (error) {
        throw new Error(error.message);
      }

      if (data) {
        setBuild(data);
      }
    } finally {
      setConfirmingPlan(false);
    }
  }

  if (loading) {
    return (
      <div className="space-y-4 p-6 md:p-8">
        <div className="h-12 rounded-lg bg-muted animate-pulse" />
        <div className="h-48 rounded-lg bg-muted animate-pulse" />
        <div className="h-64 rounded-lg bg-muted animate-pulse" />
      </div>
    );
  }

  if (error || !build) {
    return (
      <div className="p-6 md:p-8">
        <div className="flex gap-4 rounded-lg border border-destructive/20 bg-destructive/5 p-6">
          <AlertCircle className="h-5 w-5 text-destructive flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-destructive">Error Loading Build</h3>
            <p className="mt-1 text-sm text-destructive/80">{error || 'Build not found'}</p>
            <Link href="/dashboard">
              <Button variant="outline" size="sm" className="mt-4">
                Back to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6 md:p-8">
      {/* Back Button */}
      <Link
        href="/dashboard"
        className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
      >
        <ChevronLeft size={16} />
        Back to Builds
      </Link>

      {/* Header */}
      <div className="space-y-4">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-light tracking-tight">{build.title || 'Untitled Build'}</h1>
            <p className="mt-2 text-muted-foreground">{build.prompt}</p>
          </div>
          <StageBadge stage={build.stage} size="md" />
        </div>

        {/* Timeline */}
        <Card className="p-6">
          <StageTimeline currentStage={build.stage} events={build.timeline} />
        </Card>
      </div>

      {/* Content based on Stage */}
      <div className="space-y-4">
        {build.stage === 'initiated' && (
          <Card className="p-6 text-center">
            <div className="flex justify-center mb-4">
              <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
            </div>
            <p className="text-sm text-muted-foreground">Processing your project request...</p>
          </Card>
        )}

        {build.stage === 'plan' && build.followUpQuestions && build.followUpQuestions.length > 0 && (
          <FollowUpForm
            questions={build.followUpQuestions}
            onSubmit={handleSubmitAnswers}
            isLoading={submittingAnswers}
          />
        )}

        {(build.stage === 'plan' || build.stage === 'validate' || build.stage === 'ready') && build.plan && (
          <PlanSummaryCard
            plan={build.plan}
            onConfirm={handleConfirmPlan}
            isConfirming={confirmingPlan}
            isConfirmed={build.plan.confirmed}
          />
        )}

        {build.stage === 'ready' && (
          <Card className="border-green-200 bg-green-50 dark:border-green-900 dark:bg-green-950 p-6">
            <h3 className="font-medium text-green-900 dark:text-green-100">Build Ready</h3>
            <p className="mt-2 text-sm text-green-800 dark:text-green-200">
              Your project is ready for generation. The generation process will begin shortly.
            </p>
          </Card>
        )}
      </div>

      {/* Error Status */}
      {build.status === 'error' && (
        <Card className="border-destructive/20 bg-destructive/5 p-6">
          <p className="text-sm text-destructive">An error occurred during processing</p>
          <Button onClick={fetchBuild} variant="outline" size="sm" className="mt-4">
            Retry
          </Button>
        </Card>
      )}
    </div>
  );
}
