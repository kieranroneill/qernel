export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3001/api';

export const API_ENDPOINTS = {
  AUTH: {
    START: `${API_BASE_URL}/auth/github/start`,
    COMPLETE: `${API_BASE_URL}/auth/github/complete`,
    LOGOUT: `${API_BASE_URL}/auth/logout`,
    ME: `${API_BASE_URL}/auth/me`,
  },
  BUILDS: {
    LIST: `${API_BASE_URL}/builds`,
    CREATE: `${API_BASE_URL}/builds`,
    GET: (id: string) => `${API_BASE_URL}/builds/${id}`,
    RESOLVE: (id: string) => `${API_BASE_URL}/builds/${id}/resolve`,
    SUBMIT_ANSWERS: (id: string) => `${API_BASE_URL}/builds/${id}/answers`,
    CONFIRM_PLAN: (id: string) => `${API_BASE_URL}/builds/${id}/confirm`,
  },
};
