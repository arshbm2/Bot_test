from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QueryAnalysis(BaseModel):
    """Simple structured output for SQL query generation"""
    
    sql_query: str = Field(description="The generated SQL query")
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0", ge=0.0, le=1.0)
    reasoning: str = Field(description="Brief reasoning for the query construction")
    potential_errors: list[str] = Field(description="List of potential issues with this query")
    needs_guidance: bool = Field(description="Whether guidance is needed due to unclear KPIs or terms", default=False)

class SubQuestion(BaseModel):
    """Represents a single sub-question in the decomposition"""
    
    question: str = Field(description="The sub-question text")
    purpose: str = Field(description="What this sub-question is trying to find out")
    dependencies: List[int] = Field(description="List of sub-question indices this depends on", default=[])
    sql_query: Optional[str] = Field(description="The SQL query for this sub-question", default=None)
    result: Optional[str] = Field(description="The result of executing this sub-question", default=None)
    confidence_score: float = Field(description="Confidence in this sub-question", ge=0.0, le=1.0, default=1.0)

class DecompositionPlan(BaseModel):
    """Plan for breaking down a complex question into sub-questions"""
    
    original_question: str = Field(description="The original complex question")
    sub_questions: List[SubQuestion] = Field(description="List of sub-questions to solve")
    execution_order: List[int] = Field(description="Order in which to execute sub-questions (by index)")
    complexity_reason: str = Field(description="Why this question requires decomposition")
    estimated_iterations: int = Field(description="Estimated number of iterations needed")

class IterationResult(BaseModel):
    """Result of executing one iteration of sub-questions"""
    
    iteration_number: int = Field(description="Which iteration this is")
    sub_question_index: int = Field(description="Which sub-question was executed")
    sql_query: str = Field(description="The SQL query that was executed")
    result: str = Field(description="The result from the database")
    success: bool = Field(description="Whether the query executed successfully")
    error_message: Optional[str] = Field(description="Error message if execution failed", default=None)
    confidence_score: float = Field(description="Confidence in this result", ge=0.0, le=1.0)

class ComplexityAnalysis(BaseModel):
    """Analysis of whether a question needs iterative decomposition"""
    
    needs_decomposition: bool = Field(description="Whether this question needs iterative decomposition")
    complexity_score: float = Field(description="Complexity score between 0.0 and 1.0", ge=0.0, le=1.0)
    complexity_reasons: List[str] = Field(description="Reasons why this is complex")
    suggested_approach: str = Field(description="Suggested approach: 'direct' or 'iterative'")
