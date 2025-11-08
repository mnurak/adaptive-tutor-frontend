import { useState, useEffect, useRef } from 'react';
import api from '../api/api';

export const useSessionTracking = (sessionType = 'chat') => {
  const [sessionId, setSessionId] = useState(null);
  const sessionStartTime = useRef(null);
  const interactionsCount = useRef(0);
  const conceptsCovered = useRef(new Set());

  useEffect(() => {
    startSession();
    return () => {
      if (sessionId) {
        endSession();
      }
    };
  }, []);

  const startSession = async () => {
    try {
      const response = await api.post('/api/v1/sessions/start', {
        session_type: sessionType,
        device_type: getDeviceType()
      });
      setSessionId(response.data.id);
      sessionStartTime.current = new Date();
    } catch (error) {
      console.error('Failed to start session:', error);
    }
  };

  const endSession = async () => {
    if (!sessionId) return;

    try {
      const duration = (new Date() - sessionStartTime.current) / 1000;
      await api.post(`/api/v1/sessions/${sessionId}/end`, {
        completion_rate: calculateCompletionRate(),
        focus_score: calculateFocusScore(),
        concepts_covered: Array.from(conceptsCovered.current),
        frustration_indicators: 0
      });
    } catch (error) {
      console.error('Failed to end session:', error);
    }
  };

  const trackResourceInteraction = async (resourceData) => {
    if (!sessionId) return;

    try {
      await api.post(`/api/v1/sessions/${sessionId}/interactions`, resourceData);
      interactionsCount.current += 1;
    } catch (error) {
      console.error('Failed to track interaction:', error);
    }
  };

  const addConceptCovered = (conceptName) => {
    conceptsCovered.current.add(conceptName);
  };

  const getDeviceType = () => {
    const width = window.innerWidth;
    if (width < 768) return 'mobile';
    if (width < 1024) return 'tablet';
    return 'desktop';
  };

  const calculateCompletionRate = () => {
    // Simple heuristic: if user has interactions, assume some completion
    return interactionsCount.current > 0 ? 0.8 : 0.5;
  };

  const calculateFocusScore = () => {
    // Simple heuristic based on session duration
    const duration = (new Date() - sessionStartTime.current) / 1000;
    if (duration < 60) return 0.5; // Less than 1 minute
    if (duration < 300) return 0.7; // Less than 5 minutes
    return 0.85; // 5+ minutes
  };

  return {
    sessionId,
    trackResourceInteraction,
    addConceptCovered
  };
};

