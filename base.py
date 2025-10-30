from tools import db_query_tool, process_sql_tool_call
from state import State
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import uuid
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
import json
from llm_config import llm
# Commented out Langfuse imports - using local prompt functions instead
# from langfuse_setup import get_metadata, get_retreival_prompt, get_query_gen_prompt,get_final_answer_prompt,get_table_descriptions
from prompt import (get_query_gen_prompt, get_final_answer_prompt, get_table_retrieval_prompt,
                    get_complexity_analysis_prompt, get_decomposition_prompt, 
                    get_sub_question_query_prompt, get_result_combination_prompt)
from metadata import get_metadata, get_table_descriptions, get_additional_business_info
from models import QueryAnalysis, ComplexityAnalysis, DecompositionPlan, IterationResult, SubQuestion
from utils import extract_vector_tables, clean_and_limit_tables 
from dotenv import load_dotenv
load_dotenv()

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(embedding_function=embedding_function, persist_directory="./ChromaDB")


def get_similar_examples(query, chat_history, k=5):
    context = ""
    input_query = query.lower().strip().replace("\n", " ").replace("\t", " ")
    
    print(f"[DEBUG] get_similar_examples - Input query: '{query}'")
    print(f"[DEBUG] get_similar_examples - Processed query: '{input_query}'")
    
    for entry in chat_history[-5:]:  # Use the last 4 interactions for context
        entry['question']= entry['question'].lower().strip().replace("\n", " ").replace("\t", " ")
        entry['answer']= entry['answer'].lower().strip().replace("\n", " ").replace("\t", " ")
        context += f"{entry['question']} {entry['answer']} "
    context += f"{input_query}"
    
    # Preprocess the query with chat history
    # Perform similarity search
    examples = []
    conv_queries = db.similarity_search(context, k=k)
   
    for query in conv_queries:
        question_example = query.page_content
        sql_query_example = query.metadata.get('sql_query', "No SQL query available")
        examples.append((question_example, sql_query_example))
    queries = db.similarity_search_with_score(input_query, k=k)
   
    for query, score in queries:
        question_example = query.page_content
        sql_query_example = query.metadata.get('sql_query', "No SQL query available")
        examples.append((question_example, sql_query_example))
        
    
    # Format examples as a clean string
    examples_str = "\n\n".join([
        f"Question: {q}\nSQL Query:\n{s}" for q, s in examples
    ])
    
    print(f"[DEBUG] get_similar_examples - Found {len(examples)} examples")
    print(f"Formatted examples:\n{examples_str}")
    return examples_str

def get_relevant_tables_via_llm(history, question: str) -> list[str]:
    tables_description=get_table_descriptions()
    tables_info = "\n".join([f"- {name}: {desc}" for name, desc in tables_description.items()])
    
    retrieval_prompt = get_table_retrieval_prompt(tables_info, question, history)
    response= llm.invoke(retrieval_prompt)

    
    
    # More robust parsing of comma-separated values
    raw_tables = response.content.strip()
    
    # Split by comma and clean each table name
    table_candidates = []
    for table in raw_tables.split(","):
        clean_table = table.strip()
        # Remove any quotes or extra characters
        clean_table = clean_table.strip("\"'")
        if clean_table:
            table_candidates.append(clean_table)    
    
    # Filter to only valid table names
    valid_tables = [t for t in table_candidates if t in tables_description]
    
    
    return valid_tables

def retrieve_and_process_tables(state: State):
    print(f"[DEBUG] retrieve_and_process_tables - incoming messages count: {len(state.get('messages', []))}")
    for i, msg in enumerate(state.get('messages', [])):
        print(f"  Message {i}: {type(msg).__name__}")
    
    print(f"[DEBUG] retrieve_and_process_tables - state keys: {list(state.keys())}")
    print(f"[DEBUG] retrieve_and_process_tables - question from state: '{state.get('question', 'NOT FOUND')}'")
    
    history = "\n---\n".join([
        f"Q: {conv['question']}\nA: {conv.get('answer', '')}" 
        for conv in state.get("conversation", [])[-4:]
    ])    
    user_input=state["question"]
    
    print(f"[DEBUG] retrieve_and_process_tables - using question: '{user_input}'")


    llm_tables = get_relevant_tables_via_llm(history, user_input)
    vector_search_results = db.similarity_search(user_input, k=5)
    vector_tables = extract_vector_tables(vector_search_results)
    all_tables = llm_tables + vector_tables
    
    # Clean and deduplicate
    unique_tables = clean_and_limit_tables(all_tables)
    print(f"[DEBUG] Final unique tables: {unique_tables}")


    # Use the new get_metadata function instead of inline metadata creation
    metadata_section = get_metadata(unique_tables)
    examples_str=get_similar_examples(user_input, state.get("conversation", []), k=5)

    print(f"[DEBUG] retrieve_and_process_tables - metadata length: {len(metadata_section)}, examples length: {len(examples_str)}")
    
    return {
        "question": user_input,
        "table_metadata": metadata_section,
        "examples_str": examples_str
    }

def sql_query_generation_node(state: State):
    try:
        print(f"[DEBUG] sql_query_generation_node - incoming messages count: {len(state.get('messages', []))}")
        for i, msg in enumerate(state.get('messages', [])):
            print(f"  Message {i}: {type(msg).__name__}")
        
        # Get the most recent tool message if it exists (for retry scenarios)
        messages = state.get("messages", [])
        recent_tool_result = None
        
        for msg in reversed(messages):
            if isinstance(msg, ToolMessage):
                recent_tool_result = msg.content
                break
        
        # Format conversation history as clean, readable text
        conversation = state.get("conversation", [])
        print(f"[DEBUG] sql_query_generation_node - conversation: {conversation}")
        
        history_text = ""
        if conversation:    
            for i, chat in enumerate(conversation[-4:], 1):  # Last 4 conversations
                history_text += f"\nQ{i}: {chat['question']}\n"
                history_text += f"A{i}: {chat['answer']}\n"
        else:
            history_text = ""
        
        print(f"[DEBUG] sql_query_generation_node - history_text: {history_text}")
        
        # Use reconstructed question if available, otherwise use original
        question_to_use = state.get("question", "")
        if state.get("reconstructed_question"):
            question_to_use = state.get("reconstructed_question")
            print(f"[DEBUG] sql_query_generation_node - Using reconstructed question: '{question_to_use}'")
        else:
            print(f"[DEBUG] sql_query_generation_node - Using original question: '{question_to_use}'")
        
        inputs = {
            "question": question_to_use,
            "table_metadata": state.get("table_metadata", ""),
            "examples_str": state.get("examples_str", ""),
            "history": history_text,
            "additional_business_info": get_additional_business_info()
        }

        # Handle recent tool results
        if recent_tool_result:
            tool_result_str = str(recent_tool_result)
            print(f"[DEBUG] sql_query_generation_node - Processing tool result: {tool_result_str[:100]}...")
            
            # Check if the result is an error
            if "Error" in tool_result_str or "Query failed" in tool_result_str:
                print("[DEBUG] sql_query_generation_node - Tool result contains error, generating corrected query")
                inputs["question"] = f"{inputs['question']}\n\nPrevious query failed with error: {tool_result_str}\nPlease generate a corrected SQL query."
                inputs["additional_business_info"] = get_additional_business_info()
                
                # Generate corrected SQL query with structured output
                query_gen_prompt = get_query_gen_prompt(inputs)
                structured_llm = llm.with_structured_output(QueryAnalysis)
                structured_response = structured_llm.invoke(query_gen_prompt)
                
                # Extract the SQL query and create a tool call message
                sql_query = structured_response.sql_query
                print(f"[DEBUG] Generated SQL Query: {sql_query}")
                print(f"[DEBUG] Confidence Score: {structured_response.confidence_score}")
                print(f"[DEBUG] Reasoning: {structured_response.reasoning}")
                # Check if guidance is needed based on multiple criteria
                unclear_terms_in_errors = any("unclear" in error.lower() or "ambiguous" in error.lower() or "unknown" in error.lower() for error in structured_response.potential_errors)
                needs_guidance_explicit = getattr(structured_response, 'needs_guidance', False)
                
                if needs_guidance_explicit or structured_response.confidence_score < 0.4 or unclear_terms_in_errors:
                    # Route to guidance agent
                    error_details = "; ".join(structured_response.potential_errors) if structured_response.potential_errors else "low confidence in query interpretation"
                    uncertainty_reason = f"Query generation uncertainty: {error_details}. Confidence score: {structured_response.confidence_score}"
                    
                    print(f"[DEBUG] Routing to guidance agent - Needs Guidance: {needs_guidance_explicit}, Confidence: {structured_response.confidence_score}, Errors: {structured_response.potential_errors}")
                    
                    return {
                        "messages": [AIMessage(content=f"I need clarification on some terms in your question. Routing to guidance agent.")],
                        "needs_guidance": True,
                        "uncertainty_reason": uncertainty_reason,
                        "confidence_score": structured_response.confidence_score
                    }
                
                # Create AIMessage with manual tool call using the generated SQL
                
                tool_call_id = f"call_{uuid.uuid4().hex[:8]}"
                message = AIMessage(
                    content=f"I'll execute this SQL query: {sql_query}\n\nReasoning: {structured_response.reasoning}",
                    tool_calls=[{
                        "name": "db_query_tool",
                        "args": {"analysis": structured_response.dict()},
                        "id": tool_call_id
                    }]
                )
                return {"messages": [message]}
                
            elif tool_result_str.strip() and len(tool_result_str.strip()) > 0:
                print("[DEBUG] sql_query_generation_node - Tool result has data, proceeding to final answer node")
                # Don't format final answer here - let the final_answer_node handle it
                # Just return a message without tool binding to prevent further tool calls
                return {"messages": [AIMessage(content="Query executed successfully. Proceeding to format final answer.")]}
                
            else:
                print("[DEBUG] sql_query_generation_node - Tool result is empty, retrying with new query")
                inputs["question"] = f"{inputs['question']}\n\nPrevious query returned no results. Please try a different approach or check the data availability."
                inputs["additional_business_info"] = get_additional_business_info()
        
        # No tool result or need new query - generate SQL query with structured output
        print("[DEBUG] sql_query_generation_node - Generating new SQL query")
        query_gen_prompt = get_query_gen_prompt(inputs)
        structured_llm = llm.with_structured_output(QueryAnalysis)
        structured_response = structured_llm.invoke(query_gen_prompt)
        
        # Extract the SQL query and create a tool call message
        sql_query = structured_response.sql_query
        print(f"[DEBUG] Generated SQL Query: {sql_query}")
        print(f"[DEBUG] Confidence Score: {structured_response.confidence_score}")
        print(f"[DEBUG] Reasoning: {structured_response.reasoning}")
        if structured_response.potential_errors:
            print(f"[DEBUG] Potential Errors: {structured_response.potential_errors}")
        # Check if guidance is needed based on multiple criteria
        unclear_terms_in_errors = any("unclear" in error.lower() or "ambiguous" in error.lower() or "unknown" in error.lower() for error in structured_response.potential_errors)
        needs_guidance_explicit = getattr(structured_response, 'needs_guidance', False)
        
        if needs_guidance_explicit or structured_response.confidence_score < 0.4 or unclear_terms_in_errors:
            # Route to guidance agent
            error_details = "; ".join(structured_response.potential_errors) if structured_response.potential_errors else "low confidence in query interpretation"
            uncertainty_reason = f"Query generation uncertainty: {error_details}. Confidence score: {structured_response.confidence_score}"
            
            print(f"[DEBUG] Routing to guidance agent - Needs Guidance: {needs_guidance_explicit}, Confidence: {structured_response.confidence_score}, Errors: {structured_response.potential_errors}")
            
            return {
                "messages": [AIMessage(content=f"I need clarification on some terms in your question. Routing to guidance agent.")],
                "needs_guidance": True,
                "uncertainty_reason": uncertainty_reason,
                "confidence_score": structured_response.confidence_score
            }
        
        # Create AIMessage with manual tool call using the generated SQL
        
        tool_call_id = f"call_{uuid.uuid4().hex[:8]}"
        message = AIMessage(
            content=f"I'll execute this SQL query: {sql_query}\n\nReasoning: {structured_response.reasoning}",
            tool_calls=[{
                "name": "db_query_tool",
                "args": {"analysis": structured_response.dict()},
                "id": tool_call_id
            }]
        )
        return {"messages": [message]}

    except Exception as e:
        print(f"[DEBUG] sql_query_generation_node - ERROR: {str(e)}")
        return {"messages": [AIMessage(content=f"[Error in sql_query_generation_node] {str(e)}")]}



def complexity_analysis_node(state: State):
    """
    Analyzes question complexity to determine if iterative decomposition is needed.
    """
    try:
        print(f"[DEBUG] complexity_analysis_node - Analyzing question complexity")
        
        question = state.get("question", "")
        table_metadata = state.get("table_metadata", "")
        
        # Format conversation history
        conversation = state.get("conversation", [])
        history_text = ""
        if conversation:         
            for i, chat in enumerate(conversation[-4:], 1):  # Last 4 conversations
                history_text += f"\nQ{i}: {chat['question']}\n"
                history_text += f"A{i}: {chat['answer']}\n"
        
        inputs = {
            "question": question,
            "table_metadata": table_metadata,
            "history": history_text
        }
        
        # Get complexity analysis using structured output
        complexity_prompt = get_complexity_analysis_prompt(inputs)
        structured_llm = llm.with_structured_output(ComplexityAnalysis)
        complexity_analysis = structured_llm.invoke(complexity_prompt)
        
        print(f"[DEBUG] Complexity Analysis - Needs Decomposition: {complexity_analysis.needs_decomposition}")
        print(f"[DEBUG] Complexity Analysis - Complexity Score: {complexity_analysis.complexity_score}")
        print(f"[DEBUG] Complexity Analysis - Suggested Approach: {complexity_analysis.suggested_approach}")
        
        return {
            "complexity_analysis": complexity_analysis,
            "use_iterative_approach": complexity_analysis.needs_decomposition
        }
        
    except Exception as e:
        print(f"[DEBUG] complexity_analysis_node - ERROR: {str(e)}")
        # Default to direct approach on error
        return {
            "complexity_analysis": ComplexityAnalysis(
                needs_decomposition=False,
                complexity_score=0.5,
                complexity_reasons=["Error in analysis"],
                suggested_approach="direct"
            ),
            "use_iterative_approach": False
        }

def decomposition_node(state: State):
    """
    Breaks down complex questions into sub-questions using MAG-SQL decomposition approach.
    """
    try:
        print(f"[DEBUG] decomposition_node - Breaking down complex question using MAG-SQL approach")
        
        question = state.get("question", "")
        table_metadata = state.get("table_metadata", "")
        complexity_analysis = state.get("complexity_analysis")
        
        if not complexity_analysis or not complexity_analysis.needs_decomposition:
            print(f"[DEBUG] decomposition_node - No decomposition needed, skipping")
            return {}
        
        # Format conversation history
        conversation = state.get("conversation", [])
        history_text = ""
        if conversation:         
            for i, chat in enumerate(conversation[-4:], 1):  # Last 4 conversations
                history_text += f"\nQ{i}: {chat['question']}\n"
                history_text += f"A{i}: {chat['answer']}\n"
        
        inputs = {
            "question": question,
            "table_metadata": table_metadata,
            "history": history_text,
            "complexity_reasons": complexity_analysis.complexity_reasons
        }
        
        # Get decomposition using MAG-SQL approach (not structured output)
        decomposition_prompt = get_decomposition_prompt(inputs)
        response = llm.invoke(decomposition_prompt)
        decomposition_text = response.content
        
        print(f"[DEBUG] MAG-SQL Decomposition Response:")
        print(f"[DEBUG] {decomposition_text}")
        
        # return decomposition_text #Arsh's debug step
        # Parse MAG-SQL style decomposition response
        sub_questions = []
        execution_order = []
        
        # Extract sub-queries from the response using MAG-SQL pattern
        import re
        subquery_pattern = r"##Subquery:\s*(.+?)(?=##|$)"
        matches = re.findall(subquery_pattern, decomposition_text, re.DOTALL)
        
        for i, subquery_text in enumerate(matches):
            subquery_text = subquery_text.strip()
            if subquery_text:
                sub_question = SubQuestion(
                    question=subquery_text,
                    purpose=f"Sub-query {i+1} from MAG-SQL decomposition",
                    dependencies=[i-1] if i > 0 else [],
                    confidence_score=0.8
                )
                sub_questions.append(sub_question)
                execution_order.append(i)
        
        # If no sub-queries found, create a fallback
        if not sub_questions:
            sub_question = SubQuestion(
                question=question,
                purpose="Answer the original question directly",
                dependencies=[],
                confidence_score=0.5
            )
            sub_questions.append(sub_question)
            execution_order.append(0)
        
        # Create decomposition plan
        decomposition_plan = DecompositionPlan(
            original_question=question,
            sub_questions=sub_questions,
            execution_order=execution_order,
            complexity_reason="MAG-SQL decomposition approach",
            estimated_iterations=len(sub_questions)
        )
        
        print(f"[DEBUG] Parsed Decomposition Plan - Sub-questions: {len(decomposition_plan.sub_questions)}")
        print(f"[DEBUG] Parsed Decomposition Plan - Execution Order: {decomposition_plan.execution_order}")
        
        # Log each sub-question for better debugging
        for i, sub_q in enumerate(decomposition_plan.sub_questions):
            print(f"[DEBUG] Sub-question {i+1}: {sub_q.question}")
            print(f"[DEBUG] Sub-question {i+1} Purpose: {sub_q.purpose}")
            print(f"[DEBUG] Sub-question {i+1} Dependencies: {sub_q.dependencies}")
        
        return {
            "decomposition_plan": decomposition_plan,
            "current_iteration": 0,
            "sub_question_index": 0
        }
        
    except Exception as e:
        print(f"[DEBUG] decomposition_node - ERROR: {str(e)}")
        return {}

def iterative_query_execution_node(state: State):
    """
    Executes sub-questions iteratively, building upon previous results.
    """
    try:
        print(f"[DEBUG] iterative_query_execution_node - Executing sub-question")
        
        decomposition_plan = state.get("decomposition_plan")
        current_iteration = state.get("current_iteration", 0)
        sub_question_index = state.get("sub_question_index", 0)
        table_metadata = state.get("table_metadata", "")
        iteration_results = state.get("iteration_results", [])
        
        if not decomposition_plan or sub_question_index >= len(decomposition_plan.sub_questions):
            print(f"[DEBUG] iterative_query_execution_node - No more sub-questions to process")
            return {}
        
        # Get current sub-question
        current_sub_question = decomposition_plan.sub_questions[sub_question_index]
        
        # Format conversation history
        conversation = state.get("conversation", [])
        history_text = ""
        if conversation:         
            for i, chat in enumerate(conversation[-4:], 1):  # Last 4 conversations
                history_text += f"\nQ{i}: {chat['question']}\n"
                history_text += f"A{i}: {chat['answer']}\n"
        
        # Prepare previous SQL queries for context (not results)
        previous_sql_queries = ""
        for i, result in enumerate(iteration_results):
            previous_sql_queries += f"Sub-question {i+1} SQL: {result.sql_query}\n"
            previous_sql_queries += f"Sub-question {i+1} Result: {result.result}\n"
        
        # For progressive building, we need the most recent SQL query
        previous_sql = ""
        is_first_subquestion = True
        if iteration_results:
            previous_sql = iteration_results[-1].sql_query
            is_first_subquestion = False
        
        inputs = {
            "sub_question": current_sub_question.question,
            "purpose": current_sub_question.purpose,
            "table_metadata": table_metadata,
            "previous_results": previous_sql_queries,
            "previous_sql": previous_sql,
            "history": history_text
        }
        
        # Generate SQL query for this sub-question using MAG-SQL approach
        sub_question_prompt = get_sub_question_query_prompt(inputs)
        
        # Use regular LLM for MAG-SQL style query generation (not structured output)
        response = llm.invoke(sub_question_prompt)
        query_text = response.content
        
        print(f"[DEBUG] MAG-SQL Query Generation Response:")
        print(f"[DEBUG] {query_text}")
        
        # Extract SQL query from the response
        import re
        sql_match = re.search(r'```sql\s*(.*?)\s*```', query_text, re.DOTALL)
        if sql_match:
            sql_query = sql_match.group(1).strip()
        else:
            # Fallback: try to find SQL without code blocks
            sql_match = re.search(r'SELECT.*?(?=\n\n|\n$|$)', query_text, re.DOTALL | re.IGNORECASE)
            if sql_match:
                sql_query = sql_match.group(0).strip()
            else:
                sql_query = "SELECT 1"  # Fallback query
        
        # Create a mock QueryAnalysis object for compatibility
        query_analysis = QueryAnalysis(
            sql_query=sql_query,
            confidence_score=0.8,
            reasoning="Generated using MAG-SQL approach",
            potential_errors=[],
            needs_guidance=False
        )
        
        print(f"[DEBUG] Sub-question {sub_question_index + 1} - Question: {current_sub_question.question}")
        print(f"[DEBUG] Sub-question {sub_question_index + 1} - Purpose: {current_sub_question.purpose}")
        print(f"[DEBUG] Sub-question {sub_question_index + 1} - Previous SQL: {previous_sql}")
        print(f"[DEBUG] Sub-question {sub_question_index + 1} - Generated Query: {query_analysis.sql_query}")
        print(f"[DEBUG] Sub-question {sub_question_index + 1} - Confidence: {query_analysis.confidence_score}")
        print(f"[DEBUG] Sub-question {sub_question_index + 1} - Progressive Building: {'YES' if not is_first_subquestion else 'NO (First iteration)'}")
        
        # Execute the query with retry logic
        max_retries = 2
        retry_count = 0
        result = None
        
        while retry_count <= max_retries:
            try:
                from tools import execute_db_query
                result = execute_db_query(query_analysis.sql_query)
                print(f"[DEBUG] Query executed successfully (attempt {retry_count + 1}), result type: {type(result)}")
                if isinstance(result, dict) and "result" in result:
                    print(f"[DEBUG] Raw database result: {repr(result['result'])}")
                else:
                    print(f"[DEBUG] Raw database result: {repr(result)}")
                break  # Success, exit retry loop
            except Exception as e:
                retry_count += 1
                print(f"[DEBUG] Error executing query (attempt {retry_count}): {str(e)}")
                
                if retry_count > max_retries:
                    print(f"[DEBUG] Max retries reached, falling back to error result")
                    result = {"error": f"Query execution failed after {max_retries + 1} attempts: {str(e)}"}
                else:
                    print(f"[DEBUG] Retrying query generation...")
                    # Try to regenerate the query with error context
                    error_context = f"Previous query failed with error: {str(e)}. Please fix the SQL syntax and try again."
                    inputs["error_context"] = error_context
                    sub_question_prompt = get_sub_question_query_prompt(inputs)
                    response = llm.invoke(sub_question_prompt)
                    query_text = response.content
                    
                    # Extract SQL query from the response
                    import re
                    sql_match = re.search(r'```sql\s*(.*?)\s*```', query_text, re.DOTALL)
                    if sql_match:
                        query_analysis.sql_query = sql_match.group(1).strip()
                    else:
                        sql_match = re.search(r'SELECT.*?(?=\n\n|\n$|$)', query_text, re.DOTALL | re.IGNORECASE)
                        if sql_match:
                            query_analysis.sql_query = sql_match.group(0).strip()
                        else:
                            query_analysis.sql_query = "SELECT 1"  # Fallback query
                    
                    print(f"[DEBUG] Regenerated SQL: {query_analysis.sql_query}")
        
        # Process result for better handling
        if isinstance(result, dict):
            if "error" in result:
                processed_result = f"Error: {result['error']}"
                success = False
                error_message = result['error']
            else:
                processed_result = result.get("result", "")
                success = True
                error_message = None
        else:
            processed_result = str(result) if result else ""
            success = True
            error_message = None
        
        print(f"[DEBUG] Result type: {type(result)}")
        print(f"[DEBUG] Final processed result: {repr(processed_result)}")
        
        # Create iteration result
        iteration_result = IterationResult(
            iteration_number=current_iteration + 1,
            sub_question_index=sub_question_index,
            sql_query=query_analysis.sql_query,
            result=processed_result,
            success=success,
            error_message=error_message,
            confidence_score=query_analysis.confidence_score
        )
        
        # Update sub-question with result
        current_sub_question.sql_query = query_analysis.sql_query
        current_sub_question.result = iteration_result.result
        current_sub_question.confidence_score = query_analysis.confidence_score
        
        # Check if we should fallback to direct approach
        if not success and sub_question_index == 0:
            print(f"[DEBUG] First sub-question failed, falling back to direct approach")
            return {
                "use_iterative_approach": False,
                "iteration_results": [],
                "sub_question_index": 0,
                "current_iteration": 0
            }
        
        # Update state
        new_iteration_results = iteration_results + [iteration_result]
        next_sub_question_index = sub_question_index + 1
        
        print(f"[DEBUG] Sub-question {sub_question_index + 1} completed. Next index: {next_sub_question_index}")
        
        return {
            "iteration_results": new_iteration_results,
            "current_iteration": current_iteration + 1,
            "sub_question_index": next_sub_question_index,
            "decomposition_plan": decomposition_plan  # Update the plan with results
        }
        
    except Exception as e:
        print(f"[DEBUG] iterative_query_execution_node - ERROR: {str(e)}")
        return {}

def result_combination_node(state: State):
    """
    Combines results from all sub-queries into a final comprehensive answer.
    """
    try:
        print(f"[DEBUG] result_combination_node - Combining results")
        
        decomposition_plan = state.get("decomposition_plan")
        iteration_results = state.get("iteration_results", [])
        
        if not decomposition_plan or not iteration_results:
            print(f"[DEBUG] result_combination_node - No results to combine")
            return {}
        
        # Format conversation history
        conversation = state.get("conversation", [])
        history_text = ""
        if conversation:         
            for i, chat in enumerate(conversation[-4:], 1):  # Last 4 conversations
                history_text += f"\nQ{i}: {chat['question']}\n"
                history_text += f"A{i}: {chat['answer']}\n"
        
        # Format sub-questions and results for the prompt
        sub_questions_text = ""
        for i, sub_q in enumerate(decomposition_plan.sub_questions):
            sub_questions_text += f"Sub-question {i+1}: {sub_q.question}\n"
            sub_questions_text += f"Purpose: {sub_q.purpose}\n"
            sub_questions_text += f"Result: {sub_q.result}\n\n"
        
        iteration_results_text = ""
        for result in iteration_results:
            iteration_results_text += f"Iteration {result.iteration_number}: {result.result}\n"
        
        inputs = {
            "original_question": decomposition_plan.original_question,
            "sub_questions": sub_questions_text,
            "iteration_results": iteration_results_text,
            "history": history_text
        }
        
        # Generate combined final answer
        combination_prompt = get_result_combination_prompt(inputs)
        message = llm.invoke(combination_prompt)
        final_answer = message.content if hasattr(message, 'content') else str(message)
        
        print(f"[DEBUG] result_combination_node - Generated final answer")
        
        return {
            "messages": [AIMessage(content=final_answer)],
            "text_answer": final_answer
        }
        
    except Exception as e:
        print(f"[DEBUG] result_combination_node - ERROR: {str(e)}")
        return {"messages": [AIMessage(content="I apologize, but I encountered an error while combining the results. Please try again.")]}

def final_answer_node(state: State):
    try:
        # FIRST: Check if guidance is needed - if so, return minimal response
        if state.get("needs_guidance", False):
            print(f"[DEBUG] final_answer_node - Guidance needed, returning early")
            return {
                "text_answer": "Guidance needed - routing to guidance agent",
                "needs_guidance": True,
                "uncertainty_reason": state.get("uncertainty_reason", "Unclear terms detected"),
                "confidence_score": state.get("confidence_score", 0.3)
            }
        
        messages = state.get("messages", [])
        original_question = state.get("question", "")
        
        # Find the most recent successful query results
        query_results = ""
        
        for msg in reversed(messages):
            if isinstance(msg, ToolMessage):
                content_str = str(msg.content)
                # Skip error messages, use successful results
                if "Error" not in content_str and "Query failed" not in content_str and content_str.strip():
                    query_results = content_str
                    break
                    
            elif isinstance(msg, HumanMessage) and isinstance(msg.content, list):
                # Handle structured content from tool results
                for item in msg.content:
                    if isinstance(item, dict) and "content" in item:
                        try:
                            import json
                            parsed_content = json.loads(item["content"])
                            if "result" in parsed_content and parsed_content["result"].strip():
                                query_results = parsed_content["result"]
                                break
                        except:
                            continue
                if query_results:
                    break
        
        history_text = ""
        conversation = state.get("conversation", [])
        if conversation:         
            for i, chat in enumerate(conversation[-4:], 1):  # Last 4 conversations
                history_text += f"\nQ{i}: {chat['question']}\n"
                history_text += f"A{i}: {chat['answer']}\n"
        else:
            history_text = ""
        # Format the final answer
        # Use reconstructed question if available for better context
        question_to_use = original_question
        if state.get("reconstructed_question"):
            question_to_use = state.get("reconstructed_question")
            print(f"[DEBUG] final_answer_node - Using reconstructed question: '{question_to_use}'")
        else:
            print(f"[DEBUG] final_answer_node - Using original question: '{question_to_use}'")
        
        inputs = {
            "question": question_to_use,
            "history": history_text,
            "query_results": query_results
        }
        
        final_prompt = get_final_answer_prompt(inputs)
        message = llm.invoke(final_prompt)
        final_answer = message.content if hasattr(message, 'content') else str(message)
        
        return {"messages": [AIMessage(content=final_answer)]}
        
    except Exception as e:
        return {"messages": [AIMessage(content="I apologize, but I encountered an error while formatting the response. Please try again.")]}