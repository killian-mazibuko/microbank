// client/pages/dashboard.tsx
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

type Transaction = {
  id: string;
  type: 'deposit' | 'withdraw';
  amount: number;
  created_at: string;
};

export default function Dashboard() {
  const [balance, setBalance] = useState<number>(0);
  const [txns, setTxns] = useState<Transaction[]>([]);
  const [amount, setAmount] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  const token =
    typeof window !== 'undefined' ? localStorage.getItem('token') || '' : '';

  async function load() {
    try {
      const data = await api.get('/api/banking/balance/', token);
      setBalance(data.balance);
      setTxns(data.transactions || []);
    } catch (e: any) {
      setError(e.message || 'Failed to load balance');
    }
  }

  async function handleDeposit() {
    try {
      await api.post('/api/banking/deposit/', { amount }, token);
      setAmount(0);
      await load();
    } catch (e: any) {
      setError(e.message || 'Deposit failed');
    }
  }

  async function handleWithdraw() {
    try {
      await api.post('/api/banking/withdraw/', { amount }, token);
      setAmount(0);
      await load();
    } catch (e: any) {
      setError(e.message || 'Withdrawal failed');
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Dashboard</h1>

      {error && <p className="text-red-600 mb-3">{error}</p>}

      <p className="mb-4">
        Balance: <strong>${balance.toFixed(2)}</strong>
      </p>

      <div className="flex mb-4">
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(Number(e.target.value))}
          className="border p-2 rounded mr-2"
          placeholder="Amount"
        />
        <button
          onClick={handleDeposit}
          className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 mr-2"
        >
          Deposit
        </button>
        <button
          onClick={handleWithdraw}
          className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
        >
          Withdraw
        </button>
      </div>

      <h2 className="text-lg font-bold mb-2">Transactions</h2>
      <table className="min-w-full border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="px-3 py-2 border">Type</th>
            <th className="px-3 py-2 border">Amount</th>
            <th className="px-3 py-2 border">Date</th>
          </tr>
        </thead>
        <tbody>
          {txns.map((t) => (
            <tr key={t.id}>
              <td className="px-3 py-2 border">{t.type}</td>
              <td className="px-3 py-2 border">${t.amount.toFixed(2)}</td>
              <td className="px-3 py-2 border">
                {new Date(t.created_at).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
