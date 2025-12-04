import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'

export default function Chat() {
  const [q, setQ] = useState('')
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [history, loading])

  async function ask(e) {
    e.preventDefault()
    if (!q.trim()) return

    const userMsg = { role: 'user', content: q }
    setHistory(prev => [...prev, userMsg])
    setLoading(true)
    const currentQ = q
    setQ('')

    try {
      const res = await axios.post('http://localhost:8000/query/', { query: currentQ })
      const aiMsg = { role: 'ai', content: res.data.answer }
      setHistory(prev => [...prev, aiMsg])
    } catch (err) {
      const errorMsg = { role: 'ai', content: 'Error: ' + (err?.response?.data?.detail || err.message) }
      setHistory(prev => [...prev, errorMsg])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="glass-panel" style={{
      maxWidth: '800px',
      margin: '0 auto',
      height: '600px',
      display: 'flex',
      flexDirection: 'column'
    }}>
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '1.5rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem'
      }}>
        {history.length === 0 && (
          <div style={{
            textAlign: 'center',
            color: 'var(--text-secondary)',
            marginTop: '2rem'
          }}>
            <h3>👋 Welcome to AI Chat</h3>
            <p>Ask questions about your uploaded documents.</p>
          </div>
        )}

        {history.map((msg, i) => (
          <div key={i} style={{
            alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
            maxWidth: '80%',
            padding: '1rem',
            borderRadius: 'var(--radius-md)',
            backgroundColor: msg.role === 'user' ? 'var(--accent-primary)' : 'var(--bg-secondary)',
            color: 'var(--text-primary)',
            boxShadow: 'var(--shadow-sm)',
            borderBottomRightRadius: msg.role === 'user' ? 0 : 'var(--radius-md)',
            borderBottomLeftRadius: msg.role === 'ai' ? 0 : 'var(--radius-md)'
          }}>
            {msg.content}
          </div>
        ))}

        {loading && (
          <div style={{
            alignSelf: 'flex-start',
            padding: '1rem',
            borderRadius: 'var(--radius-md)',
            backgroundColor: 'var(--bg-secondary)',
            color: 'var(--text-secondary)',
            fontStyle: 'italic'
          }}>
            Thinking...
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div style={{
        padding: '1.5rem',
        borderTop: 'var(--glass-border)',
        backgroundColor: 'rgba(0,0,0,0.1)'
      }}>
        <form onSubmit={ask} style={{ display: 'flex', gap: '0.5rem' }}>
          <input
            className="input-field"
            value={q}
            onChange={e => setQ(e.target.value)}
            placeholder="Ask a question..."
            disabled={loading}
          />
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !q.trim()}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  )
}
