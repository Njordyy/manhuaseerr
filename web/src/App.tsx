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

  async function doSearch() {
    if (q.trim().length < 2) return
    const r = await fetch(`${API}/api/search?q=${encodeURIComponent(q)}&source=all`, {
      headers: { 'x-api-key': apiKey }
    })
    const data = await r.json()
    setResults(data)
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
    <div style={{ padding: 20, minHeight: '100vh' }}>
      <h1 style={{ fontSize: 28, fontWeight: 800 }}>Manhuaseerr</h1>
      <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
        <input value={apiKey} onChange={e=>setApiKey(e.target.value)} placeholder="API Key" style={{ width: 200, padding: 8, borderRadius: 8 }}/>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && doSearch()}
          placeholder="Search Comick..."
          style={{ flex: 1, padding: 10, borderRadius: 8, border: '1px solid #334155', background: '#0b1220', color: 'white' }}
        />
        <button onClick={doSearch} style={{ padding: '10px 16px', borderRadius: 8, background: '#4f46e5', color: 'white', border: 'none' }}>Search</button>
      </div>

      {results.length > 0 && (
        <>
          <h2 style={{ marginTop: 24, fontSize: 22, fontWeight: 700 }}>Search Results</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 16, marginTop: 8 }}>
            {results.map((s) => (
              <div key={`${s.source}-${s.id}`} style={{ background: '#111827', borderRadius: 12, overflow: 'hidden', border: '1px solid #374151' }}>
                <img src={s.cover || 'https://placehold.co/300x450'} style={{ width: '100%', height: 260, objectFit: 'cover' }} />
                <div style={{ padding: 12 }}>
                  <div style={{ fontWeight: 700 }}>{s.title}</div>
                  <div style={{ opacity: 0.7, fontSize: 12 }}>{s.source}</div>
                  <button onClick={() => addFollow(s)} style={{ marginTop: 8, width: '100%', padding: '8px 10px', borderRadius: 8, background: '#16a34a', color: 'white', border: 'none' }}>Follow</button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      <h2 style={{ marginTop: 24, fontSize: 22, fontWeight: 700 }}>Following</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 16, marginTop: 8 }}>
        {following.map((s) => (
          <div key={`${s.source}-${s.id}`} style={{ background: '#111827', borderRadius: 12, overflow: 'hidden', border: '1px solid #374151' }}>
            <img src={s.cover || 'https://placehold.co/300x450'} style={{ width: '100%', height: 260, objectFit: 'cover' }} />
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
