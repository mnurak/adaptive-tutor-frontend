"""
Enhanced SQLAlchemy Models for Adaptive Learning Platform
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, 
    ForeignKey, Text, Enum, ARRAY, JSON, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
import enum

from app.db.base_class import Base


# ============================================================================
# ENUMS
# ============================================================================

class InstructionFlow(str, enum.Enum):
    LINEAR = "linear"
    EXPLORATORY = "exploratory"
    MIXED = "mixed"


class InputPreference(str, enum.Enum):
    VISUAL = "visual"
    VERBAL = "verbal"
    MIXED = "mixed"


class EngagementStyle(str, enum.Enum):
    PASSIVE = "passive"
    ACTIVE = "active"
    MIXED = "mixed"


class ConceptTypePreference(str, enum.Enum):
    CONCRETE = "concrete"
    ABSTRACT = "abstract"
    MIXED = "mixed"


class LearningAutonomy(str, enum.Enum):
    GUIDED = "guided"
    INDEPENDENT = "independent"
    MIXED = "mixed"


class MotivationType(str, enum.Enum):
    INTRINSIC = "intrinsic"
    EXTRINSIC = "extrinsic"
    MIXED = "mixed"


class FeedbackPreference(str, enum.Enum):
    IMMEDIATE = "immediate"
    DELAYED = "delayed"
    MIXED = "mixed"


class ComplexityTolerance(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ResourceType(str, enum.Enum):
    VIDEO = "video"
    ARTICLE = "article"
    INTERACTIVE = "interactive"
    CODE_EXAMPLE = "code_example"
    QUIZ = "quiz"
    CHAT = "chat"


class MasteryLevel(str, enum.Enum):
    NOT_STARTED = "not_started"
    LEARNING = "learning"
    PRACTICING = "practicing"
    PROFICIENT = "proficient"
    MASTERED = "mastered"


# ============================================================================
# MODELS
# ============================================================================

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    timezone = Column(String(50), default="UTC")
    
    # Relationships
    cognitive_profile = relationship("CognitiveProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    onboarding = relationship("OnboardingQuestionnaire", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("LearningSession", back_populates="user", cascade="all, delete-orphan")
    resource_interactions = relationship("ResourceInteraction", back_populates="user", cascade="all, delete-orphan")
    concept_mastery = relationship("ConceptMastery", back_populates="user", cascade="all, delete-orphan")
    behavioral_metrics = relationship("BehavioralMetrics", back_populates="user", cascade="all, delete-orphan")


class CognitiveProfile(Base):
    __tablename__ = "cognitive_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    # Core Cognitive Dimensions
    instruction_flow = Column(Enum(InstructionFlow), default=InstructionFlow.LINEAR)
    input_preference = Column(Enum(InputPreference), default=InputPreference.MIXED)
    engagement_style = Column(Enum(EngagementStyle), default=EngagementStyle.MIXED)
    concept_type = Column(Enum(ConceptTypePreference), default=ConceptTypePreference.MIXED)
    learning_autonomy = Column(Enum(LearningAutonomy), default=LearningAutonomy.GUIDED)
    motivation_type = Column(Enum(MotivationType), default=MotivationType.MIXED)
    feedback_preference = Column(Enum(FeedbackPreference), default=FeedbackPreference.IMMEDIATE)
    complexity_tolerance = Column(Enum(ComplexityTolerance), default=ComplexityTolerance.MEDIUM)
    
    # Confidence Scores (0.0 - 1.0)
    instruction_flow_confidence = Column(Float, default=0.5)
    input_preference_confidence = Column(Float, default=0.5)
    engagement_style_confidence = Column(Float, default=0.5)
    concept_type_confidence = Column(Float, default=0.5)
    learning_autonomy_confidence = Column(Float, default=0.5)
    motivation_type_confidence = Column(Float, default=0.5)
    feedback_preference_confidence = Column(Float, default=0.5)
    complexity_tolerance_confidence = Column(Float, default=0.5)
    
    # Metadata
    profile_version = Column(Integer, default=1)
    last_updated = Column(DateTime(timezone=True), default=datetime.utcnow)
    total_adaptations = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="cognitive_profile")


class OnboardingQuestionnaire(Base):
    __tablename__ = "onboarding_questionnaires"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Learning Style Questions
    preferred_learning_medium = Column(String(50))  # video, text, interactive, mixed
    learning_pace = Column(String(50))  # slow, moderate, fast
    prior_programming_experience = Column(String(50))  # none, beginner, intermediate, advanced
    
    # Cognitive Preferences
    prefers_examples_or_theory = Column(String(50))  # examples, theory, both
    prefers_step_by_step_or_overview = Column(String(50))  # step_by_step, overview, both
    comfort_with_complexity = Column(String(50))  # low, medium, high
    
    # Motivation & Goals
    learning_goal = Column(Text)
    available_hours_per_week = Column(Integer)
    preferred_session_duration = Column(Integer)  # minutes
    
    # Additional Context
    previous_topics_studied = Column(ARRAY(String))
    areas_of_interest = Column(ARRAY(String))
    
    # Raw Responses (JSON for flexibility)
    raw_responses = Column(JSONB)
    
    # Derived Initial Profile
    initial_cognitive_profile = Column(JSONB)
    
    # Relationships
    user = relationship("User", back_populates="onboarding")


class LearningSession(Base):
    __tablename__ = "learning_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Session Metadata
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    ended_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    
    # Session Context
    session_type = Column(String(50))  # chat, lesson, practice, review
    device_type = Column(String(50))  # desktop, mobile, tablet
    
    # Engagement Metrics
    interactions_count = Column(Integer, default=0)
    resources_viewed = Column(Integer, default=0)
    concepts_covered = Column(ARRAY(String))
    
    # Quality Metrics
    focus_score = Column(Float)  # 0.0 - 1.0
    completion_rate = Column(Float)  # percentage
    
    # Cognitive State
    cognitive_load_estimate = Column(String(50))  # low, medium, high
    frustration_indicators = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    resource_interactions = relationship("ResourceInteraction", back_populates="session", cascade="all, delete-orphan")


class ResourceInteraction(Base):
    __tablename__ = "resource_interactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("learning_sessions.id", ondelete="SET NULL"), index=True)
    
    # Resource Identification
    resource_id = Column(String(255), nullable=False)  # Neo4j resource ID
    resource_type = Column(Enum(ResourceType), nullable=False, index=True)
    concept_name = Column(String(255), index=True)
    
    # Interaction Metrics
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    ended_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    
    # Engagement Metrics
    completion_percentage = Column(Float, default=0.0)
    interaction_count = Column(Integer, default=0)
    engagement_score = Column(Integer, CheckConstraint('engagement_score >= 1 AND engagement_score <= 5'))
    
    # Video-specific metrics
    video_watch_percentage = Column(Float)
    video_pauses_count = Column(Integer)
    video_rewinds_count = Column(Integer)
    video_speed = Column(Float, default=1.0)
    
    # Text-specific metrics
    text_scroll_depth = Column(Float)
    text_time_per_section = Column(JSONB)
    
    # Outcome
    marked_as_helpful = Column(Boolean)
    marked_as_confusing = Column(Boolean)
    user_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resource_interactions")
    session = relationship("LearningSession", back_populates="resource_interactions")


class ConceptMastery(Base):
    __tablename__ = "concept_mastery"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_name = Column(String(255), nullable=False, index=True)

    # Mastery Metrics
    current_level = Column(Enum(MasteryLevel), default=MasteryLevel.NOT_STARTED, index=True)
    confidence_score = Column(Float, default=0.0)  # 0.0 - 1.0

    # Time Investment
    total_time_spent_seconds = Column(Integer, default=0)
    first_encountered_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_practiced_at = Column(DateTime(timezone=True))

    # Resource Consumption
    videos_watched = Column(Integer, default=0)
    articles_read = Column(Integer, default=0)
    exercises_completed = Column(Integer, default=0)

    # Performance Metrics
    quiz_attempts = Column(Integer, default=0)
    quiz_success_rate = Column(Float)
    average_response_time_seconds = Column(Float)

    # Learning Curve
    learning_velocity = Column(Float)  # rate of improvement
    retention_score = Column(Float)  # how well knowledge is retained

    # Metadata
    last_updated = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="concept_mastery")

    __table_args__ = (
        CheckConstraint('confidence_score >= 0.0 AND confidence_score <= 1.0'),
    )


class BehavioralMetrics(Base):
    __tablename__ = "behavioral_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Time Window
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False)
    period_type = Column(String(50))  # daily, weekly, monthly

    # Session Patterns
    total_sessions = Column(Integer, default=0)
    avg_session_duration_minutes = Column(Float)
    total_learning_time_minutes = Column(Integer, default=0)
    preferred_learning_times = Column(JSONB)  # {hour: session_count}

    # Resource Preferences
    video_to_text_ratio = Column(Float)  # videos / (videos + text)
    interactive_engagement_rate = Column(Float)
    avg_video_completion_rate = Column(Float)
    avg_article_completion_rate = Column(Float)

    # Learning Behavior
    concepts_explored = Column(Integer, default=0)
    concepts_mastered = Column(Integer, default=0)
    avg_time_per_concept_minutes = Column(Float)
    learning_path_adherence = Column(Float)  # 0.0 - 1.0

    # Engagement Quality
    avg_focus_score = Column(Float)
    frustration_events = Column(Integer, default=0)
    help_requests = Column(Integer, default=0)

    # Cognitive Indicators
    complexity_seeking_score = Column(Float)  # tendency to seek harder content
    autonomy_score = Column(Float)  # self-directed vs guided learning
    persistence_score = Column(Float)  # ability to stick with difficult topics

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="behavioral_metrics")

