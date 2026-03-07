import { useState, useRef, useEffect } from 'react'
import './App.css'

const HIVE_ICON = '\u2b21'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const envoyer = async (e) => {
    e.preventDefault()
    const texte = input.trim()
    if (!texte || loading) return

    setInput('')
    setMessages((prev) => [...prev, { role: 'user', content: texte }])
    setLoading(true)

    try {
      const res = await fetch('/api/reine/parler', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: texte, session_id: sessionId }),
      })
      const data = await res.json()
      if (data.session_id) setSessionId(data.session_id)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.reponse || 'Pas de reponse.',
          signe: data.signe_par,
        },
      ])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Erreur de connexion au serveur.', signe: 'HIVE.WORK' },
      ])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  const nouvelleSession = () => {
    setMessages([])
    setSessionId(null)
    inputRef.current?.focus()
  }

  return (
    <div className="hive-app">
      <header className="hive-header">
        <div className="hive-logo">
          <span className="hive-hex">{HIVE_ICON}</span>
          <h1>HIVE.WORK</h1>
        </div>
        <button className="btn-reset" onClick={nouvelleSession} title="Nouvelle conversation">
          +
        </button>
      </header>

      <main className="hive-chat">
        {messages.length === 0 && (
          <div className="hive-welcome">
            <span className="hive-welcome-hex">{HIVE_ICON}</span>
            <h2>Bienvenue sur HIVE.WORK</h2>
            <p>Posez votre question. Claire, bienveillante, efficace.</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`hive-msg hive-msg-${msg.role}`}>
            {msg.role === 'assistant' && <span className="hive-msg-hex">{HIVE_ICON}</span>}
            <div className="hive-msg-content">
              <div className="hive-msg-text">{msg.content}</div>
              {msg.signe && <span className="hive-msg-signe">{msg.signe}</span>}
            </div>
          </div>
        ))}

        {loading && (
          <div className="hive-msg hive-msg-assistant">
            <span className="hive-msg-hex">{HIVE_ICON}</span>
            <div className="hive-msg-content">
              <div className="hive-typing">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </main>

      <form className="hive-input-bar" onSubmit={envoyer}>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ecrivez votre message..."
          disabled={loading}
          autoComplete="off"
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Envoyer
        </button>
      </form>
    </div>
  )
}

export default App
