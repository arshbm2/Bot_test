from langchain_core.tools import tool
from core.database.sql_db_setup import get_sql_database
from pydantic import BaseModel, Field
import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os
from utils import clean_sql_query
from models import QueryAnalysis
load_dotenv()

# Initialize database connection
sql_database = get_sql_database()
import re

def process_sql_tool_call(tool_name, tool_input, user_input=None):
    """Process tool calls from the SQL agent."""
    if tool_name == "db_query_tool":
        return execute_db_query(tool_input.get("query", ""))
    else:
        return {"error": f"Unknown tool: {tool_name}"}

def execute_db_query(query: str) -> dict:
    """
    Execute a SQL query against the SQLite database and get back the result.
    """
    print("Query: ", query)
    with open("queries.txt", "a") as file:
        file.write("\n-----------------------------------------------------------------------\n")
        file.write("Query:\n")
        clean_query = clean_sql_query(query)
        file.write(clean_query)
        file.write("\n-----------------------------------------------------------------------\n")

    try:
        result = sql_database.run_no_throw(query, include_columns=True)    
        # Debug: print what we actually got from the database
        print(f"[DEBUG] Raw database result: {repr(result)}")
        print(f"[DEBUG] Result type: {type(result)}")
        
        # Only treat None as an error (syntax errors, table not found, etc.)
        if result is None:
            return {"error": "Query failed. Please rewrite your query and try again."}
            
        # Empty DataFrames with columns are VALID results, not errors
        # Handle different types of results
        if isinstance(result, str):
            # If it's already a string, use it directly
            final_result = result
        elif hasattr(result, 'to_string'):  # It's a pandas DataFrame
            # Convert DataFrame to string with headers
            final_result = result.to_string(index=False)
        elif hasattr(result, '__iter__') and not isinstance(result, str):
            # If it's a list/tuple/iterable, convert to string representation
            final_result = str(result)
        else:
            # For any other type, convert to string
            final_result = str(result)
            
        print(f"[DEBUG] Final processed result: {repr(final_result[:200])}")
        return {"result": final_result}
        
    except Exception as e:
        print(f"[DEBUG] Exception in execute_db_query: {str(e)}")
        return {"error": f"Query execution failed: {str(e)}"}
    

@tool
def db_query_tool(analysis: QueryAnalysis) -> str:
    """
    Execute a SQL query with analysis context.
    Takes a QueryAnalysis object with query, confidence, reasoning, and potential errors.
    """
    print(f"[DEBUG] Query Confidence: {analysis.confidence_score}")
    print(f"[DEBUG] Reasoning: {analysis.reasoning}")
    print(f"[DEBUG] Potential Errors: {analysis.potential_errors}")
    
    # Execute the query using existing method
    result = execute_db_query(analysis.sql_query)
    
    if "error" in result:
        return f"Error: {result['error']}"
    
    return result["result"]
