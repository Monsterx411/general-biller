import { useState } from 'react'
const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api'

export default function Personal() {
  const [loanId, setLoanId] = useState('PL-001')
  const [message, setMessage] = useState(null)

  const addLoan = async () => {
    const res = await fetch(`${API}/v1/personal/loans`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ loan_id: loanId, lender_name: 'Lender', amount: 15000, monthly_payment: 300, interest_rate: 12.5, due_date: '12/27' }) })
    setMessage(await res.json())
  }
  const pay = async () => {
    const res = await fetch(`${API}/v1/personal/pay`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ loan_id: loanId, amount: 300 }) })
    setMessage(await res.json())
  }
  return (
    <main style={{ padding: 24 }}>
      <h2>Personal Loan</h2>
      <input value={loanId} onChange={e=>setLoanId(e.target.value)} />
      <button onClick={addLoan}>Add Loan</button>
      <button onClick={pay} style={{ marginLeft: 12 }}>Pay $300</button>
      <pre>{JSON.stringify(message, null, 2)}</pre>
    </main>
  )
}
