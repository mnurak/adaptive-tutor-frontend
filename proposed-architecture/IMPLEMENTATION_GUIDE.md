# 🛠️ **Implementation Guide - Adaptive Learning Platform**

This guide provides step-by-step instructions for implementing the enhanced adaptive learning system.

---

## **📋 Prerequisites**

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Neo4j 5.14+
- Docker & Docker Compose (optional but recommended)

---

## **🚀 Phase 1: Database Setup**

### **Step 1.1: PostgreSQL Migration**

1. **Install Alembic**
```bash
cd adaptive-tutor-backend
pip install alembic
alembic init alembic
```

2. **Configure Alembic**

Edit `alembic.ini`:
```ini
sqlalchemy.url = postgresql+asyncpg://user:password@localhost:5432/adaptive_tutor_db
```

Edit `alembic/env.py`:
```python
from app.db.base_class import Base
from app.models.enhanced_models import *  # Import all models

target_metadata = Base.metadata
```

3. **Create Initial Migration**
```bash
alembic revision --autogenerate -m "Add enhanced schema"
alembic upgrade head
```

### **Step 1.2: Neo4j Schema Setup**

1. **Connect to Neo4j**
```bash
cypher-shell -u neo4j -p your-password
```

2. **Create Constraints**
```cypher
CREATE CONSTRAINT concept_name_unique IF NOT EXISTS
FOR (c:Concept) REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT resource_id_unique IF NOT EXISTS
FOR (r:LearningResource) REQUIRE r.id IS UNIQUE;

CREATE INDEX concept_type_idx IF NOT EXISTS
FOR (c:Concept) ON (c.type);

CREATE INDEX resource_type_idx IF NOT EXISTS
FOR (r:LearningResource) ON (r.resource_type);

CREATE INDEX resource_learning_style_idx IF NOT EXISTS
FOR (r:LearningResource) ON (r.learning_style);
```

3. **Seed Sample Data**
```cypher
// Create sample concept
CREATE (c:Concept {
  id: randomUUID(),
  name: "Binary Search Trees",
  type: "data_structure",
  complexity: "intermediate",
  estimated_hours: 4.5,
  cognitive_tags: ["visual", "analytical"],
  learning_styles: ["visual", "kinesthetic"],
  description: "A tree data structure where each node has at most two children"
});

// Create sample video resource
CREATE (r:LearningResource {
  id: randomUUID(),
  resource_type: "video",
  title: "Binary Search Trees Explained Visually",
  url: "https://youtube.com/watch?v=example",
  duration_minutes: 15,
  thumbnail_url: "https://img.youtube.com/vi/example/maxresdefault.jpg",
  difficulty_level: "beginner",
  engagement_score: 4.5,
  completion_rate: 0.87,
  learning_style: "visual",
  interaction_type: "passive",
  language: "en",
  description: "Visual explanation of BST operations"
});

// Link them
MATCH (c:Concept {name: "Binary Search Trees"})
MATCH (r:LearningResource {title: "Binary Search Trees Explained Visually"})
CREATE (c)-[:HAS_RESOURCE {
  resource_order: 1,
  recommended_for: ["visual", "beginner"]
}]->(r);
```

---

## **🔧 Phase 2: Backend Implementation**

### **Step 2.1: Update Models**

1. **Copy Enhanced Models**
```bash
cp proposed-architecture/models/enhanced_models.py app/models/
```

2. **Update Imports**

Edit `app/db/base.py`:
```python
from app.models.user import User
from app.models.enhanced_models import (
    CognitiveProfile, OnboardingQuestionnaire,
    LearningSession, ResourceInteraction,
    ConceptMastery, BehavioralMetrics
)
```

### **Step 2.2: Implement Services**

1. **Copy Service Files**
```bash
cp proposed-architecture/services/enhanced_knowledge_graph.py app/services/
cp proposed-architecture/services/behavioral_analytics.py app/services/
cp proposed-architecture/services/onboarding_service.py app/services/
```

2. **Update Dependencies**

Add to `requirements.txt`:
```
alembic>=1.12.0
redis>=5.0.0
celery>=5.3.0  # For background tasks (optional)
```

### **Step 2.3: Create API Endpoints**

Create `app/api/v1/endpoints/onboarding.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.services.onboarding_service import onboarding_service, OnboardingSubmission
from app.schemas.cognitive_profile import CognitiveProfileResponse

router = APIRouter()

@router.get("/questionnaire")
async def get_questionnaire():
    """Get the onboarding questionnaire"""
    return onboarding_service.get_questionnaire()

@router.post("/submit", response_model=CognitiveProfileResponse)
async def submit_onboarding(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    submission: OnboardingSubmission
):
    """Process onboarding submission and create cognitive profile"""
    profile = await onboarding_service.process_onboarding(
        db, current_user.id, submission
    )
    return profile
```

Create `app/api/v1/endpoints/analytics.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.services.behavioral_analytics import behavioral_analytics_service

router = APIRouter()

@router.get("/resource-preferences")
async def get_resource_preferences(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    days_back: int = 30
):
    """Get user's resource consumption preferences"""
    return await behavioral_analytics_service.analyze_resource_preferences(
        db, current_user.id, days_back
    )

@router.get("/learning-patterns")
async def get_learning_patterns(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    days_back: int = 30
):
    """Get user's learning patterns"""
    return await behavioral_analytics_service.analyze_learning_patterns(
        db, current_user.id, days_back
    )

@router.post("/update-profile")
async def update_cognitive_profile(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Trigger cognitive profile update based on behavior"""
    updates = await behavioral_analytics_service.infer_cognitive_updates(
        db, current_user.id
    )
    
    # Apply updates to profile
    profile = current_user.cognitive_profile
    for key, value in updates["updates"].items():
        setattr(profile, key, value)
    
    for key, value in updates["confidence_scores"].items():
        setattr(profile, key, value)
    
    profile.total_adaptations += 1
    profile.profile_version += 1
    
    await db.commit()
    await db.refresh(profile)
    
    return {
        "profile": profile,
        "supporting_data": updates["supporting_data"]
    }
```

Create `app/api/v1/endpoints/sessions.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.api import deps
from app.models.user import User
from app.models.enhanced_models import LearningSession, ResourceInteraction
from app.schemas.session import SessionCreate, SessionEnd, ResourceInteractionCreate

router = APIRouter()

@router.post("/start")
async def start_session(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    session_data: SessionCreate
):
    """Start a new learning session"""
    session = LearningSession(
        user_id=current_user.id,
        session_type=session_data.session_type,
        device_type=session_data.device_type
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

@router.post("/{session_id}/end")
async def end_session(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    session_id: str,
    session_end: SessionEnd
):
    """End a learning session and calculate metrics"""
    session = await db.get(LearningSession, session_id)
    
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.ended_at = datetime.utcnow()
    session.duration_seconds = (session.ended_at - session.started_at).total_seconds()
    session.completion_rate = session_end.completion_rate
    session.focus_score = session_end.focus_score
    session.concepts_covered = session_end.concepts_covered
    
    await db.commit()
    return session

@router.post("/{session_id}/interactions")
async def track_resource_interaction(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    session_id: str,
    interaction: ResourceInteractionCreate
):
    """Track interaction with a learning resource"""
    resource_interaction = ResourceInteraction(
        user_id=current_user.id,
        session_id=session_id,
        **interaction.dict()
    )
    db.add(resource_interaction)
    await db.commit()
    await db.refresh(resource_interaction)
    return resource_interaction
```

### **Step 2.4: Update API Router**

Edit `app/api/v1/api.py`:
```python
from app.api.v1.endpoints import (
    auth, users, concepts, instructions, chat,
    onboarding, analytics, sessions  # NEW
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/login", tags=["Authentication"])
api_router.include_router(users.router, prefix="/student", tags=["Student"])
api_router.include_router(concepts.router, prefix="/concept", tags=["Knowledge Graph"])
api_router.include_router(instructions.router, prefix="/instruction", tags=["Tutoring"])
api_router.include_router(chat.router, prefix="/chat", tags=["Conversational Chat"])
api_router.include_router(onboarding.router, prefix="/onboarding", tags=["Onboarding"])  # NEW
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])  # NEW
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])  # NEW
```

---

## **🎨 Phase 3: Frontend Implementation**

### **Step 3.1: Create Onboarding Component**

Create `src/components/Onboarding/OnboardingWizard.jsx`:
```jsx
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
    }
  };

  if (loading) {
    return <div className={styles.loading}>Loading questionnaire...</div>;
  }

  const isLastQuestion = currentStep === questions.length;
  const currentQuestion = questions[currentStep];
  const progress = ((currentStep + 1) / (questions.length + 1)) * 100;

  return (
    <div className={styles.container}>
      <ProgressBar progress={progress} />
      
      {!isLastQuestion ? (
        <QuestionCard
          question={currentQuestion}
          answer={responses[currentQuestion.id]}
          onAnswer={(answer) => handleAnswer(currentQuestion.id, answer)}
        />
      ) : (
        <GoalsForm goals={goals} onChange={setGoals} />
      )}

      <div className={styles.navigation}>
        {currentStep > 0 && (
          <button onClick={handleBack} className={styles.backButton}>
            Back
          </button>
        )}
        
        {!isLastQuestion ? (
          <button 
            onClick={handleNext} 
            className={styles.nextButton}
            disabled={!responses[currentQuestion.id]}
          >
            Next
          </button>
        ) : (
          <button 
            onClick={handleSubmit} 
            className={styles.submitButton}
            disabled={!goals.learning_goal}
          >
            Complete Onboarding
          </button>
        )}
      </div>
    </div>
  );
};

export default OnboardingWizard;
```

### **Step 3.2: Create Session Tracking Hook**

Create `src/hooks/useSessionTracking.js`:
```javascript
import { useState, useEffect, useRef } from 'react';
import api from '../api/api';

export const useSessionTracking = (sessionType = 'chat') => {
  const [sessionId, setSessionId] = useState(null);
  const sessionStartTime = useRef(null);
  const interactionsCount = useRef(0);

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
        concepts_covered: getConceptsCovered()
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

  const getDeviceType = () => {
    const width = window.innerWidth;
    if (width < 768) return 'mobile';
    if (width < 1024) return 'tablet';
    return 'desktop';
  };

  const calculateCompletionRate = () => {
    // Implement based on your logic
    return 0.8;
  };

  const calculateFocusScore = () => {
    // Implement based on interaction patterns
    return 0.75;
  };

  const getConceptsCovered = () => {
    // Implement based on your tracking
    return [];
  };

  return {
    sessionId,
    trackResourceInteraction
  };
};
```

---

## **📊 Phase 4: Testing**

### **Step 4.1: Backend Tests**

Create `tests/test_behavioral_analytics.py`:
```python
import pytest
from app.services.behavioral_analytics import behavioral_analytics_service

@pytest.mark.asyncio
async def test_analyze_resource_preferences(db_session, test_user):
    # Create test data
    # ... add resource interactions
    
    prefs = await behavioral_analytics_service.analyze_resource_preferences(
        db_session, test_user.id, days_back=30
    )
    
    assert "video_to_text_ratio" in prefs
    assert "preferred_resource_type" in prefs

@pytest.mark.asyncio
async def test_infer_cognitive_updates(db_session, test_user):
    updates = await behavioral_analytics_service.infer_cognitive_updates(
        db_session, test_user.id
    )
    
    assert "updates" in updates
    assert "confidence_scores" in updates
```

---

## **🚀 Phase 5: Deployment**

See `ARCHITECTURE.md` for deployment architecture details.

---

## **📚 Additional Resources**

- PostgreSQL Schema: `enhanced-postgres-schema.sql`
- SQLAlchemy Models: `models/enhanced_models.py`
- Services: `services/` directory
- API Documentation: Auto-generated at `/docs`

