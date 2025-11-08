"""
Behavioral Analytics Service - Analyzes student behavior to update cognitive profiles
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from collections import defaultdict

from app.models.enhanced_models import (
    User, CognitiveProfile, LearningSession, ResourceInteraction,
    ConceptMastery, BehavioralMetrics, ResourceType, MasteryLevel,
    InputPreference, ComplexityTolerance, EngagementStyle, LearningAutonomy
)


class BehavioralAnalyticsService:
    """
    Analyzes student learning behavior to infer and update cognitive profiles
    """
    
    def __init__(self):
        self.adaptation_rate = 0.15  # How quickly profile adapts to new data
        self.confidence_threshold = 0.7  # Threshold for high-confidence predictions
    
    # ========================================================================
    # BEHAVIORAL PATTERN ANALYSIS
    # ========================================================================
    
    async def analyze_resource_preferences(
        self,
        db: AsyncSession,
        user_id: str,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze user's resource consumption patterns
        Returns insights about video vs text preference, engagement patterns, etc.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        # Query resource interactions
        query = select(ResourceInteraction).where(
            and_(
                ResourceInteraction.user_id == user_id,
                ResourceInteraction.started_at >= cutoff_date
            )
        )
        result = await db.execute(query)
        interactions = result.scalars().all()
        
        if not interactions:
            return self._get_default_preferences()
        
        # Analyze patterns
        video_count = 0
        text_count = 0
        interactive_count = 0
        
        total_video_completion = 0.0
        total_text_completion = 0.0
        total_interactive_completion = 0.0
        
        video_engagement_scores = []
        text_engagement_scores = []
        
        for interaction in interactions:
            if interaction.resource_type == ResourceType.VIDEO:
                video_count += 1
                total_video_completion += interaction.completion_percentage or 0
                if interaction.engagement_score:
                    video_engagement_scores.append(interaction.engagement_score)
            
            elif interaction.resource_type in [ResourceType.ARTICLE, ResourceType.CODE_EXAMPLE]:
                text_count += 1
                total_text_completion += interaction.completion_percentage or 0
                if interaction.engagement_score:
                    text_engagement_scores.append(interaction.engagement_score)
            
            elif interaction.resource_type == ResourceType.INTERACTIVE:
                interactive_count += 1
                total_interactive_completion += interaction.completion_percentage or 0
        
        total_resources = video_count + text_count + interactive_count
        
        # Calculate metrics
        video_to_text_ratio = video_count / (text_count + 1)  # Avoid division by zero
        
        avg_video_completion = total_video_completion / video_count if video_count > 0 else 0
        avg_text_completion = total_text_completion / text_count if text_count > 0 else 0
        avg_interactive_completion = total_interactive_completion / interactive_count if interactive_count > 0 else 0
        
        avg_video_engagement = sum(video_engagement_scores) / len(video_engagement_scores) if video_engagement_scores else 0
        avg_text_engagement = sum(text_engagement_scores) / len(text_engagement_scores) if text_engagement_scores else 0
        
        return {
            "video_count": video_count,
            "text_count": text_count,
            "interactive_count": interactive_count,
            "total_resources": total_resources,
            "video_to_text_ratio": video_to_text_ratio,
            "avg_video_completion": avg_video_completion,
            "avg_text_completion": avg_text_completion,
            "avg_interactive_completion": avg_interactive_completion,
            "avg_video_engagement": avg_video_engagement,
            "avg_text_engagement": avg_text_engagement,
            "preferred_resource_type": self._determine_preferred_resource_type(
                video_count, text_count, interactive_count,
                avg_video_engagement, avg_text_engagement
            )
        }
    
    async def analyze_learning_patterns(
        self,
        db: AsyncSession,
        user_id: str,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze learning session patterns to infer cognitive traits
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        # Query learning sessions
        query = select(LearningSession).where(
            and_(
                LearningSession.user_id == user_id,
                LearningSession.started_at >= cutoff_date
            )
        )
        result = await db.execute(query)
        sessions = result.scalars().all()
        
        if not sessions:
            return self._get_default_learning_patterns()
        
        # Analyze session patterns
        total_sessions = len(sessions)
        total_duration = sum(s.duration_seconds or 0 for s in sessions)
        avg_session_duration = total_duration / total_sessions if total_sessions > 0 else 0
        
        # Analyze time of day preferences
        hour_distribution = defaultdict(int)
        for session in sessions:
            hour = session.started_at.hour
            hour_distribution[hour] += 1
        
        # Analyze focus and completion
        focus_scores = [s.focus_score for s in sessions if s.focus_score is not None]
        completion_rates = [s.completion_rate for s in sessions if s.completion_rate is not None]
        frustration_count = sum(s.frustration_indicators or 0 for s in sessions)
        
        avg_focus = sum(focus_scores) / len(focus_scores) if focus_scores else 0.5
        avg_completion = sum(completion_rates) / len(completion_rates) if completion_rates else 0.5
        
        # Analyze concept coverage
        all_concepts = []
        for session in sessions:
            if session.concepts_covered:
                all_concepts.extend(session.concepts_covered)
        
        unique_concepts = len(set(all_concepts))
        concept_revisit_rate = len(all_concepts) / unique_concepts if unique_concepts > 0 else 1.0
        
        return {
            "total_sessions": total_sessions,
            "avg_session_duration_minutes": avg_session_duration / 60,
            "total_learning_time_hours": total_duration / 3600,
            "preferred_learning_hours": sorted(hour_distribution.items(), key=lambda x: x[1], reverse=True)[:3],
            "avg_focus_score": avg_focus,
            "avg_completion_rate": avg_completion,
            "frustration_events": frustration_count,
            "unique_concepts_explored": unique_concepts,
            "concept_revisit_rate": concept_revisit_rate,
            "learning_consistency": self._calculate_consistency(sessions)
        }
    
    async def analyze_mastery_progression(
        self,
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Analyze how quickly user masters concepts (learning velocity)
        """
        query = select(ConceptMastery).where(ConceptMastery.user_id == user_id)
        result = await db.execute(query)
        masteries = result.scalars().all()
        
        if not masteries:
            return self._get_default_mastery_metrics()
        
        # Analyze mastery levels
        level_distribution = defaultdict(int)
        for mastery in masteries:
            level_distribution[mastery.current_level.value] += 1
        
        # Calculate learning velocity
        velocities = [m.learning_velocity for m in masteries if m.learning_velocity is not None]
        avg_velocity = sum(velocities) / len(velocities) if velocities else 0.5
        
        # Calculate retention
        retentions = [m.retention_score for m in masteries if m.retention_score is not None]
        avg_retention = sum(retentions) / len(retentions) if retentions else 0.5
        
        # Analyze time investment
        total_time = sum(m.total_time_spent_seconds for m in masteries)
        avg_time_per_concept = total_time / len(masteries) if masteries else 0
        
        return {
            "total_concepts_tracked": len(masteries),
            "mastery_distribution": dict(level_distribution),
            "avg_learning_velocity": avg_velocity,
            "avg_retention_score": avg_retention,
            "avg_time_per_concept_hours": avg_time_per_concept / 3600,
            "concepts_mastered": level_distribution.get("mastered", 0),
            "concepts_in_progress": level_distribution.get("learning", 0) + level_distribution.get("practicing", 0)
        }
    
    # ========================================================================
    # COGNITIVE PROFILE INFERENCE
    # ========================================================================
    
    async def infer_cognitive_updates(
        self,
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Infer cognitive profile updates based on behavioral analysis
        """
        # Gather all behavioral data
        resource_prefs = await self.analyze_resource_preferences(db, user_id)
        learning_patterns = await self.analyze_learning_patterns(db, user_id)
        mastery_metrics = await self.analyze_mastery_progression(db, user_id)
        
        # Infer cognitive dimensions
        updates = {}
        confidence_scores = {}
        
        # 1. Input Preference (visual vs verbal)
        if resource_prefs["video_to_text_ratio"] > 2.0 and resource_prefs["avg_video_engagement"] > 3.5:
            updates["input_preference"] = InputPreference.VISUAL
            confidence_scores["input_preference_confidence"] = min(0.9, resource_prefs["avg_video_engagement"] / 5.0)
        elif resource_prefs["video_to_text_ratio"] < 0.5 and resource_prefs["avg_text_engagement"] > 3.5:
            updates["input_preference"] = InputPreference.VERBAL
            confidence_scores["input_preference_confidence"] = min(0.9, resource_prefs["avg_text_engagement"] / 5.0)
        else:
            updates["input_preference"] = InputPreference.MIXED
            confidence_scores["input_preference_confidence"] = 0.6
        
        # 2. Complexity Tolerance
        if mastery_metrics["avg_learning_velocity"] > 0.7 and learning_patterns["avg_completion_rate"] > 0.8:
            updates["complexity_tolerance"] = ComplexityTolerance.HIGH
            confidence_scores["complexity_tolerance_confidence"] = 0.85
        elif learning_patterns["frustration_events"] > 5 or learning_patterns["avg_completion_rate"] < 0.5:
            updates["complexity_tolerance"] = ComplexityTolerance.LOW
            confidence_scores["complexity_tolerance_confidence"] = 0.75
        else:
            updates["complexity_tolerance"] = ComplexityTolerance.MEDIUM
            confidence_scores["complexity_tolerance_confidence"] = 0.7
        
        # 3. Engagement Style (passive vs active)
        if resource_prefs["interactive_count"] > resource_prefs["total_resources"] * 0.3:
            updates["engagement_style"] = EngagementStyle.ACTIVE
            confidence_scores["engagement_style_confidence"] = 0.8
        elif resource_prefs["interactive_count"] < resource_prefs["total_resources"] * 0.1:
            updates["engagement_style"] = EngagementStyle.PASSIVE
            confidence_scores["engagement_style_confidence"] = 0.75
        else:
            updates["engagement_style"] = EngagementStyle.MIXED
            confidence_scores["engagement_style_confidence"] = 0.65
        
        # 4. Learning Autonomy
        if learning_patterns["concept_revisit_rate"] < 1.2 and learning_patterns["avg_focus_score"] > 0.7:
            updates["learning_autonomy"] = LearningAutonomy.INDEPENDENT
            confidence_scores["learning_autonomy_confidence"] = 0.8
        elif learning_patterns["concept_revisit_rate"] > 2.0 or learning_patterns["frustration_events"] > 3:
            updates["learning_autonomy"] = LearningAutonomy.GUIDED
            confidence_scores["learning_autonomy_confidence"] = 0.75
        else:
            updates["learning_autonomy"] = LearningAutonomy.MIXED
            confidence_scores["learning_autonomy_confidence"] = 0.6
        
        return {
            "updates": updates,
            "confidence_scores": confidence_scores,
            "supporting_data": {
                "resource_preferences": resource_prefs,
                "learning_patterns": learning_patterns,
                "mastery_metrics": mastery_metrics
            }
        }
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _determine_preferred_resource_type(
        self, video_count: int, text_count: int, interactive_count: int,
        video_engagement: float, text_engagement: float
    ) -> str:
        """Determine which resource type user prefers"""
        if video_count > text_count and video_engagement > text_engagement:
            return "video"
        elif text_count > video_count and text_engagement > video_engagement:
            return "text"
        elif interactive_count > max(video_count, text_count):
            return "interactive"
        else:
            return "mixed"
    
    def _calculate_consistency(self, sessions: List[LearningSession]) -> float:
        """Calculate learning consistency (0.0 - 1.0)"""
        if len(sessions) < 2:
            return 0.5
        
        # Calculate variance in session timing
        dates = [s.started_at.date() for s in sessions]
        unique_dates = set(dates)
        
        # More unique dates = more consistent
        days_span = (max(dates) - min(dates)).days + 1
        consistency = len(unique_dates) / days_span if days_span > 0 else 0.5
        
        return min(1.0, consistency)
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Default preferences when no data available"""
        return {
            "video_count": 0,
            "text_count": 0,
            "interactive_count": 0,
            "total_resources": 0,
            "video_to_text_ratio": 1.0,
            "avg_video_completion": 0.0,
            "avg_text_completion": 0.0,
            "avg_interactive_completion": 0.0,
            "avg_video_engagement": 0.0,
            "avg_text_engagement": 0.0,
            "preferred_resource_type": "mixed"
        }
    
    def _get_default_learning_patterns(self) -> Dict[str, Any]:
        """Default learning patterns when no data available"""
        return {
            "total_sessions": 0,
            "avg_session_duration_minutes": 0,
            "total_learning_time_hours": 0,
            "preferred_learning_hours": [],
            "avg_focus_score": 0.5,
            "avg_completion_rate": 0.5,
            "frustration_events": 0,
            "unique_concepts_explored": 0,
            "concept_revisit_rate": 1.0,
            "learning_consistency": 0.5
        }
    
    def _get_default_mastery_metrics(self) -> Dict[str, Any]:
        """Default mastery metrics when no data available"""
        return {
            "total_concepts_tracked": 0,
            "mastery_distribution": {},
            "avg_learning_velocity": 0.5,
            "avg_retention_score": 0.5,
            "avg_time_per_concept_hours": 0,
            "concepts_mastered": 0,
            "concepts_in_progress": 0
        }


# Singleton instance
behavioral_analytics_service = BehavioralAnalyticsService()

