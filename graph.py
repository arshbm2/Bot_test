from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from state import State
from base import (retrieve_and_process_tables, sql_query_generation_node, final_answer_node,
                   complexity_analysis_node, decomposition_node, iterative_query_execution_node, 
                   result_combination_node)
from tools import db_query_tool
from message_logger import SQLMessageLogger
from typing import Literal 
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize message logger
message_logger = SQLMessageLogger()

# Initialize the workflow
workflow = StateGraph(State)

# Create ToolNode only for db_query_tool
db_tool_node = ToolNode(tools=[db_query_tool])

# Add Nodes
workflow.add_node("retrieve_and_process", retrieve_and_process_tables)  # Initial data retrieval
workflow.add_node("analyze_complexity", complexity_analysis_node)  # Analyze question complexity
workflow.add_node("decomposition", decomposition_node)  # Break down complex questions
workflow.add_node("iterative_execution", iterative_query_execution_node)  # Execute sub-questions iteratively
workflow.add_node("result_combination", result_combination_node)  # Combine sub-query results
workflow.add_node("sql_query_generation", sql_query_generation_node)  # SQL query generation (direct approach)
workflow.add_node("execute_query", db_tool_node)  # DB query execution ToolNode
workflow.add_node("final_answer", final_answer_node)  # Final answer formatting and submission

# Define Edges
workflow.add_edge(START, "retrieve_and_process")  # Start to Retrieve
workflow.add_edge("retrieve_and_process", "analyze_complexity")  # Retrieve to Complexity Analysis

# Routing function for complexity analysis
def route_after_complexity_analysis(state: State):
    """Route after complexity analysis to determine approach"""
    use_iterative = state.get("use_iterative_approach", False)
    
    if use_iterative:
        logger.debug("Complex question detected, routing to decomposition")
        return "decomposition"
    else:
        logger.debug("Simple question detected, routing to direct SQL generation")
        return "sql_query_generation"

# Add conditional edge from complexity analysis
workflow.add_conditional_edges(
    "analyze_complexity",
    route_after_complexity_analysis,
    {
        "decomposition": "decomposition",
        "sql_query_generation": "sql_query_generation"
    }
)

# Edge from decomposition to iterative execution
workflow.add_edge("decomposition", "iterative_execution")

# Routing function for iterative execution
def route_after_iterative_execution(state: State):
    """Route after iterative execution to continue or combine results"""
    decomposition_plan = state.get("decomposition_plan")
    sub_question_index = state.get("sub_question_index", 0)
    current_iteration = state.get("current_iteration", 0)
    use_iterative_approach = state.get("use_iterative_approach", True)
    
    # Check if we fell back to direct approach
    if not use_iterative_approach:
        logger.debug("Fell back to direct approach, routing to SQL query generation")
        return "sql_query_generation"
    
    # Safety check: prevent infinite loops
    if current_iteration > 5:  # Reduced max iterations to 5
        logger.debug(f"Max iterations reached ({current_iteration}), routing to result combination")
        return "result_combination"
    
    if not decomposition_plan:
        logger.debug("No decomposition plan, routing to final answer")
        return "final_answer"
    
    # Check if all sub-questions are completed
    if sub_question_index >= len(decomposition_plan.sub_questions):
        logger.debug(f"All sub-questions completed (index: {sub_question_index}, total: {len(decomposition_plan.sub_questions)}), routing to result combination")
        return "result_combination"
    
    # Check if we have results for all sub-questions
    iteration_results = state.get("iteration_results", [])
    if len(iteration_results) >= len(decomposition_plan.sub_questions):
        logger.debug(f"All sub-questions have results ({len(iteration_results)}/{len(decomposition_plan.sub_questions)}), routing to result combination")
        return "result_combination"
    
    # Continue with next sub-question
    logger.debug(f"Processing sub-question {sub_question_index + 1} of {len(decomposition_plan.sub_questions)}, continuing iterative execution")
    return "iterative_execution"

# Add conditional edge from iterative execution
workflow.add_conditional_edges(
    "iterative_execution",
    route_after_iterative_execution,
    {
        "iterative_execution": "iterative_execution",
        "result_combination": "result_combination",
        "sql_query_generation": "sql_query_generation",
        "final_answer": "final_answer"
    }
)

# Edge from result combination to final answer
workflow.add_edge("result_combination", "final_answer")

# Custom routing function for sql_query_generation node
def route_query_gen_tools(state: State):
    """Route from query_gen to execute_query tool node based on tool calls"""
    
    # FIRST PRIORITY: Check if guidance is needed
    if state.get("needs_guidance", False):
        logger.debug(f"needs_guidance=True detected, routing to final_answer to terminate workflow")
        return "final_answer"
    
    messages = state["messages"]
    if not messages:
        return "final_answer"
    
    last_message = messages[-1]
    
    # First, check if we already have successful query results from previous executions
    has_successful_results = False
    last_successful_result = None
    
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            content_str = str(msg.content)
        
            # Check if result is successful: no errors AND has meaningful content
            if ("Error" not in content_str and 
                "Query failed" not in content_str and 
                content_str.strip() and 
                len(content_str.strip()) > 0):
                has_successful_results = True
                last_successful_result = content_str
                logger.debug(f"Found successful query results, content: {content_str[:100]}...")
                break
    
    if has_successful_results:
        logger.debug("Has successful results, routing directly to final_answer")
        return "final_answer"
    
    # Also check if the last message indicates successful execution
    if (hasattr(last_message, 'content') and 
        isinstance(last_message.content, str) and 
        "Query executed successfully" in last_message.content):
        logger.debug("Last message indicates successful execution, routing to final_answer")
        return "final_answer"
    
    # Only proceed with tool execution if we don't have successful results yet
    # Check if the last message has tool calls for db_query_tool
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        tool_call = last_message.tool_calls[0]
        if tool_call["name"] == "db_query_tool":
            # Count how many db_query_tool executions we've had
            db_tool_count = 0
            for msg in messages:
                if isinstance(msg, ToolMessage):
                    db_tool_count += 1
            
            # If we've already executed 2 or more queries, go to final answer regardless
            # This prevents infinite loops
            if db_tool_count >= 2:
                logger.debug(f"Already executed {db_tool_count} queries, forcing final answer")
                return "final_answer"
            
            return "execute_query"
    
    # If no tool calls and no successful results, also go to final answer to prevent loops
    logger.debug("No tool calls and no successful results, routing to final_answer")
    return "final_answer"

# Add conditional edges from sql_query_generation
workflow.add_conditional_edges(
    "sql_query_generation",
    route_query_gen_tools,
    {
        "execute_query": "execute_query",
        "final_answer": "final_answer"
    }
)

# After executing the db query, route to final answer to prevent loops
def should_continue_after_db_query(state: State) -> Literal["final_answer"]:
    messages = state["messages"]
    last_message = messages[-1]
    
    # Count the number of ToolMessages (database executions)
    tool_message_count = sum(1 for msg in messages if isinstance(msg, ToolMessage))
    
    logger.debug(f"Database query executed ({tool_message_count} total), routing to final answer")
    
    # Always route to final answer after database execution to prevent loops
    return "final_answer"

workflow.add_conditional_edges(
    "execute_query",
    should_continue_after_db_query,
    {
        "final_answer": "final_answer"
    }
)

# Final answer node handles both formatting and submission, then ends
workflow.add_edge("final_answer", END)

def log_messages_from_state(state: State, node_name: str) -> None:
    """Helper function to log messages from state."""
    messages = state["messages"]
    logger.debug(f"Processing messages in node: {node_name}")
    
    # Log the last LLM interaction if it exists
    if len(messages) >= 2:
        input_messages = [msg.dict() for msg in messages[:-1]]
        output = messages[-1].dict()
        message_logger.log_llm_interaction(input_messages, output)
    
    for msg in messages[-2:]:  # Log last 2 messages
        if isinstance(msg, HumanMessage):
            message_logger.log_user_message(msg.content)
        elif isinstance(msg, AIMessage):
            # Check if this is a tool-using message
            if hasattr(msg, 'additional_kwargs') and 'tool_calls' in msg.additional_kwargs:
                tool_calls = msg.additional_kwargs['tool_calls']
                for tool_call in tool_calls:
                    tool_use = {
                        "id": f"toolu_sql_{uuid.uuid4().hex[:24]}",
                        "name": tool_call.get('name', ''),
                        "input": tool_call.get('arguments', {})
                    }
                    message_logger.log_assistant_message(text=msg.content, tool_use=tool_use)
            else:
                message_logger.log_assistant_message(text=msg.content)
        elif isinstance(msg, ToolMessage):
            # Generate a unique ID for the tool use
            tool_id = f"toolu_sql_{uuid.uuid4().hex[:24]}"
            message_logger.log_tool_result(tool_id, msg.content)

# Compile the workflow
app = workflow.compile()

# # # Get the PNG content from the graph and save it
# png_data = app.get_graph().draw_mermaid_png()
# # Save the PNG content to a file
# with open('src/nodes/analytics_agent/analytics_architecture.png', 'wb') as file:
#     file.write(png_data)
