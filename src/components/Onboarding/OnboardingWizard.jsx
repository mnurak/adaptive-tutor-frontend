import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../api/api';
import QuestionCard from './QuestionCard';
import ProgressBar from './ProgressBar';
import GoalsForm from './GoalsForm';
import styles from './OnboardingWizard.module.css';

const OnboardingWizard = () => {
  const [questions, setQuestions] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [responses, setResponses] = useState({});
  const [goals, setGoals] = useState({
    learning_goal: '',
    available_hours_per_week: 5,
    preferred_session_duration: 30
  });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchQuestionnaire();
  }, []);

  const fetchQuestionnaire = async () => {
    try {
      const response = await api.get('/api/v1/onboarding/questionnaire');
      setQuestions(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch questionnaire:', error);
      setError('Failed to load questionnaire. Please try again.');
      setLoading(false);
    }
  };

  const handleAnswer = (questionId, answer) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleNext = () => {
    if (currentStep < questions.length) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError(null);
    
    try {
      const submission = {
        responses: Object.entries(responses).map(([question_id, answer]) => ({
          question_id,
          answer
        })),
        ...goals
      };

      await api.post('/api/v1/onboarding/submit', submission);
      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to submit onboarding:', error);
      setError('Failed to submit. Please try again.');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading questionnaire...</div>
      </div>
    );
  }

  if (error && questions.length === 0) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
        <button onClick={fetchQuestionnaire} className={styles.retryButton}>
          Retry
        </button>
      </div>
    );
  }

  const isLastQuestion = currentStep === questions.length;
  const currentQuestion = questions[currentStep];
  const progress = ((currentStep + 1) / (questions.length + 1)) * 100;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Welcome! Let's personalize your learning experience</h1>
        <p>This will take about 5 minutes</p>
      </div>

      <ProgressBar progress={progress} currentStep={currentStep + 1} totalSteps={questions.length + 1} />
      
      {error && <div className={styles.error}>{error}</div>}

      <div className={styles.content}>
        {!isLastQuestion ? (
          <QuestionCard
            question={currentQuestion}
            answer={responses[currentQuestion.id]}
            onAnswer={(answer) => handleAnswer(currentQuestion.id, answer)}
          />
        ) : (
          <GoalsForm goals={goals} onChange={setGoals} />
        )}
      </div>

      <div className={styles.navigation}>
        {currentStep > 0 && (
          <button onClick={handleBack} className={styles.backButton} disabled={submitting}>
            ← Back
          </button>
        )}
        
        <div className={styles.spacer} />
        
        {!isLastQuestion ? (
          <button 
            onClick={handleNext} 
            className={styles.nextButton}
            disabled={!responses[currentQuestion.id]}
          >
            Next →
          </button>
        ) : (
          <button 
            onClick={handleSubmit} 
            className={styles.submitButton}
            disabled={!goals.learning_goal || submitting}
          >
            {submitting ? 'Submitting...' : 'Complete Onboarding'}
          </button>
        )}
      </div>
    </div>
  );
};

export default OnboardingWizard;

