import { useState } from 'react';
import { useRouter } from 'next/router';
import { apiClient } from '@/lib/api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const data = await apiClient.post('/api/client/login/', {
        email,
        password,
      });
      localStorage.setItem('jwtToken', data.access); // Save JWT
      router.push('/dashboard');
    } catch (err: any) {
      alert(err.message || 'Login failed');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        type="password"
        placeholder="Password"
      />
      <button type="submit">Login</button>
    </form>
  );
}
