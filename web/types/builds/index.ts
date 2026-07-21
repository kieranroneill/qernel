// Build and Planning Types
export type BuildStage = 'initiated' | 'plan' | 'validate' | 'ready';

export interface BuildSummary {
  id: string;
  title: string;
  prompt: string;
  stage: BuildStage;
  createdAt: string;
  updatedAt: string;
}

export interface Build extends BuildSummary {
  plan?: Plan;
  followUpQuestions?: FollowUpQuestion[];
  timeline: TimelineEvent[];
  status: 'processing' | 'completed' | 'error';
}

// API Request/Response Types
export interface ResolveRequest {
  prompt: string;
}

export interface ResolveResponse {
  id: string;
  plan: Plan;
  questions: FollowUpQuestion[];
  stage: BuildStage;
  status: 'processing' | 'completed' | 'error';
}

// Follow-up Questions
export type QuestionType = 'text' | 'textarea' | 'select' | 'multiselect' | 'toggle';

export interface QuestionOption {
  label: string;
  value: string;
}

export interface FollowUpQuestion {
  id: string;
  question: string;
  description?: string;
  type: QuestionType;
  required?: boolean;
  options?: QuestionOption[];
  placeholder?: string;
}

export interface FollowUpAnswers {
  [questionId: string]: string | string[] | boolean;
}

// Plan Types
export interface PlanStep {
  id: string;
  title: string;
  description: string;
  order: number;
}

export interface Plan {
  id: string;
  title: string;
  description: string;
  steps: PlanStep[];
  confirmed: boolean;
  confirmedAt?: string;
}

// Timeline Events
export type TimelineEventType =
  'prompt_received' | 'plan_generated' | 'validation_started' | 'validation_complete' | 'ready' | 'error';

export interface TimelineEvent {
  id: string;
  type: TimelineEventType;
  stage: BuildStage;
  timestamp: string;
  message: string;
  data?: Record<string, any>;
}

// API Error Type
export interface ApiError {
  message: string;
  code?: string;
  details?: Record<string, any>;
}

// Build Context
export interface BuildsContextType {
  builds: BuildSummary[];
  currentBuild: Build | null;
  loading: boolean;
  error: ApiError | null;
  fetchBuilds: () => Promise<void>;
  fetchBuild: (id: string) => Promise<void>;
  createBuild: (prompt: string) => Promise<Build>;
  updateBuild: (id: string, data: Partial<Build>) => Promise<void>;
}
