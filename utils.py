import re 


def read_last_query_from_file() -> str:
    """
    Read the last query from queries.txt file.
    Returns the most recent SQL query from the file, or empty string if none found.
    """
    try:
        with open("queries.txt", "r") as file:
            content = file.read()
        
        # Split by the separator line to get individual query blocks
        query_blocks = content.split("-----------------------------------------------------------------------")
        
        # Find the last non-empty query block
        for block in reversed(query_blocks):
            block = block.strip()
            if block and "Query:" in block:
                # Extract the query part (everything after "Query:")
                lines = block.split("\n")
                query_lines = []
                capture_query = False
                
                for line in lines:
                    if line.strip() == "Query:":
                        capture_query = True
                        continue
                    elif capture_query and line.strip():
                        query_lines.append(line)
                
                if query_lines:
                    return "\n".join(query_lines).strip()
        
        return ""
    except FileNotFoundError:
        print("[DEBUG] queries.txt file not found")
        return ""
    except Exception as e:
        print(f"[DEBUG] Error reading queries.txt: {str(e)}")
        return ""

def clean_sql_query(query: str) -> str:
    """
    Clean and normalize SQL query by removing extra whitespace, 
    comments, and formatting issues.
    """
    # Remove SQL comments (-- style)
    query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
    
    # Remove SQL comments (/* */ style)
    query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
    
    # Remove extra whitespace and normalize
    query = ' '.join(query.split())
    
    # Remove trailing semicolon if present
    query = query.rstrip(';')
    
    # Ensure query ends with semicolon
    if query and not query.endswith(';'):
        query += ';'
    
    return query.strip()


def extract_vector_tables(vector_search_results) -> list[str]:
    """
    Extract and clean table names from vector search results.
    
    Args:
        vector_search_results: List of documents from vector similarity search
        
    Returns:
        list[str]: List of clean table names
    """
    vector_tables = []
    for doc in vector_search_results:
        if 'table_name' in doc.metadata:
            table_name = doc.metadata['table_name']
            
            # Handle different formats of table names in metadata
            if isinstance(table_name, (list, tuple)):
                vector_tables.extend(table_name)
            elif isinstance(table_name, str):
                # If it's a comma-separated string, split it
                if ',' in table_name:
                    split_tables = [t.strip() for t in table_name.split(',')]
                    vector_tables.extend(split_tables)
                else:
                    vector_tables.append(table_name)
    
    return vector_tables


def clean_and_limit_tables(all_tables, max_tables=2) -> list[str]:
    """
    Clean, deduplicate and limit the number of table names.
    
    Args:
        all_tables: List of table names that may contain duplicates
        max_tables: Maximum number of tables to return (default: 2)
        
    Returns:
        list[str]: List of clean, unique table names limited to max_tables
    """
    unique_tables = []
    for table in all_tables:
        clean_table = str(table).strip()
        if clean_table and clean_table not in unique_tables:
            unique_tables.append(clean_table)

    # Limit to maximum specified number of tables to prevent token overflow
    return unique_tables[:max_tables]


def extract_examples_from_vector_search(vector_search_results) -> str:
    """
    Extract and format examples from vector search results.
    
    Args:
        vector_search_results: List of documents from vector similarity search
        
    Returns:
        str: Formatted examples string with questions and SQL queries
    """
    examples = []
    for doc in vector_search_results:
        if 'sql_query' in doc.metadata and 'table_name' in doc.metadata:
            examples.append((doc.page_content, doc.metadata['sql_query']))
    
    examples_str = "\n".join([
        f"Q: {q}\nSQL: {s}" for q, s in examples
    ])
    
    return examples_str


