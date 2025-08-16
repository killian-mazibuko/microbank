import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api';

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

  const loadClients = async () => {
    try {
      const token = localStorage.getItem('token') || '';
      const data = await apiClient.get('/api/clients/', token);
      setClients(data);
    } catch (e: any) {
      setError(e.message);
    }
  };

  const toggleBlacklist = async (id: string, current: boolean) => {
    try {
      const token = localStorage.getItem('token') || '';
      await apiClient.post(
        `/api/clients/${id}/blacklist/`,
        { is_blacklisted: !current },
        token
      );
      await loadClients();
    } catch (e: any) {
      setError(e.message);
    }
  };

  useEffect(() => {
    loadClients();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Admin Panel</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr>
            <th className="border p-2">Email</th>
            <th className="border p-2">Name</th>
            <th className="border p-2">Admin</th>
            <th className="border p-2">Blacklisted</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {clients.map((c) => (
            <tr key={c.id}>
              <td className="border p-2">{c.email}</td>
              <td className="border p-2">{c.name}</td>
              <td className="border p-2">{c.is_admin ? 'Yes' : 'No'}</td>
              <td className="border p-2">{c.is_blacklisted ? 'Yes' : 'No'}</td>
              <td className="border p-2">
                <button
                  className="px-3 py-1 bg-blue-500 text-white rounded"
                  onClick={() => toggleBlacklist(c.id, c.is_blacklisted)}
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
