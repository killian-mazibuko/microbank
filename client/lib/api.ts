// Base URLs for services
export const API_BASE_CLIENT = 'http://localhost:8000';
export const API_BASE_BANKING = 'http://localhost:8001';

// Retrieve JWT from localStorage
export const getToken = () => localStorage.getItem('jwtToken');

// Client Service API
export const apiClient = {
  get: async (path: string) => {
    const token = getToken();
    const res = await fetch(`${API_BASE_CLIENT}${path}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    });
    if (!res.ok) throw new Error('Client API request failed');
    return res.json();
  },
  post: async (path: string, body: any) => {
    const token = getToken();
    const res = await fetch(`${API_BASE_CLIENT}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error('Client API request failed');
    return res.json();
  },
};

// Banking Service API
export const apiBanking = {
  get: async (path: string) => {
    const token = getToken();
    const res = await fetch(`${API_BASE_BANKING}${path}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    });
    if (!res.ok) throw new Error('Banking API request failed');
    return res.json();
  },
  post: async (path: string, body: any) => {
    const token = getToken();
    const res = await fetch(`${API_BASE_BANKING}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error('Banking API request failed');
    return res.json();
  },
};
