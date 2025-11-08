import React from 'react';
import styles from './QuestionCard.module.css';

const QuestionCard = ({ question, answer, onAnswer }) => {
  if (!question) return null;

  const renderInput = () => {
    switch (question.type) {
      case 'multiple_choice':
        return (
          <div className={styles.options}>
            {question.options.map((option, index) => (
              <button
                key={index}
                className={`${styles.option} ${answer === option ? styles.selected : ''}`}
                onClick={() => onAnswer(option)}
              >
                {option}
              </button>
            ))}
          </div>
        );

      case 'scale':
        return (
          <div className={styles.scaleContainer}>
            <div className={styles.scaleLabels}>
              <span>{question.scale_labels?.min || 'Low'}</span>
              <span>{question.scale_labels?.max || 'High'}</span>
            </div>
            <div className={styles.scale}>
              {[1, 2, 3, 4, 5].map((value) => (
                <button
                  key={value}
                  className={`${styles.scaleButton} ${answer === value ? styles.selected : ''}`}
                  onClick={() => onAnswer(value)}
                >
                  {value}
                </button>
              ))}
            </div>
          </div>
        );

      case 'text':
        return (
          <textarea
            className={styles.textInput}
            value={answer || ''}
            onChange={(e) => onAnswer(e.target.value)}
            placeholder="Type your answer here..."
            rows={4}
          />
        );

      default:
        return null;
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.questionNumber}>
        Question {question.order || ''}
      </div>
      <h2 className={styles.questionText}>{question.question}</h2>
      {question.description && (
        <p className={styles.description}>{question.description}</p>
      )}
      <div className={styles.inputContainer}>
        {renderInput()}
      </div>
    </div>
  );
};

export default QuestionCard;

