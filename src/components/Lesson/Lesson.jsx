import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import api from '../../api/api.js';
import Mermaid from './Mermaid.jsx';
import Loader from '../Common/Loader.jsx';
import styles from './Lesson.module.css';

const Lesson = () => {
  const [concept, setConcept] = useState('');
  const [lessonContent, setLessonContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerateLesson = async (e) => {
    e.preventDefault();
    if (!concept.trim()) return;

    setLoading(true);
    setError('');
    setLessonContent('');

    try {
      // THIS IS THE FIX: The concept name is now correctly placed in the URL path,
      // and the request body is empty as per the backend's expectation.
      const response = await api.post(`/api/v1/instruction/${concept}/generate`, {});
      
      setLessonContent(response.data.generated_instruction);
    } catch (err) {
      const errorDetail = err.response?.data?.detail || `Failed to generate lesson for "${concept}".`;
      setError(errorDetail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.lessonContainer}>
      <h2>Structured Lesson Generator</h2>
      <p>Enter a topic to get a complete, structured lesson based on your current learning profile.</p>
      
      <form onSubmit={handleGenerateLesson} className={styles.form}>
        <input
          type="text"
          value={concept}
          onChange={(e) => setConcept(e.target.value)}
          placeholder="e.g., Arrays, Recursion"
          required
        />
        <button type="submit" disabled={loading || !concept.trim()}>
          Generate Lesson
        </button>
      </form>

      {loading && (
        <div className={styles.loadingContainer}>
            <Loader />
            <p>Generating your lesson on "{concept}"...</p>
        </div>
      )}
      
      {error && <p className={styles.error}>{error}</p>}
      
      {lessonContent && (
        <div className={styles.lessonContent}>
          <h3>Lesson on: {concept}</h3>
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
            {lessonContent}
          </ReactMarkdown>
        </div>
      )}
    </div>
  );
};

export default Lesson;