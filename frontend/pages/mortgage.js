import { useState } from 'react'
const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api'

export default function Mortgage() {
  const [mid, setMid] = useState('M-001')
  const [message, setMessage] = useState(null)

  const addLoan = async () => {
    const res = await fetch(`${API}/v1/mortgage/loans`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mortgage_id: mid, lender_name: 'Lender', property_address: '123 Main St', principal_balance: 250000, monthly_payment: 1200, interest_rate: 6.0, remaining_term_months: 360, due_date: '12/27' }) })
    setMessage(await res.json())
  }
  const pay = async () => {
    const res = await fetch(`${API}/v1/mortgage/pay`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mortgage_id: mid, amount: 1200 }) })
    setMessage(await res.json())
  }
  return (
    <main style={{ padding: 24 }}>
      <h2>Mortgage</h2>
      <input value={mid} onChange={e=>setMid(e.target.value)} />
      <button onClick={addLoan}>Add Mortgage</button>
      <button onClick={pay} style={{ marginLeft: 12 }}>Pay $1200</button>
      <pre>{JSON.stringify(message, null, 2)}</pre>
    </main>
  )
}
