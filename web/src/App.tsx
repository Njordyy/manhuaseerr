import React, { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

type Series = {
  id: string
  title: string
  cover?: string
  source: string
}

export default function App() {
  const [q, setQ] = useState('')
  const [apiKey, setApiKey] = useState('changeme')
  const [results, setResults] = useState<Series[]>([])
  const [following, setFollowing] = useState<Series[]>([])
  const [error, setError] = useState<string | null>(null)

  async function doSearch() {
    setError(null)
    if (q.trim().length < 2) return
    try {
      const r = await fetch(`${API}/api/search?q=${encodeURIComponent(q)}&source=all`, {
        headers: { 'x-api-key': apiKey }
      })
      if (!r.ok) throw new Error('Search failed')
      const data = await r.json()
      setResults(data)
    } catch (e: any) {
      setError(e.message)
    }
  }

  async function addFollow(s: Series) {
    await fetch(`${API}/api/follow`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': apiKey },
      body: JSON.stringify({ id: s.id, title: s.title, cover: s.cover, source: s.source })
    })
    loadFollowing()
  }

  async function loadFollowing() {
    const r = await fetch(`${API}/api/following`, { headers: { 'x-api-key': apiKey } })
    setFollowing(await r.json())
  }

  useEffect(() => { loadFollowing() }, [])

  return (
    <div className="app">
      <header>Manhuaseerr</header>
      <div className="search">
        <input value={apiKey} onChange={e => setApiKey(e.target.value)} placeholder="API Key" className="input" style={{ width: 200 }} />
        <input
          value={q}
          onChange={e => setQ(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && doSearch()}
          placeholder="Search Comick..."
          className="input"
        />
        <button onClick={doSearch} className="button">Search</button>
      </div>
      {error && <div className="error">{error}</div>}

      {results.length > 0 && (
        <>
          <h2 style={{ marginTop: 24, fontSize: 22, fontWeight: 700 }}>Search Results</h2>
          <div className="grid">
            {results.map((s) => (
              <div key={`${s.source}-${s.id}`} className="card">
                <img src={s.cover || 'https://placehold.co/300x450'} />
                <div style={{ padding: 12 }}>
                  <div style={{ fontWeight: 700 }}>{s.title}</div>
                  <div style={{ opacity: 0.7, fontSize: 12 }}>{s.source}</div>
                  <button onClick={() => addFollow(s)} className="follow-btn">Follow</button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      <h2 style={{ marginTop: 24, fontSize: 22, fontWeight: 700 }}>Following</h2>
      <div className="grid">
        {following.map((s) => (
          <div key={`${s.source}-${s.id}`} className="card">
            <img src={s.cover || 'https://placehold.co/300x450'} />
            <div style={{ padding: 12 }}>
              <div style={{ fontWeight: 700 }}>{s.title}</div>
              <div style={{ opacity: 0.7, fontSize: 12 }}>{s.source}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
