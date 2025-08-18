import { useEffect, useState } from 'react';

const CLIENT_API = process.env.CLIENT_SERVICE_URL || 'http://20.63.49.65:8001';
const BANKING_API =
  process.env.BANKING_SERVICE_URL || 'http://20.63.49.65:8002';

export default function Home() {
  const [mode, setMode] = useState('login');
  const [username, setUsername] = useState('alice');
  const [password, setPassword] = useState('pw12345');
  const [email, setEmail] = useState('alice@example.com');
  const [token, setToken] = useState(null);
  const [me, setMe] = useState(null);
  const [balance, setBalance] = useState('0.00');
  const [amount, setAmount] = useState('10.00');
  const [txns, setTxns] = useState([]);
  const [clients, setClients] = useState([]);

  const authHeaders = () => (token ? { Authorization: 'Bearer ' + token } : {});

  async function register() {
    await fetch(`${CLIENT_API}/client/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });
    setMode('login');
  }
  async function login() {
    const r = await fetch(`${CLIENT_API}/client/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const j = await r.json();
    if (!j.token) {
      alert('Login failed: ' + (j.detail || 'Invalid credentials'));
      if (localStorage.getItem('token')) {
        localStorage.removeItem('token'); // Clear token if login fails
      }
      setToken(null);
      setMe(null);
    } else {
      localStorage.setItem('token', j.token);
      console.log('Token: ', j.token);
      setToken(j.token);
    }
  }

  async function fetchMe() {
    const r = await fetch(`${CLIENT_API}/client/me`, {
      headers: authHeaders(),
    });
    const j = await r.json();
    setMe(j);
  }
  async function fetchBalance() {
    const r = await fetch(`${BANKING_API}/banking/balance`, {
      headers: authHeaders(),
    });
    const j = await r.json();
    if (j.detail === 'Blacklisted') alert('You are blacklisted');
    setBalance(j.balance || '0.00');
  }
  async function doDeposit() {
    const r = await fetch(`${BANKING_API}/banking/deposit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify({ amount }),
    });
    const j = await r.json();
    if (j.detail) alert(j.detail);
    setBalance(j.balance || balance);
    loadTxns();
  }
  async function doWithdraw() {
    const r = await fetch(`${BANKING_API}/banking/withdraw`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify({ amount }),
    });
    const j = await r.json();
    if (j.detail) alert(j.detail);
    setBalance(j.balance || balance);
    loadTxns();
  }
  async function loadTxns() {
    const r = await fetch(`${BANKING_API}/banking/transactions`, {
      headers: authHeaders(),
    });
    const j = await r.json();
    setTxns(j.results || []);
  }
  async function loadClients() {
    const r = await fetch(`${CLIENT_API}/client/admin/clients`, {
      headers: authHeaders(),
    });
    const j = await r.json();
    setClients(j.results || []);
  }
  async function toggleBlacklist(id, is_blacklisted) {
    const r = await fetch(`${API}/client/admin/blacklist`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify({ user_id: id, is_blacklisted }),
    });
    await loadClients();
  }

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
    }
    if (token) {
      fetchMe();
      fetchBalance();
      loadTxns();
    }
  }, [token]);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Microbank</h1>

        {!token && (
          <div className="bg-white p-4 rounded-2xl shadow mb-4">
            <div className="flex gap-4 mb-4">
              <button
                className={`px-3 py-1 rounded ${
                  mode === 'login' ? 'bg-black text-white' : ''
                }`}
                onClick={() => setMode('login')}
              >
                Login
              </button>
              <button
                className={`px-3 py-1 rounded ${
                  mode === 'register' ? 'bg-black text-white' : ''
                }`}
                onClick={() => setMode('register')}
              >
                Register
              </button>
            </div>
            <div className="grid gap-2">
              <input
                className="border p-2 rounded"
                placeholder="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              {mode === 'register' && (
                <input
                  className="border p-2 rounded"
                  placeholder="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              )}
              <input
                className="border p-2 rounded"
                type="password"
                placeholder="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              {mode === 'login' ? (
                <button
                  className="bg-blue-600 text-white px-4 py-2 rounded"
                  onClick={login}
                >
                  Login
                </button>
              ) : (
                <button
                  className="bg-green-600 text-white px-4 py-2 rounded"
                  onClick={register}
                >
                  Register
                </button>
              )}
            </div>
          </div>
        )}

        {token && me && (
          <div className="bg-white p-4 rounded-2xl shadow mb-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-semibold">Welcome, {me.username}</div>
                <div className="text-sm text-gray-600">{me.email}</div>
              </div>
              <button
                className="text-red-600"
                onClick={() => {
                  setToken(null);
                  setMe(null);
                  localStorage.removeItem('token');
                }}
              >
                Log out
              </button>
            </div>
          </div>
        )}

        {token && (
          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-2xl shadow">
              <div className="text-xl font-semibold mb-2">Balance</div>
              <div className="text-3xl mb-4">${balance}</div>
              <div className="flex gap-2">
                <input
                  className="border p-2 rounded w-full"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                />
                <button
                  className="bg-green-600 text-white px-4 py-2 rounded"
                  onClick={doDeposit}
                >
                  Deposit
                </button>
                <button
                  className="bg-yellow-600 text-white px-4 py-2 rounded"
                  onClick={doWithdraw}
                >
                  Withdraw
                </button>
              </div>
            </div>

            <div className="bg-white p-4 rounded-2xl shadow">
              <div className="text-xl font-semibold mb-2">Transactions</div>
              <button className="text-sm underline mb-2" onClick={loadTxns}>
                Refresh
              </button>
              <ul className="space-y-2 max-h-64 overflow-auto">
                {txns.map((t) => (
                  <li
                    key={t.id}
                    className="flex justify-between border p-2 rounded"
                  >
                    <span>{t.type}</span>
                    <span>${t.amount}</span>
                    <span className="text-xs text-gray-500">
                      {new Date(t.created_at).toLocaleString()}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {token && me && me.is_staff && (
          <div className="bg-white p-4 rounded-2xl shadow mt-4">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xl font-semibold">Admin Panel</div>
              <button className="text-sm underline" onClick={loadClients}>
                Load Clients
              </button>
            </div>
            <table className="w-full text-left">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>User</th>
                  <th>Email</th>
                  <th>Blacklisted</th>
                  <th>Toggle</th>
                </tr>
              </thead>
              <tbody>
                {clients.map((c) => (
                  <tr key={c.id} className="border-t">
                    <td>{c.id}</td>
                    <td>{c.username}</td>
                    <td>{c.email}</td>
                    <td>{c.is_blacklisted ? 'Yes' : 'No'}</td>
                    <td>
                      <button
                        className="px-2 py-1 rounded bg-gray-200"
                        onClick={() => toggleBlacklist(c.id, !c.is_blacklisted)}
                      >
                        {c.is_blacklisted ? 'Unblacklist' : 'Blacklist'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
