// client/lib/api.ts
export const api = {
  async get(path: string, token?: string) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}${path}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) throw new Error(`GET ${path} failed`);
    return res.json();
  },

  async post(path: string, body: any, token?: string) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`POST ${path} failed`);
    return res.json();
  },
};
