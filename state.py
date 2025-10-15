from typing import Annotated, List, Optional
from typing_extensions import TypedDict,Dict
from langgraph.graph.message import AnyMessage, add_messages
from .models import DecompositionPlan, IterationResult, ComplexityAnalysis


# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    conversation: list[Dict[str, str]] = []
    question: str
    table_metadata: str  # Add this field to store table metadata
    examples_str: str    # Add this field to store example queries
    text_answer:str
    needs_guidance: bool = False  # Add field for guidance routing
    uncertainty_reason: str = ""  # Add field for uncertainty details
    confidence_score: float = 1.0  # Add field for confidence tracking
    
    # Iterative decomposition fields
    complexity_analysis: Optional[ComplexityAnalysis] = None  # Analysis of question complexity
    decomposition_plan: Optional[DecompositionPlan] = None  # Plan for breaking down the question
    iteration_results: List[IterationResult] = []  # Results from each iteration
    current_iteration: int = 0  # Current iteration number
    use_iterative_approach: bool = False  # Whether to use iterative decomposition
    sub_question_index: int = 0  # Current sub-question being processed
