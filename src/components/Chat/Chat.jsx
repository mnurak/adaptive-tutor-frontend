import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import api from '../../api/api.js';
import Mermaid from '../Lesson/Mermaid.jsx'; // We can reuse this
import Loader from '../Common/Loader.jsx';
import styles from './Chat.module.css';

const Chat = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hello! What concept would you like to learn about today?" }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { role: 'user', content: inputValue };
    const conversationHistory = [...messages]; // History before the new message

    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await api.post('/api/v1/chat/conversation', {
        prompt: inputValue,
        conversation_history: conversationHistory,
      });

      const assistantMessage = { role: 'assistant', content: response.data.generated_response };
      setMessages(prevMessages => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error("Failed to get response:", error);
      const errorMessage = { role: 'assistant', content: "Sorry, I encountered an error. Please try again." };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messageWindow}>
        {messages.map((msg, index) => (
          <div key={index} className={`${styles.message} ${styles[msg.role]}`}>
            <ReactMarkdown
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '');
                  if (match && match[1] === 'mermaid') {
                    return <div className={styles.mermaidDiagram}><Mermaid chart={String(children)} /></div>;
                  }
                  return <code className={className || 'code-block'} {...props}>{children}</code>;
                },
              }}
            >
              {msg.content}
            </ReactMarkdown>
          </div>
        ))}
        {isLoading && (
          <div className={`${styles.message} ${styles.assistant}`}>
            <span className={styles.typingIndicator}></span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
      <form onSubmit={handleSendMessage} className={styles.inputForm}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask me anything about..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>Send</button>
      </form>
    </div>
  );
};

export default Chat;