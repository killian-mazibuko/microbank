export const API_BASE = {
  CLIENT_SERVICE:
    process.env.NEXT_PUBLIC_CLIENT_SERVICE_URL || 'http://localhost:8000',
  BANKING_SERVICE:
    process.env.NEXT_PUBLIC_BANKING_SERVICE_URL || 'http://localhost:8001',
};

// Generic GET/POST wrapper
async function request(path: string, options: RequestInit = {}) {
  const res = await fetch(path, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// Client service API
export const apiClient = {
  get: (path: string, token?: string) =>
    request(`${API_BASE.CLIENT_SERVICE}${path}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    }),
  post: (path: string, body: any, token?: string) =>
    request(`${API_BASE.CLIENT_SERVICE}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    }),
};

// Banking service API
export const apiBanking = {
  get: (path: string, token?: string) =>
    request(`${API_BASE.BANKING_SERVICE}${path}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    }),
  post: (path: string, body: any, token?: string) =>
    request(`${API_BASE.BANKING_SERVICE}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    }),
};
