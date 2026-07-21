import type { User, BuildSummary, Build, FollowUpAnswers, Plan, ApiError } from '@/types';
import { API_ENDPOINTS } from '@/constants/api';

class ApiService {
  private async request<T>(url: string, options?: RequestInit): Promise<{ data?: T; error?: ApiError }> {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        credentials: 'include',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          error: {
            message: errorData.message || 'An error occurred',
            code: errorData.code,
            details: errorData.details,
          },
        };
      }

      const data = await response.json();
      return { data };
    } catch (err) {
      return {
        error: {
          message: err instanceof Error ? err.message : 'Network error',
        },
      };
    }
  }

  // Auth endpoints
  async startGithubAuth(): Promise<{ authorizeUrl?: string; error?: ApiError }> {
    const result = await this.request<{ authorizeUrl: string }>(API_ENDPOINTS.AUTH.START, { method: 'POST' });
    return result;
  }

  async completeGithubAuth(code: string): Promise<{ data?: User; error?: ApiError }> {
    return this.request<User>(API_ENDPOINTS.AUTH.COMPLETE, {
      method: 'POST',
      body: JSON.stringify({ code }),
    });
  }

  async getCurrentUser(): Promise<{ data?: User; error?: ApiError }> {
    return this.request<User>(API_ENDPOINTS.AUTH.ME);
  }

  async logout(): Promise<{ error?: ApiError }> {
    const result = await this.request(API_ENDPOINTS.AUTH.LOGOUT, {
      method: 'POST',
    });
    return { error: result.error };
  }

  // Build endpoints
  async getBuildSessions(): Promise<{ data?: BuildSummary[]; error?: ApiError }> {
    return this.request<BuildSummary[]>(API_ENDPOINTS.BUILDS.LIST);
  }

  async getBuild(id: string): Promise<{ data?: Build; error?: ApiError }> {
    return this.request<Build>(API_ENDPOINTS.BUILDS.GET(id));
  }

  async createBuild(prompt: string): Promise<{ data?: Build; error?: ApiError }> {
    return this.request<Build>(API_ENDPOINTS.BUILDS.CREATE, {
      method: 'POST',
      body: JSON.stringify({ prompt }),
    });
  }

  async resolveBuild(id: string): Promise<{ data?: { plan: Plan; questions: any[] }; error?: ApiError }> {
    return this.request<{ plan: Plan; questions: any[] }>(API_ENDPOINTS.BUILDS.RESOLVE(id), { method: 'POST' });
  }

  async submitFollowUpAnswers(id: string, answers: FollowUpAnswers): Promise<{ data?: Build; error?: ApiError }> {
    return this.request<Build>(API_ENDPOINTS.BUILDS.SUBMIT_ANSWERS(id), {
      method: 'POST',
      body: JSON.stringify(answers),
    });
  }

  async confirmPlan(id: string): Promise<{ data?: Build; error?: ApiError }> {
    return this.request<Build>(API_ENDPOINTS.BUILDS.CONFIRM_PLAN(id), {
      method: 'POST',
    });
  }
}

export const apiService = new ApiService();
