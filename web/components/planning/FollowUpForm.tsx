'use client';

import React, { useState } from 'react';
import { FollowUpRenderer } from '@/components/planning/FollowUpRenderer';
import type { FollowUpQuestion, FollowUpAnswers } from '@/types';
import { Card } from '@/components/ui/card';

// components
import Button from '@/components/ui/Button';

interface FollowUpFormProps {
  questions: FollowUpQuestion[];
  onSubmit: (answers: FollowUpAnswers) => Promise<void>;
  isLoading?: boolean;
}

export function FollowUpForm({ questions, onSubmit, isLoading = false }: FollowUpFormProps) {
  const [answers, setAnswers] = useState<FollowUpAnswers>({});
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (questionId: string, value: string | string[] | boolean) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate required fields
    for (const question of questions) {
      if (question.required && !answers[question.id]) {
        setError(`${question.question} is required`);
        return;
      }
    }

    try {
      setSubmitting(true);
      setError(null);
      await onSubmit(answers);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit answers');
    } finally {
      setSubmitting(false);
    }
  };

  if (questions.length === 0) {
    return (
      <Card>
        <div className="p-6 text-center text-sm text-muted-foreground">No follow-up questions at this time</div>
      </Card>
    );
  }

  return (
    <Card>
      <form onSubmit={handleSubmit} className="space-y-6 p-6">
        <div>
          <h3 className="text-lg font-medium">Review & Answer Questions</h3>
          <p className="mt-1 text-sm text-muted-foreground">Help us refine the plan by answering these questions</p>
        </div>

        {/* Questions */}
        <div className="space-y-6 border-t border-border pt-6">
          {questions.map((question) => (
            <FollowUpRenderer
              key={question.id}
              question={question}
              value={answers[question.id]}
              onChange={(value) => handleChange(question.id, value)}
              disabled={isLoading || submitting}
            />
          ))}
        </div>

        {/* Error Message */}
        {error && (
          <div className="rounded-lg border border-destructive/20 bg-destructive/5 p-3 text-sm text-destructive">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end gap-3 border-t border-border pt-6">
          <Button type="submit" disabled={isLoading || submitting} className="gap-2">
            {submitting ? (
              <>
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                Submitting...
              </>
            ) : (
              'Continue'
            )}
          </Button>
        </div>
      </form>
    </Card>
  );
}
