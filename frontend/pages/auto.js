import { useState } from 'react'
const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api'

export default function Auto() {
  const [loanId, setLoanId] = useState('AL-001')
  const [message, setMessage] = useState(null)

  const addLoan = async () => {
    const res = await fetch(`${API}/v1/auto/loans`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ loan_id: loanId, lender_name: 'Lender', vehicle_make: 'Toyota', vehicle_model: 'Camry', vehicle_year: 2020, vin: 'VIN123', loan_amount: 25000, monthly_payment: 350, interest_rate: 5.0, months_remaining: 60, due_date: '12/27' }) })
    setMessage(await res.json())
  }
  const pay = async () => {
    const res = await fetch(`${API}/v1/auto/pay`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ loan_id: loanId, amount: 350 }) })
    setMessage(await res.json())
  }
  return (
    <main style={{ padding: 24 }}>
      <h2>Auto Loan</h2>
      <input value={loanId} onChange={e=>setLoanId(e.target.value)} />
      <button onClick={addLoan}>Add Auto Loan</button>
      <button onClick={pay} style={{ marginLeft: 12 }}>Pay $350</button>
      <pre>{JSON.stringify(message, null, 2)}</pre>
    </main>
  )
}
