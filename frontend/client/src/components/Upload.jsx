import React, { useState } from 'react'
import axios from 'axios'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('')
  const [isUploading, setIsUploading] = useState(false)

  async function doUpload(e) {
    e.preventDefault()
    if (!file) return

    const fd = new FormData()
    fd.append('file', file)

    setStatus('Uploading...')
    setIsUploading(true)

    try {
      const res = await axios.post('http://localhost:8000/upload/', fd, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setStatus('Success! Document ready for querying.')
      setFile(null)
    } catch (err) {
      setStatus('Error: ' + (err?.response?.data?.detail || err.message))
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="glass-panel" style={{ maxWidth: '600px', margin: '0 auto', padding: '2rem' }}>
      <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Upload Knowledge Base</h2>

      <form onSubmit={doUpload} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div style={{
          border: '2px dashed var(--border-color)',
          borderRadius: 'var(--radius-lg)',
          padding: '3rem',
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.2s',
          backgroundColor: 'rgba(255,255,255,0.02)'
        }}
          onClick={() => document.getElementById('file-input').click()}
        >
          <input
            id="file-input"
            type="file"
            onChange={e => setFile(e.target.files[0])}
            style={{ display: 'none' }}
          />
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📄</div>
          {file ? (
            <div style={{ color: 'var(--accent-primary)', fontWeight: 'bold' }}>
              {file.name}
            </div>
          ) : (
            <div style={{ color: 'var(--text-secondary)' }}>
              Click to select a PDF or Text file
            </div>
          )}
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={!file || isUploading}
          style={{ width: '100%' }}
        >
          {isUploading ? 'Processing...' : 'Upload Document'}
        </button>
      </form>

      {status && (
        <div style={{
          marginTop: '1.5rem',
          padding: '1rem',
          borderRadius: 'var(--radius-md)',
          backgroundColor: status.includes('Error') ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)',
          color: status.includes('Error') ? 'var(--error)' : 'var(--success)',
          textAlign: 'center'
        }}>
          {status}
        </div>
      )}
    </div>
  )
}
