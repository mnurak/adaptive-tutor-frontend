"""
Intelligent Onboarding Service - Generates and processes cognitive questionnaires
"""
from typing import Dict, Any, List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enhanced_models import (
    OnboardingQuestionnaire, CognitiveProfile,
    InstructionFlow, InputPreference, EngagementStyle,
    ConceptTypePreference, LearningAutonomy, MotivationType,
    FeedbackPreference, ComplexityTolerance
)


# ============================================================================
# SCHEMAS
# ============================================================================

class QuestionnaireQuestion(BaseModel):
    """Represents a single questionnaire question"""
    id: str
    question_text: str
    question_type: str  # multiple_choice, scale, text
    options: List[str] = []
    cognitive_dimension: str  # which dimension this question measures
    weight: float = 1.0  # importance weight


class QuestionnaireResponse(BaseModel):
    """User's response to a questionnaire"""
    question_id: str
    answer: Any  # Can be string, int, list, etc.


class OnboardingSubmission(BaseModel):
    """Complete onboarding submission"""
    responses: List[QuestionnaireResponse]
    learning_goal: str
    available_hours_per_week: int
    preferred_session_duration: int


# ============================================================================
# ONBOARDING SERVICE
# ============================================================================

class OnboardingService:
    """
    Generates intelligent questionnaires and derives initial cognitive profiles
    """
    
    def __init__(self):
        self.questionnaire = self._build_questionnaire()
    
    def _build_questionnaire(self) -> List[QuestionnaireQuestion]:
        """Build the adaptive questionnaire"""
        return [
            # Input Preference Questions
            QuestionnaireQuestion(
                id="q1_learning_medium",
                question_text="When learning a new programming concept, which format helps you understand best?",
                question_type="multiple_choice",
                options=[
                    "Video tutorials with visual demonstrations",
                    "Written articles and documentation",
                    "Interactive coding exercises",
                    "A mix of all formats"
                ],
                cognitive_dimension="input_preference",
                weight=1.5
            ),
            QuestionnaireQuestion(
                id="q2_explanation_style",
                question_text="How do you prefer explanations to be presented?",
                question_type="multiple_choice",
                options=[
                    "Diagrams, flowcharts, and visual representations",
                    "Detailed written descriptions",
                    "Code examples with comments",
                    "Real-world analogies and stories"
                ],
                cognitive_dimension="input_preference",
                weight=1.2
            ),
            
            # Complexity Tolerance Questions
            QuestionnaireQuestion(
                id="q3_complexity_comfort",
                question_text="When faced with a complex topic, how do you typically feel?",
                question_type="multiple_choice",
                options=[
                    "Excited - I enjoy challenging material",
                    "Comfortable - I can handle it with some effort",
                    "Overwhelmed - I prefer simpler explanations first",
                    "It depends on the topic"
                ],
                cognitive_dimension="complexity_tolerance",
                weight=1.5
            ),
            QuestionnaireQuestion(
                id="q4_learning_pace",
                question_text="What learning pace works best for you?",
                question_type="multiple_choice",
                options=[
                    "Fast - I grasp concepts quickly",
                    "Moderate - I need time to understand thoroughly",
                    "Slow - I prefer to master each step before moving on",
                    "Variable - depends on the topic"
                ],
                cognitive_dimension="complexity_tolerance",
                weight=1.3
            ),
            
            # Engagement Style Questions
            QuestionnaireQuestion(
                id="q5_learning_activity",
                question_text="How do you learn most effectively?",
                question_type="multiple_choice",
                options=[
                    "By doing - hands-on practice and experimentation",
                    "By watching - observing examples and demonstrations",
                    "By reading - studying theory and documentation",
                    "By discussing - talking through concepts with others"
                ],
                cognitive_dimension="engagement_style",
                weight=1.5
            ),
            QuestionnaireQuestion(
                id="q6_practice_preference",
                question_text="After learning a new concept, what do you prefer to do?",
                question_type="multiple_choice",
                options=[
                    "Immediately try coding it myself",
                    "Review more examples first",
                    "Take notes and summarize",
                    "Move on to the next topic"
                ],
                cognitive_dimension="engagement_style",
                weight=1.2
            ),
            
            # Instruction Flow Questions
            QuestionnaireQuestion(
                id="q7_learning_path",
                question_text="How do you prefer to navigate learning materials?",
                question_type="multiple_choice",
                options=[
                    "Step-by-step in a structured order",
                    "Jump around based on my interests",
                    "Follow recommendations but explore side topics",
                    "No strong preference"
                ],
                cognitive_dimension="instruction_flow",
                weight=1.4
            ),
            
            # Learning Autonomy Questions
            QuestionnaireQuestion(
                id="q8_guidance_level",
                question_text="When learning, do you prefer:",
                question_type="multiple_choice",
                options=[
                    "Clear guidance and structured lessons",
                    "Freedom to explore on my own",
                    "A balance of both",
                    "It depends on my familiarity with the topic"
                ],
                cognitive_dimension="learning_autonomy",
                weight=1.3
            ),
            
            # Concept Type Preference Questions
            QuestionnaireQuestion(
                id="q9_concept_preference",
                question_text="Which type of content resonates with you more?",
                question_type="multiple_choice",
                options=[
                    "Concrete examples and practical applications",
                    "Abstract theories and underlying principles",
                    "Both equally",
                    "Depends on the context"
                ],
                cognitive_dimension="concept_type",
                weight=1.2
            ),
            
            # Feedback Preference Questions
            QuestionnaireQuestion(
                id="q10_feedback_timing",
                question_text="When practicing, how do you prefer to receive feedback?",
                question_type="multiple_choice",
                options=[
                    "Immediately after each attempt",
                    "After completing a section",
                    "Only when I ask for it",
                    "No strong preference"
                ],
                cognitive_dimension="feedback_preference",
                weight=1.1
            ),
            
            # Motivation Type Questions
            QuestionnaireQuestion(
                id="q11_motivation",
                question_text="What motivates you most to learn programming?",
                question_type="multiple_choice",
                options=[
                    "Personal curiosity and love of learning",
                    "Career goals and job requirements",
                    "Building specific projects",
                    "A combination of reasons"
                ],
                cognitive_dimension="motivation_type",
                weight=1.0
            ),
            
            # Experience Level
            QuestionnaireQuestion(
                id="q12_experience",
                question_text="What is your current programming experience level?",
                question_type="multiple_choice",
                options=[
                    "Complete beginner - no prior experience",
                    "Beginner - some basic knowledge",
                    "Intermediate - comfortable with fundamentals",
                    "Advanced - experienced programmer"
                ],
                cognitive_dimension="prior_experience",
                weight=1.5
            ),
        ]
    
    def get_questionnaire(self) -> List[QuestionnaireQuestion]:
        """Return the questionnaire for frontend"""
        return self.questionnaire
    
    async def process_onboarding(
        self,
        db: AsyncSession,
        user_id: str,
        submission: OnboardingSubmission
    ) -> CognitiveProfile:
        """
        Process onboarding responses and create initial cognitive profile
        """
        # Convert responses to dict for easy lookup
        response_map = {r.question_id: r.answer for r in submission.responses}
        
        # Derive cognitive dimensions
        profile_data = self._derive_cognitive_profile(response_map)
        
        # Create onboarding record
        onboarding = OnboardingQuestionnaire(
            user_id=user_id,
            preferred_learning_medium=self._extract_learning_medium(response_map),
            learning_pace=self._extract_learning_pace(response_map),
            prior_programming_experience=self._extract_experience(response_map),
            prefers_examples_or_theory=self._extract_concept_preference(response_map),
            prefers_step_by_step_or_overview=self._extract_flow_preference(response_map),
            comfort_with_complexity=self._extract_complexity_comfort(response_map),
            learning_goal=submission.learning_goal,
            available_hours_per_week=submission.available_hours_per_week,
            preferred_session_duration=submission.preferred_session_duration,
            raw_responses={q.question_id: q.answer for q in submission.responses},
            initial_cognitive_profile=profile_data
        )
        
        db.add(onboarding)
        await db.commit()
        
        # Create cognitive profile
        cognitive_profile = CognitiveProfile(
            user_id=user_id,
            **profile_data
        )
        
        return cognitive_profile
    
    def _derive_cognitive_profile(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Derive cognitive profile from questionnaire responses"""
        profile = {}
        
        # Input Preference
        q1 = responses.get("q1_learning_medium", "")
        q2 = responses.get("q2_explanation_style", "")
        
        if "Video" in q1 or "Diagrams" in q2:
            profile["input_preference"] = InputPreference.VISUAL
            profile["input_preference_confidence"] = 0.75
        elif "Written" in q1 or "written" in q2:
            profile["input_preference"] = InputPreference.VERBAL
            profile["input_preference_confidence"] = 0.75
        else:
            profile["input_preference"] = InputPreference.MIXED
            profile["input_preference_confidence"] = 0.6
        
        # Complexity Tolerance
        q3 = responses.get("q3_complexity_comfort", "")
        q4 = responses.get("q4_learning_pace", "")
        
        if "Excited" in q3 or "Fast" in q4:
            profile["complexity_tolerance"] = ComplexityTolerance.HIGH
            profile["complexity_tolerance_confidence"] = 0.8
        elif "Overwhelmed" in q3 or "Slow" in q4:
            profile["complexity_tolerance"] = ComplexityTolerance.LOW
            profile["complexity_tolerance_confidence"] = 0.8
        else:
            profile["complexity_tolerance"] = ComplexityTolerance.MEDIUM
            profile["complexity_tolerance_confidence"] = 0.7
        
        # Engagement Style
        q5 = responses.get("q5_learning_activity", "")
        q6 = responses.get("q6_practice_preference", "")
        
        if "doing" in q5 or "Immediately try" in q6:
            profile["engagement_style"] = EngagementStyle.ACTIVE
            profile["engagement_style_confidence"] = 0.8
        elif "watching" in q5 or "Review more" in q6:
            profile["engagement_style"] = EngagementStyle.PASSIVE
            profile["engagement_style_confidence"] = 0.75
        else:
            profile["engagement_style"] = EngagementStyle.MIXED
            profile["engagement_style_confidence"] = 0.65
        
        # Instruction Flow
        q7 = responses.get("q7_learning_path", "")
        
        if "Step-by-step" in q7:
            profile["instruction_flow"] = InstructionFlow.LINEAR
            profile["instruction_flow_confidence"] = 0.8
        elif "Jump around" in q7:
            profile["instruction_flow"] = InstructionFlow.EXPLORATORY
            profile["instruction_flow_confidence"] = 0.8
        else:
            profile["instruction_flow"] = InstructionFlow.MIXED
            profile["instruction_flow_confidence"] = 0.65
        
        # Learning Autonomy
        q8 = responses.get("q8_guidance_level", "")
        
        if "Clear guidance" in q8:
            profile["learning_autonomy"] = LearningAutonomy.GUIDED
            profile["learning_autonomy_confidence"] = 0.75
        elif "Freedom to explore" in q8:
            profile["learning_autonomy"] = LearningAutonomy.INDEPENDENT
            profile["learning_autonomy_confidence"] = 0.75
        else:
            profile["learning_autonomy"] = LearningAutonomy.MIXED
            profile["learning_autonomy_confidence"] = 0.6
        
        # Concept Type Preference
        q9 = responses.get("q9_concept_preference", "")
        
        if "Concrete" in q9:
            profile["concept_type"] = ConceptTypePreference.CONCRETE
            profile["concept_type_confidence"] = 0.75
        elif "Abstract" in q9:
            profile["concept_type"] = ConceptTypePreference.ABSTRACT
            profile["concept_type_confidence"] = 0.75
        else:
            profile["concept_type"] = ConceptTypePreference.MIXED
            profile["concept_type_confidence"] = 0.6
        
        # Feedback Preference
        q10 = responses.get("q10_feedback_timing", "")
        
        if "Immediately" in q10:
            profile["feedback_preference"] = FeedbackPreference.IMMEDIATE
            profile["feedback_preference_confidence"] = 0.7
        elif "After completing" in q10:
            profile["feedback_preference"] = FeedbackPreference.DELAYED
            profile["feedback_preference_confidence"] = 0.7
        else:
            profile["feedback_preference"] = FeedbackPreference.MIXED
            profile["feedback_preference_confidence"] = 0.6
        
        # Motivation Type
        q11 = responses.get("q11_motivation", "")
        
        if "curiosity" in q11:
            profile["motivation_type"] = MotivationType.INTRINSIC
            profile["motivation_type_confidence"] = 0.7
        elif "Career" in q11:
            profile["motivation_type"] = MotivationType.EXTRINSIC
            profile["motivation_type_confidence"] = 0.7
        else:
            profile["motivation_type"] = MotivationType.MIXED
            profile["motivation_type_confidence"] = 0.6
        
        return profile
    
    # Helper extraction methods
    def _extract_learning_medium(self, responses: Dict[str, Any]) -> str:
        answer = responses.get("q1_learning_medium", "")
        if "Video" in answer:
            return "video"
        elif "Written" in answer:
            return "text"
        elif "Interactive" in answer:
            return "interactive"
        return "mixed"
    
    def _extract_learning_pace(self, responses: Dict[str, Any]) -> str:
        answer = responses.get("q4_learning_pace", "")
        if "Fast" in answer:
            return "fast"
        elif "Slow" in answer:
            return "slow"
        return "moderate"
    
    def _extract_experience(self, responses: Dict[str, Any]) -> str:
        answer = responses.get("q12_experience", "")
        if "Complete beginner" in answer:
            return "none"
        elif "Beginner" in answer:
            return "beginner"
        elif "Intermediate" in answer:
            return "intermediate"
        return "advanced"
    
    def _extract_concept_preference(self, responses: Dict[str, Any]) -> str:
        answer = responses.get("q9_concept_preference", "")
        if "Concrete" in answer:
            return "examples"
        elif "Abstract" in answer:
            return "theory"
        return "both"
    
    def _extract_flow_preference(self, responses: Dict[str, Any]) -> str:
        answer = responses.get("q7_learning_path", "")
        if "Step-by-step" in answer:
            return "step_by_step"
        elif "Jump" in answer:
            return "overview"
        return "both"
    
    def _extract_complexity_comfort(self, responses: Dict[str, Any]) -> str:
        answer = responses.get("q3_complexity_comfort", "")
        if "Excited" in answer:
            return "high"
        elif "Overwhelmed" in answer:
            return "low"
        return "medium"


# Singleton instance
onboarding_service = OnboardingService()

