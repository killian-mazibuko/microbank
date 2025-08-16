import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { apiBanking } from '@/lib/api';

type Transaction = { id: string; type: string; amount: number; date: string };

export default function Dashboard() {
  const router = useRouter();
  const [balance, setBalance] = useState(0);
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  useEffect(() => {
    const token = localStorage.getItem('jwtToken');
    if (!token) router.push('/login');

    const load = async () => {
      try {
        const data = await apiBanking.get('/api/banking/balance/');
        setBalance(data.balance);
        setTransactions(data.transactions || []);
      } catch (e: any) {
        alert(e.message);
      }
    };

    load();
  }, [router]);

  return (
    <div>
      <h1>Balance: ${balance}</h1>
      <h2>Transactions:</h2>
      <ul>
        {transactions.map((t) => (
          <li key={t.id}>
            {t.type} ${t.amount} on {new Date(t.date).toLocaleString()}
          </li>
        ))}
      </ul>
      <button
        onClick={() => {
          localStorage.removeItem('jwtToken');
          router.push('/login');
        }}
      >
        Logout
      </button>
    </div>
  );
}
