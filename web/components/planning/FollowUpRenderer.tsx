import React from 'react';
import type { FollowUpQuestion } from '@/types';

interface FollowUpRendererProps {
  question: FollowUpQuestion;
  value?: string | string[] | boolean;
  onChange: (value: string | string[] | boolean) => void;
  disabled?: boolean;
}

export function FollowUpRenderer({ question, value, onChange, disabled }: FollowUpRendererProps) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium">
        {question.question}
        {question.required && <span className="text-destructive">*</span>}
      </label>

      {question.description && <p className="text-xs text-muted-foreground">{question.description}</p>}

      {question.type === 'text' && (
        <input
          type="text"
          value={(value as string) || ''}
          onChange={(e) => onChange(e.target.value)}
          placeholder={question.placeholder}
          disabled={disabled}
          className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm placeholder-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-50"
        />
      )}

      {question.type === 'textarea' && (
        <textarea
          value={(value as string) || ''}
          onChange={(e) => onChange(e.target.value)}
          placeholder={question.placeholder}
          disabled={disabled}
          rows={4}
          className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm placeholder-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-50"
        />
      )}

      {question.type === 'select' && question.options && (
        <select
          value={(value as string) || ''}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
          className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-50"
        >
          <option value="">Select an option...</option>
          {question.options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      )}

      {question.type === 'multiselect' && question.options && (
        <div className="space-y-2">
          {question.options.map((option) => {
            const values = Array.isArray(value) ? value : [];
            const isSelected = values.includes(option.value);

            return (
              <label key={option.value} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={(e) => {
                    if (e.target.checked) {
                      onChange([...values, option.value]);
                    } else {
                      onChange(values.filter((v) => v !== option.value));
                    }
                  }}
                  disabled={disabled}
                  className="rounded border-input accent-primary disabled:opacity-50"
                />
                <span className="text-sm">{option.label}</span>
              </label>
            );
          })}
        </div>
      )}

      {question.type === 'toggle' && (
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={(value as boolean) || false}
            onChange={(e) => onChange(e.target.checked)}
            disabled={disabled}
            className="rounded border-input accent-primary disabled:opacity-50"
          />
          <span className="text-sm">Yes, I agree</span>
        </label>
      )}
    </div>
  );
}
