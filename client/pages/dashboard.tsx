import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import { api } from '@/lib/api'

type Txn = { id:number; type:'deposit'|'withdraw'; amount:string; created_at:string }
export default function Dashboard() {
  const [balance, setBalance] = useState<string>('0.00')
  const [txns, setTxns] = useState<Txn[]>([])
  const [amt, setAmt] = useState('')
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const load = async () => {
    try {
      const data = await api('/api/banking/balance/')
      setBalance(data.balance)
      setTxns(data.transactions || [])
    } catch (e: any) {
      setError(e.message)
    }
  }

  useEffect(() => { load() }, [])

  const act = async (path: string) => {
    try {
      setError(null)
      await api(`/api/banking/${path}`, { method: 'POST', body: JSON.stringify({ amount: amt }) })
      setAmt('')
      await load()
    } catch (e: any) {
      setError(e.message)
    }
  }

  return (
    <div className="container space-y-4">
      <div className="card space-y-2">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <div className="space-x-2">
            <a className="underline" href="/admin">Admin</a>
            <button className="btn" onClick={() => { localStorage.removeItem('token'); router.push('/login') }}>Logout</button>
          </div>
        </div>
        {error && <div className="text-red-600">Error: {error}</div>}
        <div>Balance: <span className="font-mono">${balance}</span></div>
        <div className="flex gap-2">
          <input className="input" placeholder="Amount" value={amt} onChange={e=>setAmt(e.target.value)} />
          <button className="btn bg-green-600 text-white" onClick={() => act('deposit')}>Deposit</button>
          <button className="btn bg-red-600 text-white" onClick={() => act('withdraw')}>Withdraw</button>
        </div>
      </div>
      <div className="card">
        <h2 className="text-xl font-semibold mb-2">Transactions</h2>
        <div className="space-y-1">
          {txns.map(t => (
            <div key={t.id} className="flex justify-between border-b py-1 text-sm">
              <span className="uppercase">{t.type}</span>
              <span className="font-mono">${t.amount}</span>
              <span>{new Date(t.created_at).toLocaleString()}</span>
            </div>
          ))}
          {txns.length === 0 && <div className="text-gray-500">No transactions yet.</div>}
        </div>
      </div>
    </div>
  )
}
