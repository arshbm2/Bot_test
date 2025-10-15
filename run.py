from src.nodes.analytics_agent.graph import app
import time 
import logging

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
    "question":"what is the most amazing region?",
}

print("Processing your query...")
print("=" * 50)

start = time.time()
messages = app.invoke(inputs)
end = time.time()

# Extract and print the clean answer
final_answer = extract_final_answer(messages)
print(final_answer)

print("=" * 50)
print(f"Execution time: {end-start:.2f} seconds")

