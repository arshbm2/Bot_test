from src.langgraph.state import AgentState
# from src.nodes.sql_agent.agent import sql_chain_invoke
#from agent import sql_chain_invoke
from src.nodes.analytics_agent.graph import app
# from sql_langgraph import app
from langchain_core.messages import HumanMessage, AIMessage
import logging
import time
import re
from src.nodes.analytics_agent.utils import read_last_query_from_file
from src.nodes.analytics_agent.prompt import get_guidance_prompt
from src.nodes.analytics_agent.metadata import get_table_descriptions, get_additional_business_info
from src.core.utils.llm_config import llm
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)




def analytics_node(state: AgentState):
    duration = 0.0  # Initialize duration inside the function
    try:
        messages = []
        
        chat_history = state.conversation
        input_question = state.input
        last4_entries = chat_history[-4:] 
        
        print(f"[DEBUG] Analytics node received question: '{input_question}'")
        print(f"[DEBUG] State type: {type(state)}")
        print(f"[DEBUG] State.input field: '{state.input}'")
        print(f"[DEBUG] Question being passed to internal workflow: '{input_question}'")
        
        for chat in last4_entries:
            messages.append(HumanMessage(content=chat["question"]))
            messages.append(AIMessage(content=chat["answer"]))

        # Add the input question from the user
        messages.append(HumanMessage(content=input_question))
       
        start_time = time.time()
        
        # Prepare state for internal analytics workflow
        internal_state = {
            "messages": messages, 
            "conversation": chat_history,
            "question": input_question
        }
        
        print(f"[DEBUG] Calling internal analytics workflow with state: {list(internal_state.keys())}")
        thread = app.invoke(internal_state)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Time taken: {duration} seconds")
        
        # Check if messages exists and has items
        if "messages" in thread and thread["messages"]:
            print("Messages found, accessing tool_calls...")
            last_message = thread["messages"][-1]
            print(f"Last message type: {type(last_message)}")
            print(f"Last message has tool_calls: {hasattr(last_message, 'tool_calls') and last_message.tool_calls is not None}")
            
            # Check if tool_calls exists and is not empty
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                result = last_message.tool_calls[0]["args"]["final_answer"]
                print(f"[DEBUG] SQL_new_node - Extracted from tool_calls: {repr(result[:200])}")
            else:
                print("No tool_calls found in last message")
                # Remove the 'final_answer=' prefix if it exists
                content = last_message.content if hasattr(last_message, 'content') else "Error: No content available"
                print(f"[DEBUG] SQL_new_node - Raw content: {repr(str(content)[:200])}")
                
                if content.startswith("final_answer='"):
                    # Extract content between quotes
                    result = content[len("final_answer='"):-1]
                    print(f"[DEBUG] SQL_new_node - Extracted from prefix: {repr(result[:200])}")
                else:
                    result = content
                    print(f"[DEBUG] SQL_new_node - Using content directly: {repr(str(result)[:200])}")
        else:
            print("No messages found in thread result")
            result = "Error: No result available"
            
        print(f"[DEBUG] SQL_new_node - Final result type: {type(result)}")
        print(f"[DEBUG] SQL_new_node - Final result length: {len(str(result)) if result else 0}")
        print(f"[DEBUG] SQL_new_node - Final result content: {repr(str(result)[:300])}")
        
    except Exception as e:
        print("------------ERROR--------------------")
        print(f"Error executing workflow: {str(e)}")
        print("Exception type:", type(e).__name__)
        import traceback
        traceback.print_exc()
        print("--------------------------------")
        result = f"Error: {str(e)}"
        duration = 0.0  # Set duration to 0 in case of error
        thread = {}  # Initialize thread as empty dict to prevent UnboundLocalError
        
    query = read_last_query_from_file()
    print(f"Last Query Read: {query}")
    
    # Clean up queries.txt file
    try:
        import os
        if os.path.exists("queries.txt"):
            os.remove("queries.txt")
            print("[DEBUG] queries.txt file deleted successfully")
    except Exception as e:
        print(f"[DEBUG] Failed to delete queries.txt: {str(e)}")
    
    # Ensure clean state transfer to prevent any corruption issues
    if result is not None:
        # Force string conversion and clean any potential state issues
        result = str(result).strip()
        # Remove any potential control characters or encoding issues
        result = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', result)
    
    print(f"[DEBUG] SQL_new_node - Setting state.text_answer to: {repr(str(result)[:200])}")
    
    # Try to extract confidence information from the thread messages
    confidence_score = 1.0
    uncertainty_reason = ""
    needs_guidance = False
    
    print(f"[DEBUG] Thread keys: {list(thread.keys()) if isinstance(thread, dict) else 'Not a dict'}")
    
    # First, check if the internal workflow directly set needs_guidance
    if "needs_guidance" in thread and thread["needs_guidance"]:
        needs_guidance = True
        uncertainty_reason = thread.get("uncertainty_reason", "Internal workflow flagged need for guidance")
        confidence_score = thread.get("confidence_score", 0.3)
        print(f"[DEBUG] Internal workflow set needs_guidance=True, reason: {uncertainty_reason}")
    
    # Look for confidence information in the messages
    elif "messages" in thread and thread["messages"]:
        print(f"[DEBUG] Found {len(thread['messages'])} messages in thread")
        for i, message in enumerate(thread["messages"]):
            if hasattr(message, 'content') and message.content:
                content = str(message.content)
                print(f"[DEBUG] Message {i} content preview: {content[:100]}...")
                
                # Look for confidence score patterns
                if "Confidence Score:" in content:
                    try:
                        confidence_line = [line for line in content.split('\n') if 'Confidence Score:' in line][0]
                        confidence_score = float(confidence_line.split(':')[1].strip())
                        print(f"[DEBUG] Extracted confidence score: {confidence_score}")
                    except Exception as e:
                        print(f"[DEBUG] Failed to extract confidence score: {e}")
                
                # Look for reasoning patterns that might indicate uncertainty
                if ("uncertainty" in content.lower() or 
                    "unsure" in content.lower() or 
                    "unclear" in content.lower() or
                    "missing" in content.lower() or
                    confidence_score < 0.4):  # Updated threshold to match our implementation
                    needs_guidance = True
                    uncertainty_reason = f"Low confidence ({confidence_score}) or uncertain parameters detected"
                    print(f"[DEBUG] Detected uncertainty, needs_guidance: True, reason: {uncertainty_reason}")
    else:
        print("[DEBUG] No messages found in thread or thread is not properly structured")
        # If no messages, this might indicate an error condition
        if not result or "error" in str(result).lower():
            needs_guidance = True
            uncertainty_reason = "Analytics agent failed to process query properly"
    
    return {
        "sql_query": query,
        "execution_time": duration,
        "text_answer": result,
        "confidence_score": confidence_score,
        "uncertainty_reason": uncertainty_reason,
        "needs_guidance": needs_guidance
    }

