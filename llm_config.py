import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Configure OpenAI LLM
# openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o-2024-08-06", 
    temperature=0, 
    top_p=1, 
    openai_api_key=openai_api_key
)

eval_llm = ChatOpenAI(
    model="gpt-4o-2024-08-06", 
    temperature=0, 
    top_p=1, 
    openai_api_key=openai_api_key,
    timeout=30,  # 30 second timeout to prevent hanging
    max_retries=1  # Limit retries to prevent infinite loops
)

# eval_llm = ChatOpenAI(
#     model="o1-2024-12-17",     
#     top_p=1, 
#     openai_api_key=openai_api_key
# )

def test_llm():
    """
    Test function to verify the LLM is working properly.
    
    Returns:
        str: Response from the LLM
    """
    try:
        test_prompt = "Hello! Please respond with 'LLM is working correctly' to confirm the connection."
        response = llm.invoke(test_prompt)
        
        # Extract content from the response
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
            
    except Exception as e:
        return f"Error testing LLM: {str(e)}"


if __name__ == "__main__":
    # Test the LLM when running this file directly
    print("Testing LLM configuration...")
    result = test_llm()
    print(f"LLM Response: {result}")
    