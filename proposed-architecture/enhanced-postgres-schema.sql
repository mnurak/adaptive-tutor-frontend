-- ============================================================================
-- ENHANCED POSTGRESQL SCHEMA FOR ADAPTIVE LEARNING PLATFORM
-- ============================================================================

-- ============================================================================
-- 1. USER & AUTHENTICATION
-- ============================================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    timezone VARCHAR(50) DEFAULT 'UTC'
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- ============================================================================
-- 2. ENHANCED COGNITIVE PROFILE
-- ============================================================================

CREATE TYPE instruction_flow_type AS ENUM ('linear', 'exploratory', 'mixed');
CREATE TYPE input_preference_type AS ENUM ('visual', 'verbal', 'mixed');
CREATE TYPE engagement_style_type AS ENUM ('passive', 'active', 'mixed');
CREATE TYPE concept_type_preference AS ENUM ('concrete', 'abstract', 'mixed');
CREATE TYPE learning_autonomy_type AS ENUM ('guided', 'independent', 'mixed');
CREATE TYPE motivation_type AS ENUM ('intrinsic', 'extrinsic', 'mixed');
CREATE TYPE feedback_preference_type AS ENUM ('immediate', 'delayed', 'mixed');
CREATE TYPE complexity_tolerance_type AS ENUM ('low', 'medium', 'high');

CREATE TABLE cognitive_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Core Cognitive Dimensions
    instruction_flow instruction_flow_type DEFAULT 'linear',
    input_preference input_preference_type DEFAULT 'mixed',
    engagement_style engagement_style_type DEFAULT 'mixed',
    concept_type concept_type_preference DEFAULT 'mixed',
    learning_autonomy learning_autonomy_type DEFAULT 'guided',
    motivation_type motivation_type DEFAULT 'mixed',
    feedback_preference feedback_preference_type DEFAULT 'immediate',
    complexity_tolerance complexity_tolerance_type DEFAULT 'medium',
    
    -- Confidence Scores (0.0 - 1.0)
    instruction_flow_confidence FLOAT DEFAULT 0.5,
    input_preference_confidence FLOAT DEFAULT 0.5,
    engagement_style_confidence FLOAT DEFAULT 0.5,
    concept_type_confidence FLOAT DEFAULT 0.5,
    learning_autonomy_confidence FLOAT DEFAULT 0.5,
    motivation_type_confidence FLOAT DEFAULT 0.5,
    feedback_preference_confidence FLOAT DEFAULT 0.5,
    complexity_tolerance_confidence FLOAT DEFAULT 0.5,
    
    -- Metadata
    profile_version INT DEFAULT 1,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    total_adaptations INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_cognitive_profiles_user_id ON cognitive_profiles(user_id);

-- ============================================================================
-- 3. ONBOARDING QUESTIONNAIRE
-- ============================================================================

CREATE TABLE onboarding_questionnaires (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Learning Style Questions
    preferred_learning_medium VARCHAR(50), -- video, text, interactive, mixed
    learning_pace VARCHAR(50), -- slow, moderate, fast
    prior_programming_experience VARCHAR(50), -- none, beginner, intermediate, advanced
    
    -- Cognitive Preferences
    prefers_examples_or_theory VARCHAR(50), -- examples, theory, both
    prefers_step_by_step_or_overview VARCHAR(50), -- step_by_step, overview, both
    comfort_with_complexity VARCHAR(50), -- low, medium, high
    
    -- Motivation & Goals
    learning_goal TEXT,
    available_hours_per_week INT,
    preferred_session_duration INT, -- minutes
    
    -- Additional Context
    previous_topics_studied TEXT[], -- array of topic names
    areas_of_interest TEXT[],
    
    -- Raw Responses (JSON for flexibility)
    raw_responses JSONB,
    
    -- Derived Initial Profile
    initial_cognitive_profile JSONB
);

CREATE INDEX idx_onboarding_user_id ON onboarding_questionnaires(user_id);

-- ============================================================================
-- 4. LEARNING SESSIONS
-- ============================================================================

CREATE TABLE learning_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Session Metadata
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INT,
    
    -- Session Context
    session_type VARCHAR(50), -- chat, lesson, practice, review
    device_type VARCHAR(50), -- desktop, mobile, tablet
    
    -- Engagement Metrics
    interactions_count INT DEFAULT 0,
    resources_viewed INT DEFAULT 0,
    concepts_covered TEXT[], -- array of concept names
    
    -- Quality Metrics
    focus_score FLOAT, -- 0.0 - 1.0, derived from interaction patterns
    completion_rate FLOAT, -- percentage of planned content completed
    
    -- Cognitive State
    cognitive_load_estimate VARCHAR(50), -- low, medium, high
    frustration_indicators INT DEFAULT 0, -- count of signs of struggle
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sessions_user_id ON learning_sessions(user_id);
CREATE INDEX idx_sessions_started_at ON learning_sessions(started_at);
CREATE INDEX idx_sessions_user_started ON learning_sessions(user_id, started_at DESC);

-- ============================================================================
-- 5. RESOURCE INTERACTIONS
-- ============================================================================

CREATE TYPE resource_type AS ENUM ('video', 'article', 'interactive', 'code_example', 'quiz', 'chat');

CREATE TABLE resource_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID REFERENCES learning_sessions(id) ON DELETE SET NULL,
    
    -- Resource Identification
    resource_id VARCHAR(255) NOT NULL, -- Neo4j resource ID
    resource_type resource_type NOT NULL,
    concept_name VARCHAR(255),
    
    -- Interaction Metrics
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INT,
    
    -- Engagement Metrics
    completion_percentage FLOAT DEFAULT 0.0,
    interaction_count INT DEFAULT 0, -- clicks, pauses, rewinds for video
    engagement_score INT CHECK (engagement_score BETWEEN 1 AND 5),
    
    -- Video-specific metrics
    video_watch_percentage FLOAT,
    video_pauses_count INT,
    video_rewinds_count INT,
    video_speed FLOAT DEFAULT 1.0,
    
    -- Text-specific metrics
    text_scroll_depth FLOAT,
    text_time_per_section JSONB, -- {section_id: seconds}
    
    -- Outcome
    marked_as_helpful BOOLEAN,
    marked_as_confusing BOOLEAN,
    user_notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_resource_interactions_user_id ON resource_interactions(user_id);
CREATE INDEX idx_resource_interactions_session_id ON resource_interactions(session_id);
CREATE INDEX idx_resource_interactions_resource_type ON resource_interactions(resource_type);
CREATE INDEX idx_resource_interactions_concept ON resource_interactions(concept_name);

-- ============================================================================
-- 6. CONCEPT MASTERY TRACKING
-- ============================================================================

CREATE TYPE mastery_level AS ENUM ('not_started', 'learning', 'practicing', 'proficient', 'mastered');

CREATE TABLE concept_mastery (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    concept_name VARCHAR(255) NOT NULL,
    
    -- Mastery Metrics
    current_level mastery_level DEFAULT 'not_started',
    confidence_score FLOAT DEFAULT 0.0, -- 0.0 - 1.0
    
    -- Time Investment
    total_time_spent_seconds INT DEFAULT 0,
    first_encountered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_practiced_at TIMESTAMP WITH TIME ZONE,
    
    -- Resource Consumption
    videos_watched INT DEFAULT 0,
    articles_read INT DEFAULT 0,
    exercises_completed INT DEFAULT 0,
    
    -- Performance Metrics
    quiz_attempts INT DEFAULT 0,
    quiz_success_rate FLOAT,
    average_response_time_seconds FLOAT,
    
    -- Learning Curve
    learning_velocity FLOAT, -- rate of improvement
    retention_score FLOAT, -- how well knowledge is retained over time
    
    -- Metadata
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, concept_name)
);

CREATE INDEX idx_concept_mastery_user_id ON concept_mastery(user_id);
CREATE INDEX idx_concept_mastery_concept ON concept_mastery(concept_name);
CREATE INDEX idx_concept_mastery_level ON concept_mastery(current_level);

-- ============================================================================
-- 7. BEHAVIORAL ANALYTICS
-- ============================================================================

CREATE TABLE behavioral_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Time Window
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    period_type VARCHAR(50), -- daily, weekly, monthly
    
    -- Session Patterns
    total_sessions INT DEFAULT 0,
    avg_session_duration_minutes FLOAT,
    total_learning_time_minutes INT DEFAULT 0,
    preferred_learning_times JSONB, -- {hour: session_count}
    
    -- Resource Preferences
    video_to_text_ratio FLOAT, -- videos / (videos + text)
    interactive_engagement_rate FLOAT,
    avg_video_completion_rate FLOAT,
    avg_article_completion_rate FLOAT,
    
    -- Learning Behavior
    concepts_explored INT DEFAULT 0,
    concepts_mastered INT DEFAULT 0,
    avg_time_per_concept_minutes FLOAT,
    learning_path_adherence FLOAT, -- 0.0 - 1.0
    
    -- Engagement Quality
    avg_focus_score FLOAT,
    frustration_events INT DEFAULT 0,
    help_requests INT DEFAULT 0,
    
    -- Cognitive Indicators
    complexity_seeking_score FLOAT, -- tendency to seek harder content
    autonomy_score FLOAT, -- self-directed vs guided learning
    persistence_score FLOAT, -- ability to stick with difficult topics
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, period_start, period_type)
);

CREATE INDEX idx_behavioral_metrics_user_id ON behavioral_metrics(user_id);
CREATE INDEX idx_behavioral_metrics_period ON behavioral_metrics(period_start, period_end);

