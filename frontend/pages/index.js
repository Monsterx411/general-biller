import { useEffect, useState } from 'react'

export default function Home() {
  const [health, setHealth] = useState(null)

  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api'
    fetch(base.replace(/\/$/, '').replace(/api$/, '') + 'health')
      .then(res => res.json())
      .then(setHealth)
      .catch(() => setHealth({ status: 'error' }))
  }, [])

  return (
    <main style={{ padding: 24, fontFamily: 'system-ui, sans-serif' }}>
      <h1>Loan Manager</h1>
      <p>Web frontend connected to Flask API.</p>
      <pre>{JSON.stringify(health, null, 2)}</pre>
      <nav style={{ marginTop: 24 }}>
        <a href="/credit-card" style={{ marginRight: 12 }}>Credit Card</a>
        <a href="/personal" style={{ marginRight: 12 }}>Personal</a>
        <a href="/mortgage" style={{ marginRight: 12 }}>Mortgage</a>
        <a href="/auto" style={{ marginRight: 12 }}>Auto</a>
      </nav>
    </main>
  )
}
