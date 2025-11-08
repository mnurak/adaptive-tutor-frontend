// Concept-to-Resource relationships
(c:Concept)-[:HAS_RESOURCE {
  resource_order: 1,
  recommended_for: ["visual", "beginner"],
  avg_time_spent_minutes: 12.5,
  completion_rate: 0.85
}]->(r:LearningResource)

// Student-specific learning paths
(s:Student)-[:CONSUMED_RESOURCE {
  started_at: datetime(),
  completed_at: datetime(),
  time_spent_seconds: 720,
  completion_percentage: 100,
  engagement_score: 4,
  notes: "Found helpful"
}]->(r:LearningResource)