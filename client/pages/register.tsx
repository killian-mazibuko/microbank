import { useState } from 'react';
import { useRouter } from 'next/router';
import { apiClient } from '@/lib/api';

export default function Register() {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.post('/api/client/register/', { email, name, password });
      alert('Registration successful! Please login.');
      router.push('/login');
    } catch (err: any) {
      alert(err.message || 'Registration failed');
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
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
      <button type="submit">Register</button>
    </form>
  );
}
