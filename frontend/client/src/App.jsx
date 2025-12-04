import React, { useState } from 'react'
import Upload from './components/Upload'
import Chat from './components/Chat'

export default function App() {
  const [activeTab, setActiveTab] = useState('upload')

  return (
    <div className="app-wrapper">
      <nav className="glass-panel" style={{
        margin: '2rem auto',
        padding: '1rem',
        maxWidth: '600px',
        display: 'flex',
        justifyContent: 'center',
        gap: '1rem'
      }}>
        <button 
          className={`btn ${activeTab === 'upload' ? 'btn-primary' : ''}`}
          onClick={() => setActiveTab('upload')}
          style={{ color: activeTab === 'upload' ? 'white' : 'var(--text-secondary)' }}
        >
          Upload Documents
        </button>
        <button 
          className={`btn ${activeTab === 'chat' ? 'btn-primary' : ''}`}
          onClick={() => setActiveTab('chat')}
          style={{ color: activeTab === 'chat' ? 'white' : 'var(--text-secondary)' }}
        >
          AI Chat
        </button>
      </nav>

      <main className="container animate-fade-in">
        {activeTab === 'upload' ? <Upload /> : <Chat />}
      </main>
    </div>
  )
}
