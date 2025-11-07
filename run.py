from graph import app
import time 
import logging
import pandas as pd

# Suppress debug output by setting logging level to WARNING
logging.getLogger().setLevel(logging.WARNING)

# Get the graph
graph = app.get_graph()

def extract_final_answer(messages):
    """Extract the final text answer from the agent's response"""
    try:
        # Get the messages list from the response
        message_list = messages.get("messages", [])
        
        # Find the last AIMessage with content (final answer)
        for message in reversed(message_list):
            if hasattr(message, 'content') and message.content.strip():
                return message.content.strip()
        
        # Fallback: if no content found, return a message
        return "No answer found in the response."
    except Exception as e:
        return f"Error extracting answer: {str(e)}"

inputs = {
    "messages": "what is the most amazing region?",
    "conversation": [
        # {
        #     "question": "what is sales?",
        #     "answer": "Could you clarify which specific type of sales you are interested in? For example, are you looking for gross sales, net sales, or sales broken down by payer type (Commercial, Medicare, Medicaid, Other)? Additionally, should this data be for a specific territory, account, or aggregated across all entities?"
        # },
   
    #     # {
    #     #     "question": "aggreate across all hcps quaterly.",
    #     #     "answer": "For which specific quarter would you like the aggregated call reach data?"
    #     # }
    ],
    "question":"How many HCPs received  a call for the first time in 2025 and also wrote a script in the same year for the first time?"
}

it_results = []

def get_output(app, inputs, it_results):

    for event in app.stream(inputs):
        node_name = list(event.keys())[0]         # e.g. "retrieve_and_process"
        state = event[node_name]   
        print(state.keys())   
        # if node_name == "retrieve_and_process":
        #     print(f"[Debug - AA] retrieve_and_process_tables node")
        #     print(f"[Debug - AA] Table metadata length: {state['table_metadata']}")
        #     print(f"[Debug - AA] Examples string length: {state['examples_str']}")
        if node_name == "iterative_execution":
            # print(f"[Debug - AA] Iterative execution node")
            # print(f"[Debug - AA] Node executed: {node_name}")
            # print(state["iteration_results"][0].sql_query)
            original_question = state["decomposition_plan"].original_question
            # print(f"original_question: {original_question};")
            # print(f"Length of iteration results: {len(state['iteration_results'])}")
            # # break
            
            subq_index = len(state["iteration_results"]) - 1
            sub_question = state["decomposition_plan"].sub_questions[subq_index].question
            sub_query = state["iteration_results"][subq_index].sql_query
            #current row for the final dataframe
            curr_row = {'Question': original_question,
                        'Sub Question Index': subq_index,
                        'Sub Question': sub_question,
                        'SQL Query': sub_query}
            it_results.append(curr_row)

    return it_results

it_results = get_output(app, inputs, it_results)
print(f"Debug - AA iteration results {it_results}")

test_questions = pd.read_excel("L3_questions.xlsx")['Question'].tolist()

# for i in range(len(test_questions)):
#     inputs = {
#         "messages": "",
#         "conversation": [],
#         "question":test_questions[i],
#     }
#     print(f"Processing question {i+1}/{len(test_questions)}: {test_questions[i]}")
#     try:
#         it_results = get_output(app, inputs, it_results)
#         time.sleep(1)  # brief pause between questions
#     except Exception as e:
#         row = {'Question': test_questions[i],
#                'Sub Question Index': -1,
#                'Sub Question': '',
#                'SQL Query': f"Error: {str(e)}"}
#         it_results.append(row)
#     # break

# it_results_df = pd.DataFrame(it_results)
# it_results_df.to_csv("iteration_results v4 test.csv", index=False)
# print("Saved iteration results to iteration_results v4.csv")