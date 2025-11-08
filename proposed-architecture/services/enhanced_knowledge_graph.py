"""
Enhanced Neo4j Knowledge Graph Service with Multimedia Support
"""
from typing import List, Dict, Optional, Any
from neo4j import AsyncSession
from pydantic import BaseModel
from datetime import datetime


# ============================================================================
# SCHEMAS
# ============================================================================

class LearningResource(BaseModel):
    """Represents a learning resource (video, article, etc.)"""
    id: str
    resource_type: str  # video, article, interactive, code_example
    title: str
    url: str
    duration_minutes: Optional[int] = None
    thumbnail_url: Optional[str] = None
    difficulty_level: str = "beginner"
    engagement_score: float = 0.0
    completion_rate: float = 0.0
    learning_style: str  # visual, verbal, kinesthetic
    interaction_type: str = "passive"  # passive, active, interactive
    language: str = "en"
    description: Optional[str] = None
    tags: List[str] = []


class EnhancedConcept(BaseModel):
    """Enhanced concept with cognitive metadata"""
    id: str
    name: str
    type: str
    complexity: str
    estimated_hours: float
    cognitive_tags: List[str] = []
    learning_styles: List[str] = []
    description: Optional[str] = None
    prerequisites_count: int = 0
    subtopics_count: int = 0
    resources: List[LearningResource] = []


class PersonalizedLearningPath(BaseModel):
    """Personalized learning path for a student"""
    concept_name: str
    recommended_resources: List[LearningResource]
    estimated_time_minutes: int
    difficulty_match_score: float
    style_match_score: float
    next_concepts: List[str] = []


# ============================================================================
# ENHANCED KNOWLEDGE GRAPH SERVICE
# ============================================================================

class EnhancedKnowledgeGraphService:
    """
    Enhanced Neo4j service with multimedia support and personalized recommendations
    """
    
    def __init__(self):
        pass
    
    # ========================================================================
    # RESOURCE MANAGEMENT
    # ========================================================================
    
    async def create_learning_resource(
        self, 
        session: AsyncSession, 
        resource: LearningResource
    ) -> str:
        """Create a new learning resource in Neo4j"""
        query = """
        CREATE (r:LearningResource {
            id: $id,
            resource_type: $resource_type,
            title: $title,
            url: $url,
            duration_minutes: $duration_minutes,
            thumbnail_url: $thumbnail_url,
            difficulty_level: $difficulty_level,
            engagement_score: $engagement_score,
            completion_rate: $completion_rate,
            learning_style: $learning_style,
            interaction_type: $interaction_type,
            language: $language,
            description: $description,
            tags: $tags,
            created_at: datetime(),
            last_updated: datetime()
        })
        RETURN r.id as resource_id
        """
        
        result = await session.run(query, **resource.dict())
        record = await result.single()
        return record["resource_id"]
    
    async def link_resource_to_concept(
        self,
        session: AsyncSession,
        concept_name: str,
        resource_id: str,
        resource_order: int = 1,
        recommended_for: List[str] = None
    ) -> bool:
        """Link a learning resource to a concept"""
        query = """
        MATCH (c:Concept {name: $concept_name})
        MATCH (r:LearningResource {id: $resource_id})
        CREATE (c)-[:HAS_RESOURCE {
            resource_order: $resource_order,
            recommended_for: $recommended_for,
            created_at: datetime()
        }]->(r)
        RETURN c.name as concept, r.id as resource
        """
        
        result = await session.run(
            query,
            concept_name=concept_name,
            resource_id=resource_id,
            resource_order=resource_order,
            recommended_for=recommended_for or []
        )
        record = await result.single()
        return record is not None
    
    async def get_resources_for_concept(
        self,
        session: AsyncSession,
        concept_name: str,
        learning_style: Optional[str] = None,
        difficulty_level: Optional[str] = None
    ) -> List[LearningResource]:
        """Get all resources for a concept, optionally filtered by learning style"""
        query = """
        MATCH (c:Concept {name: $concept_name})-[rel:HAS_RESOURCE]->(r:LearningResource)
        WHERE ($learning_style IS NULL OR r.learning_style = $learning_style)
          AND ($difficulty_level IS NULL OR r.difficulty_level = $difficulty_level)
        RETURN r, rel.resource_order as order
        ORDER BY order, r.engagement_score DESC
        """
        
        result = await session.run(
            query,
            concept_name=concept_name,
            learning_style=learning_style,
            difficulty_level=difficulty_level
        )
        
        resources = []
        async for record in result:
            resource_data = dict(record["r"])
            resources.append(LearningResource(**resource_data))
        
        return resources
    
    # ========================================================================
    # PERSONALIZED RECOMMENDATIONS
    # ========================================================================
    
    async def get_personalized_learning_path(
        self,
        session: AsyncSession,
        concept_name: str,
        user_cognitive_profile: Dict[str, Any],
        user_mastery_data: Dict[str, Any]
    ) -> PersonalizedLearningPath:
        """
        Generate a personalized learning path based on cognitive profile
        """
        # Extract user preferences
        learning_style = user_cognitive_profile.get("input_preference", "mixed")
        complexity_tolerance = user_cognitive_profile.get("complexity_tolerance", "medium")
        
        # Map complexity tolerance to difficulty level
        difficulty_map = {
            "low": "beginner",
            "medium": "intermediate",
            "high": "advanced"
        }
        preferred_difficulty = difficulty_map.get(complexity_tolerance, "intermediate")
        
        # Get resources matching user's learning style
        query = """
        MATCH (c:Concept {name: $concept_name})-[rel:HAS_RESOURCE]->(r:LearningResource)
        
        // Calculate style match score
        WITH c, r, rel,
             CASE 
                 WHEN r.learning_style = $learning_style THEN 1.0
                 WHEN r.learning_style = 'mixed' THEN 0.7
                 ELSE 0.3
             END as style_score,
             CASE
                 WHEN r.difficulty_level = $preferred_difficulty THEN 1.0
                 WHEN r.difficulty_level = 'beginner' AND $preferred_difficulty = 'intermediate' THEN 0.7
                 WHEN r.difficulty_level = 'intermediate' AND $preferred_difficulty = 'advanced' THEN 0.7
                 ELSE 0.5
             END as difficulty_score
        
        // Calculate overall match score
        WITH c, r, rel, style_score, difficulty_score,
             (style_score * 0.6 + difficulty_score * 0.4 + r.engagement_score * 0.2) as match_score
        
        // Get next recommended concepts
        OPTIONAL MATCH (c)-[:PREREQUISITE_FOR]->(next:Concept)
        
        RETURN r, rel.resource_order as order, 
               style_score, difficulty_score, match_score,
               collect(DISTINCT next.name) as next_concepts,
               c.estimated_hours as estimated_hours
        ORDER BY match_score DESC, order ASC
        LIMIT 10
        """
        
        result = await session.run(
            query,
            concept_name=concept_name,
            learning_style=learning_style,
            preferred_difficulty=preferred_difficulty
        )
        
        resources = []
        next_concepts = []
        estimated_time = 0
        style_match = 0.0
        difficulty_match = 0.0
        
        async for record in result:
            resource_data = dict(record["r"])
            resources.append(LearningResource(**resource_data))
            
            if not next_concepts:
                next_concepts = record["next_concepts"] or []
                estimated_time = int((record["estimated_hours"] or 0) * 60)
            
            style_match = max(style_match, record["style_score"])
            difficulty_match = max(difficulty_match, record["difficulty_score"])
        
        return PersonalizedLearningPath(
            concept_name=concept_name,
            recommended_resources=resources,
            estimated_time_minutes=estimated_time,
            difficulty_match_score=difficulty_match,
            style_match_score=style_match,
            next_concepts=next_concepts
        )
    
    # ========================================================================
    # ANALYTICS & TRACKING
    # ========================================================================
    
    async def update_resource_engagement_metrics(
        self,
        session: AsyncSession,
        resource_id: str,
        completion_rate: float,
        engagement_score: float
    ) -> bool:
        """Update resource engagement metrics based on user interactions"""
        query = """
        MATCH (r:LearningResource {id: $resource_id})
        SET r.completion_rate = (r.completion_rate * 0.9 + $completion_rate * 0.1),
            r.engagement_score = (r.engagement_score * 0.9 + $engagement_score * 0.1),
            r.last_updated = datetime()
        RETURN r.id as resource_id
        """
        
        result = await session.run(
            query,
            resource_id=resource_id,
            completion_rate=completion_rate,
            engagement_score=engagement_score
        )
        record = await result.single()
        return record is not None
    
    async def get_resource_analytics(
        self,
        session: AsyncSession,
        resource_id: str
    ) -> Dict[str, Any]:
        """Get analytics for a specific resource"""
        query = """
        MATCH (r:LearningResource {id: $resource_id})
        OPTIONAL MATCH (c:Concept)-[:HAS_RESOURCE]->(r)
        RETURN r, c.name as concept_name
        """
        
        result = await session.run(query, resource_id=resource_id)
        record = await result.single()
        
        if not record:
            return {}
        
        resource_data = dict(record["r"])
        resource_data["concept_name"] = record["concept_name"]
        return resource_data
    
    # ========================================================================
    # ENHANCED CONCEPT RETRIEVAL
    # ========================================================================
    
    async def get_enhanced_concept_with_resources(
        self,
        session: AsyncSession,
        concept_name: str,
        learning_style: Optional[str] = None
    ) -> Optional[EnhancedConcept]:
        """Get concept with all its resources"""
        query = """
        MATCH (c:Concept {name: $concept_name})
        OPTIONAL MATCH (c)-[:HAS_RESOURCE]->(r:LearningResource)
        WHERE $learning_style IS NULL OR r.learning_style = $learning_style OR r.learning_style = 'mixed'
        OPTIONAL MATCH (c)<-[:PREREQUISITE_FOR]-(prereq:Concept)
        OPTIONAL MATCH (c)-[:HAS_SUBTOPIC]->(sub:Concept)
        
        WITH c, 
             collect(DISTINCT r) as resources,
             count(DISTINCT prereq) as prereq_count,
             count(DISTINCT sub) as subtopic_count
        
        RETURN c, resources, prereq_count, subtopic_count
        """
        
        result = await session.run(query, concept_name=concept_name, learning_style=learning_style)
        record = await result.single()
        
        if not record:
            return None
        
        concept_data = dict(record["c"])
        resources_data = [dict(r) for r in record["resources"] if r]
        
        return EnhancedConcept(
            id=concept_data.get("id", concept_name),
            name=concept_data["name"],
            type=concept_data.get("type", "unknown"),
            complexity=concept_data.get("complexity", "medium"),
            estimated_hours=concept_data.get("estimated_hours", 1.0),
            cognitive_tags=concept_data.get("cognitive_tags", []),
            learning_styles=concept_data.get("learning_styles", []),
            description=concept_data.get("description"),
            prerequisites_count=record["prereq_count"],
            subtopics_count=record["subtopic_count"],
            resources=[LearningResource(**r) for r in resources_data]
        )


# Singleton instance
enhanced_kg_service = EnhancedKnowledgeGraphService()

