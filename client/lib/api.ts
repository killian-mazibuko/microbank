// Define base URLs for your services
export const API_BASE = {
  CLIENT_SERVICE:
    process.env.NEXT_PUBLIC_CLIENT_SERVICE_URL || 'http://localhost:8000',
  BANKING_SERVICE:
    process.env.NEXT_PUBLIC_BANKING_SERVICE_URL || 'http://localhost:8001',
};

// Generic API wrapper
export const api = {
  async get(path: string, token?: string) {
    const res = await fetch(path, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async post(path: string, body: any, token?: string) {
    const res = await fetch(path, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
};
