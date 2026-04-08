import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, AlertTriangle, Shield, Heart, Sparkles, User, LogOut } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE_URL = '/_backend';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [profile, setProfile] = useState({ patterns: [], common_emotions: [] });
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { text: input, type: 'user', timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: input,
        session_id: sessionId
      });

      const { reply, session_id, is_risk, is_early_risk } = response.data;
      
      if (!sessionId) setSessionId(session_id);

      const botMessage = {
        text: reply,
        type: 'bot',
        timestamp: new Date(),
        isRisk: is_risk,
        isEarlyRisk: is_early_risk
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error("Chat Error:", error);
      setMessages(prev => [...prev, { 
        text: "I'm having trouble connecting to my creative center. Please try again in a moment.", 
        type: 'bot', 
        error: true 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <Shield size={24} />
          <span>SoulSync AI</span>
        </div>

        <nav style={{ flex: 1, marginTop: '2rem' }}>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', padding: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
            Your Journey
          </div>
          <div style={{ padding: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem', cursor: 'pointer' }}>
            <Heart size={18} className="profile-tag" />
            <span>Emotional Pulse</span>
          </div>
        </nav>

        <div className="personality-card">
          <h4 style={{ fontSize: '0.9rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Sparkles size={16} color="var(--accent-primary)" />
            Real-time Insights
          </h4>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
            {profile.patterns.length > 0 
              ? `I've noticed some ${profile.patterns.join(', ')} in our conversation.`
              : "I'm currently mirroring your emotional state to provide tailored support."}
          </p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="crisis-banner">
          <AlertTriangle size={18} />
          <span>SoulSync is an AI support companion, not a replacement for professional therapy. If you're in immediate danger, please contact emergency services.</span>
        </header>

        <div className="chat-history">
          <AnimatePresence>
            {messages.length === 0 && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                style={{ textAlign: 'center', padding: '4rem 2rem', color: 'var(--text-secondary)' }}
              >
                <div style={{ display: 'inline-block', padding: '1rem', background: 'rgba(168, 85, 247, 0.05)', borderRadius: '50%', marginBottom: '1.5rem' }}>
                  <Shield size={48} color="var(--accent-primary)" />
                </div>
                <h2>Welcome to SoulSync AI</h2>
                <p style={{ marginTop: '0.5rem' }}>A safe space to explore your thoughts and emotions.</p>
              </motion.div>
            )}

            {messages.map((msg, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`message ${msg.type} ${msg.isRisk || msg.isEarlyRisk ? 'risk-alert' : ''}`}
              >
                {msg.text}
                <div style={{ fontSize: '0.7rem', marginTop: '0.5rem', opacity: 0.6, textAlign: msg.type === 'user' ? 'right' : 'left' }}>
                  {msg.type === 'bot' ? 'Mindful AI' : 'You'}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          
          {isLoading && (
            <div className="message bot">
              <div className="typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <footer className="input-area">
          <form onSubmit={handleSend} className="input-container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="How are you feeling right now?"
              disabled={isLoading}
            />
            <button type="submit" className="send-btn" disabled={!input.trim() || isLoading}>
              <Send size={20} />
            </button>
          </form>
        </footer>
      </main>
    </div>
  );
}

export default App;
