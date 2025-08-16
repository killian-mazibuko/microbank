// client/pages/admin.tsx
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

type Client = {
  id: string;
  email: string;
  name: string;
  is_admin: boolean;
  is_blacklisted: boolean;
};

export default function Admin() {
  const [clients, setClients] = useState<Client[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function fetchClients() {
    try {
      const token = localStorage.getItem('token') || '';
      const data = await api.get('/api/client/admin/clients/', token);
      setClients(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load clients');
    }
  }

  async function toggleBlacklist(id: string) {
    try {
      const token = localStorage.getItem('token') || '';
      await api.post(`/api/client/admin/clients/${id}/blacklist/`, {}, token);
      await fetchClients();
    } catch (err: any) {
      setError(err.message || 'Failed to toggle blacklist');
    }
  }

  useEffect(() => {
    fetchClients();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Admin Panel</h1>

      {error && <p className="text-red-600 mb-3">{error}</p>}

      <table className="min-w-full border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="px-3 py-2 border">Email</th>
            <th className="px-3 py-2 border">Name</th>
            <th className="px-3 py-2 border">Blacklisted</th>
            <th className="px-3 py-2 border">Action</th>
          </tr>
        </thead>
        <tbody>
          {clients.map((c) => (
            <tr key={c.id}>
              <td className="px-3 py-2 border">{c.email}</td>
              <td className="px-3 py-2 border">{c.name}</td>
              <td className="px-3 py-2 border">
                {c.is_blacklisted ? 'Yes' : 'No'}
              </td>
              <td className="px-3 py-2 border">
                <button
                  onClick={() => toggleBlacklist(c.id)}
                  className="px-3 py-1 rounded bg-blue-500 text-white hover:bg-blue-600"
                >
                  {c.is_blacklisted ? 'Unblacklist' : 'Blacklist'}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
