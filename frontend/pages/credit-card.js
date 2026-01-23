import { useState } from 'react'

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api'

export default function CreditCard() {
  const [form, setForm] = useState({ card_type: 'Visa', card_suffix: '1234', balance: 5000, minimum_payment: 150, interest_rate: 18.5, due_date: '12/27' })
  const [message, setMessage] = useState(null)

  const addLoan = async () => {
    const res = await fetch(`${API}/v1/credit-card/loans`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
    setMessage(await res.json())
  }

  const pay = async () => {
    const res = await fetch(`${API}/v1/credit-card/pay`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ card_type: form.card_type, card_suffix: form.card_suffix, amount: 100 }) })
    setMessage(await res.json())
  }

  return (
    <main style={{ padding: 24 }}>
      <h2>Credit Card Loan</h2>
      <button onClick={addLoan}>Add Loan</button>
      <button onClick={pay} style={{ marginLeft: 12 }}>Pay $100</button>
      <pre>{JSON.stringify(message, null, 2)}</pre>
    </main>
  )
}
