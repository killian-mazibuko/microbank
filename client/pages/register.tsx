import { useState } from 'react'
import { useRouter } from 'next/router'
import { api, API_BASE } from '@/lib/api'

export default function Register() {
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const submit = async (e: any) => {
    e.preventDefault()
    setError(null)
    try {
      await api('/api/client/register/', { method: 'POST', body: JSON.stringify({ email, name, password }) })
      router.push('/login')
    } catch (e: any) {
      setError(e.message)
    }
  }

  return (
    <div className="container">
      <div className="card space-y-4">
        <h1 className="text-2xl font-bold">Register</h1>
        {error && <div className="text-red-600">{error}</div>}
        <form onSubmit={submit} className="space-y-3">
          <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
          <input className="input" placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
          <input type="password" className="input" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
          <button className="btn bg-black text-white" type="submit">Create account</button>
        </form>
        <a className="underline" href="/login">Have an account? Log in</a>
      </div>
    </div>
  )
}
