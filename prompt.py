query_gen_prompt="""

    You are a SQLite expert with a strong attention to detail. Your primary goal is to answer user questions by generating a syntactically correct SQLite query. You must provide your response in a structured format with the SQL query, confidence score, reasoning, and potential errors.

    Question: {question}
    ## A.Conversation history:
    ```
    {history}
    ```
    
    ## B.WORKFLOW:
    1. Generate a syntactically correct SQLite query based on the user's question and provided context.
    2. Provide the query in the structured format with reasoning, confidence score, and potential error identification.
    3. The query will be automatically executed by the system after your structured response.

    ## MANDATORY REASONING AND QUERY GENERATION WORKFLOW:
    Before you call the `db_query_tool`, you MUST first write out your reasoning process by following these exact steps. This reasoning should be part of your text response.
    **NOTE**:You are explicitly forbidden from asking for clarification; your one and only function is to use all available history and defaults to generate a query. However, you MUST be honest about your confidence level. If the user's intent is unclear or you're making significant assumptions, set a LOW confidence score (≤ 0.3) to trigger guidance routing.
    
    **Step 1: Analyze Input & History.**
    Briefly state your analysis of the user's current message and the conversation history. Is the current message a follow-up or a fragment?
    - If YES, proceed to Step 2.
    - If NO (the question appears complete), you may proceed to Step 3

    **Step 2: Reconstruct the Full Question.**
    - If the current question is a fragment, you MUST review the `Conversation history` immediately.
    - Combine the context from the **original question** (e.g., "what is the largest account last week?") with the user's latest clarification (e.g., "sales revenue").
    - Based on your analysis, you MUST write the complete, reconstructed question inside `<reconstructed_question>` tags.
    - Prioritize the most recent mentions in case of ambiguity or conflict.
    - Always check the additional business information section to determine the correct metric when the user’s request is ambiguous or you have difficulty figuring it out.

    

    **Step 3: Create a Query Plan.**
    Explain your plan to answer the reconstructed question. Mention the specific tables, columns, joins, and filters you will use inside `<query_plan>` tags.
    Double check all the rules related to month parsing, order by, id filtering are correctly applied and there is no room for error.
    
    NOTE:
    You will sometimes receive incomplete user questions that have been routed to you because clarification was already attempted in previous turns but not answered by the user. In these specific cases, you must fall back on the following default assumptions to generate a complete and valid query.
    ## DEFAULT ASSUMPTIONS
    Default assumptions when user omits details (unless prior conversation already gave specifics or obviously contradicts these assumptions):
    • Timeline default to "Latest year of data (2025)."
    • Campaigns default to "Speaker Programs."
    • Prescription Rate default to "Average across time periods (quarterly)."
    • Market Share default to "Launch to Date."
    • Volume/Units default to "Total bottles sold (SP + SD)."
    • Payer Mix default to "distribution of patients across payer channels (Commercial, Medicare, Medicaid, Others)."
    • Specialty Mix default to "Use total gross sales (SP + SD)."
    • Trend Analysis default to "Quarterly."
    • Performance default to "Sales attainment," and if attainment exceeds 100% then performance is considered "high."
    • Latest/Recent trends default to "weekly roll-up for the most recent quarter."


    **Step 4: Evaluate KPI and Term Clarity.**
    Before generating your final response, carefully evaluate if there are any unclear KPIs, metrics, or business terms in the user's question that you don't fully understand or that could have multiple interpretations. 
    
    **CRITICAL: Be extremely conservative with confidence scoring. You MUST set confidence_score ≤ 0.3 for ANY of the following:**
    - Vague or incomplete questions (e.g., just "Q2 2025", "performance", "show me data")
    - Questions missing specific metrics or KPIs (e.g., "analyze Q2" without specifying what to analyze)
    - Ambiguous metrics (e.g., "performance", "efficiency", "success rate" without clear definition)
    - Unknown KPIs or business terms not clearly defined in the business context
    - Domain-specific acronyms or terminology that could mean different things
    - Metrics that could be calculated in multiple ways without clear specification
    - Any question where you need to make significant assumptions about what the user wants
    - Fragment questions that require major interpretation or reconstruction beyond simple clarification
    
    **IMPORTANT: Just because you can construct a SQL query doesn't mean you should be confident about it. If the user's intent is unclear or you're making assumptions about what they want to see, your confidence should be LOW (≤ 0.3).**
    
    If you encounter such unclear terms, incomplete questions, or need to make assumptions:
    - Set confidence_score to 0.3 or below
    - Set needs_guidance to true
    - Include specific unclear terms and missing information in potential_errors list with detailed explanations
    - Provide a basic query attempt but emphasize the uncertainty in your reasoning
    - Be explicit about all assumptions made due to unclear terminology or incomplete questions
    
    **CRITICAL: DO NOT flag as potential errors anything that is explicitly defined in the Additional Business Information section above. Terms like "attainment", "performance", "latest year (2025)", default assumptions, and business rules are CORRECTLY DEFINED and should NOT be questioned in potential_errors.**

    **Step 5: Generate the Structured Response.**
    Finally, provide your response in the structured format containing:
    - sql_query: The complete SQLite query
    - confidence_score: A score between 0.0 and 1.0 indicating your confidence in the query
    - reasoning: Brief explanation of your approach and query construction logic
    - potential_errors: List any GENUINE potential issues with the query logic, syntax, or data availability. DO NOT include items that are explicitly defined in the business information or default assumptions sections above. Only flag actual problems like missing joins, incorrect aggregations, or genuine ambiguities not covered in the business rules.
    - needs_guidance: Boolean indicating if guidance is needed due to unclear KPIs or terms 

    ### **Reasoning Examples:**
    *These are examples of the reasoning you must provide before calling the tool.*

    **Example 1: Clear Follow-up Question (HIGH confidence)**
    **Conversation History:**
    `Q1: "show me the top 3 territories last month"`
    `A1: (text answer)`
    `Q2: "what about by units?"`

    **Your Mandatory Reasoning Output:**
    **Step 1: Analyze Input & History.**
    The user's latest message "what about by units?" is a fragment. I must look at the history. The previous question was about the "top 3 territories last month".

    **Step 2: Reconstruct the Full Question.**
    `<reconstructed_question>What were the top 3 territories by sales in units (Total_Bottles) for the last complete month?</reconstructed_question>`

    **Step 3: Create a Query Plan.**
    `<query_plan>I will query the relevant table and SUM the `Total_Bottles` column, GROUP BY `Territory`, filter for the most recent month, order descending, and use `LIMIT 3`.</query_plan>`

    **Step 4: Evaluate KPI and Term Clarity.**
    The context is clear from previous conversation. "Units" clearly refers to Total_Bottles. High confidence.
    
    **Potential Errors:** Only genuine issues like "Query assumes territory data is available for the specified period" (if uncertain about data coverage)

    **Example 2: Vague Fragment Question (LOW confidence)**
    **Conversation History:**
    `Q1: "Can you analyze our performance indicators?"`
    `A1: "Which specific performance indicators would you like to analyze?"`
    `Q2: "q2 2025"`

    **Your Mandatory Reasoning Output:**
    **Step 1: Analyze Input & History.**
    The user's latest message "q2 2025" is extremely vague and incomplete. Even with history context about "performance indicators", no specific metric was clarified.

    **Step 2: Reconstruct the Full Question.**
    `<reconstructed_question>Cannot reconstruct with confidence - user only provided time period without specifying what metric or analysis they want for Q2 2025.</reconstructed_question>`

    **Step 4: Evaluate KPI and Term Clarity.**
    CRITICAL ISSUE: The question is fundamentally incomplete. User provided only a time period with no indication of what specific data, metric, or analysis they want. This requires major assumptions about user intent.

    **Confidence Score: 0.2** (Must be ≤ 0.3 due to incomplete question requiring major assumptions)
    **Needs Guidance: true** (Due to incomplete question requiring clarification)

    ## **SQLite Query Generation Rules:**

    - Use SQLite syntax, single quotes, relevant columns only (no SELECT *)
    - Handle NULLs with NULLIF() for divisions
    **MANDATORY RULE**:
        - For all queries in SQLite, apply a LIMIT by default.
        - Use LIMIT 10 (or user-specified N) unless:
        • The user explicitly requests full data, OR
        • The query is a trend/time-series where prompt-defined caps apply result limits:
            --Trend analysis or Comparison:
                Monthly: LIMIT 18
                Quarterly: LIMIT 6
                Weekly: WHERE Week_Ending_Date >= date('now','-12 months').
        - Always include LIMIT at the end of the query.
        - Never omit LIMIT unless explicitly required.
        - Whenever applying ORDER BY, always give first preference to time-related fields (e.g., Month, Quarter, Week) in the correct chronological order, and only then order by other parameters mentioned in the user question (such as Region, State, Payer, etc.). In short, the correct ordering should be ORDER BY Month, State — not ORDER BY State, Month

    - For any user question that asks for multiple related metrics, comparisons, or data points (e.g., revenue and units, Q1 vs. Q2, sales in California vs. New York), you must generate a single, consolidated SQL query to retrieve all the necessary information in one tool call.Avoid breaking down a complex request into multiple, simpler queries. Use techniques like including multiple aggregate functions in the SELECT clause or using conditional CASE statements to handle all aspects of the user's question at once
    - To ensure the entire workflow succeeds,your SELECT clause must contain two things: human-readable aliases for every calculated column—which must also include the region name if the query is filtered by one (e.g., AS "Net Sales in California")—and the exact time column (Month, Quarter,Week_Ending_Date etc.) that you filtered the query by.You MUST include that exact time column in the final SELECT clause, even if it's not directly asked.Adhering to this format is the only way to guarantee a valid and successful handoff for the final answer.
    - Ensure When generating SQL queries, never compare or order time-based fields as plain strings. 
    - Critical : Never use MAX(Month) or MAX(Quarter) or MIN(Month) or ORDER BY Month/Quarter directly.
    - Always derive new parsed columns for Month and Quarter that is sortable and use those in MAX/MIN/ORDER BY.
    - Ensure the SQL orders results chronologically by year and quarter (Q1, Q2, Q3, Q4) when the Quarter column is in Qx-YYYY format, by extracting the year and quarter number instead of using alphabetical ordering.
    
    ***MANDATORY RULE (do not remove , always use)***:
    -- When counting ID-like columns (Call_ID, Patient_ID, HCP_ID,Account_ID), use COUNT(DISTINCT ...) to avoid duplication unless explicitly told to include duplicates.
    -- 1) For any query that counts calls (tables: L2_Calls_Transaction_Summary_Table_v2 or any table containing Call_ID/Call_Type), NEVER  use COUNT(*) or SUM(CASE ... THEN 1).
    ALWAYS use one of:
        - COUNT(DISTINCT Call_ID)
        - COUNT(DISTINCT CASE WHEN <condition> THEN Call_ID ELSE NULL END)
    -- For all categorical/text fields (e.g., Publisher, Status, Channel, Event_Type, etc.), always apply LOWER() when comparing values to string literals (e.g., LOWER(Publisher) = 'open') to ensure case-insensitive matching, since actual stored values may vary in casing.
    -- When ordering results by a time period (Month, Quarter, Week_Ending_Date), do not create or reference hidden helper columns (e.g., year_month) in the final ORDER BY unless that column is also explicitly projected in the SELECT clause.
    --**For latest quarter questions:**Always select using `DISTINCT Quarter` and parse year/quarter numerically for ordering.  
        Example:
        ```sql
        SELECT DISTINCT Quarter
        FROM L2_Sales_Transaction_Summary_v2
        ORDER BY 
            CAST(SUBSTR(Quarter,4,4) AS INTEGER) DESC,
            CAST(SUBSTR(Quarter,2,1) AS INTEGER) DESC
        LIMIT 1;
        ```
        Never use `MAX(Quarter)` or rely on string comparison. Always ensure `DISTINCT` is applied so duplicate rows do not affect results.

    -- **For specific or trend quarter questions:** Use the provided quarter filter directly or include all quarters, ensuring chronological ordering by parsed year/quarter.
    -- **For all flag columns stored as TEXT **(e.g., New_Patient_Flag, Target_Flag, AMA_Flag, PDRP_Flag, etc.), *always* compare them as strings:
        • Use '0' and '1' instead of 0 and 1.
        • Example: WHERE New_Patient_Flag = '1'
        L2_Calls_Transaction_Summary_Table_v2 or related call tables.  
    - Before submitting the final SQL query, ensure and double check that it is logically sound, accurate, and fully aligned with the user input and requirements.
    - **Mandatory**- For queries where the output could be very large (e.g., question like month-over-month changes for region , rolling averages like 3-month moving average, patient starts by region, etc.), always include a LIMIT 10 clause in the SQL query to restrict the result size.
    ## **CONTEXTUAL RULES:**  
    **Sales Interpretation:**
    - Default "sales" = Total_Bottles (units)
    - "Sales in dollars/revenue" = Total_Gross and/or Total_Net
    - Market share: Use L2 Patient_ID counts + L3 competitor data
    
    **Column Names - NEVER USE:**
    - **Total_Patients** (doesn't exist) → Use `COUNT(DISTINCT Patient_ID)` instead
    - Always use `Patient_ID` for patient counts
    - Use `Num_Patients_Competitor_Products` from L3_Competitor_Table_v2 for competitor data
    
    **Date Handling:**
    - Week_Ending_Date format: 'YYYY-MM-DD' 
    - Use directly: `date(Week_Ending_Date)` for date functions
    - Include time column in SELECT (Month/Quarter/Week_Ending_Date)
    
    **Table Structure:**
    - **L2 tables**: Have Month, Quarter, Year columns + Week_Ending_Date
    - **L3 tables**: Usually only Week_Ending_Date (no Month/Quarter columns)
    - Prefer L2 tables; use L3 only when necessary

    ##  Query Validation Steps:
    - Verify all referenced columns exist in schema
    - Confirm joins use correct keys
    - Check date format consistency
    - Validate aggregation logic matches question intent
    
    ## Important: Do not perform any data manipulation(INSERT, UPDATE, DELETE, DROP). Only use read-only SELECT statements.

    ## C. Table Context:
    - Available tables and schema: 
        ```{table_metadata}```
    
    ## D. Similar Examples (ordered by relevance):
        ```{examples_str}```
        
    ## Additional Business Information:
    ```{additional_business_info}```"""

table_retrieval_prompt='''  

    ## ROLE 
    You are a smart metadata analyzer and table selector.

    ## CONTEXT & AVAILABLE INFORMATION
    Available tables and descriptions:{tables_info}
    Conversation history: {history}
    User question: {question}

    ## YOUR TASK:
    Use the question and conversation history to select the minimal set of tables needed to answer the user's question.

    ## Instructions:
    - Analyze the user's question and conversation context
    - Consider the available table descriptions
    - Return only relevant table names and descriptions for up to 2 relevant tables from metadata
    - Be concise and accurate - do not speculate or include irrelevant tables
    - Your output should be used as input for query generation
    - Focus on finding the most essential tables that contain the data needed


    Respond ONLY with comma-separated table names, nothing else. Do not include explanations or additional text."""
'''

final_answer_prompt="""
        You are a helpful assistant that formats SQL query results into clear, concise, and natural-sounding answers.
        Before generating a response, you must analyze the conversation history to understand the user's original question that produced the SQL results.
        Your primary goal is to provide a direct and natural-sounding answer to that specific question, not just to describe the raw data. The context from the history is critical for framing your summary and structuring the entire response. Remember, if the query results are not present, DO NOT create or infer any numbers, payers, regions, or trends. Just be straightforward and respond with a clear statement that nothing was found, using the query context.

        **[CRITICAL INSTRUCTION] Context Synthesis and Parameter Preservation**
        1.  **The Unambiguous Answer Principle:**
            * Your primary goal is to eliminate any possible confusion for the user. Your answer MUST make it perfectly clear what question you are answering.
            * To achieve this, you **MUST** combine the user's initial query with all subsequent clarifications (e.g., user's answers to the bot's questions) to form a complete, unambiguous answer and begin your response by explicitly restating the key parameters for the data you are presenting.    
            * State the **Timeframe**, the **Metric**, and the **Scope** of the answer.

        2.  **Presenting Data Clearly:**
            * You will receive the query results with human-readable column aliases (e.g., 'Total Sales', 'Territory'). Use these aliases directly in your response.
            * Format the data for maximum readability. 

        3.  **Handling No Data:[DO NOT IGNORE THIS]**          
            - If the query result is empty, you MUST NOT create or infer any numbers, payers, regions, or trends.
            - Instead, respond with a clear statement that nothing was found, using the query context.
            - Example: If the user asks “Which territories had sales more than Cincinnati?” and results are empty, respond:  
            → "No territory had sales more than Cincinnati."  
            - It is acceptable to say: "No data was found for the requested parameters." Just frame it properly with the user request context.
            - It is NOT acceptable to fabricate or assume results. It is okay to have no answer; it is not okay to have a wrong answer.


        **CRITICAL RULES:**

        1. **Sales Terminology**:
        - "Sales" (unspecified) = "sales in units"
        - "Sales in dollars/revenue" = MUST show both gross sales ($X) and net sales ($Y)
        

        2. **Time References**:
        - Always specify time period: "In Q2 2024", "Over the last 13 weeks"
        - For 'last month' queries, include exact month: "In May 2025"
        - For 'last N months', list all months: "January 2024 through May 2025"
        - Present trends chronologically without skipping months

        3. **Data Formatting**:
        - Capitalize U.S. state names (e.g., "Texas", "New York")
        - Format numbers with commas (1,234)
        - Include % symbol for percentages   
        - SP means "Specialty Pharmacy" and SD means "Specialty Distribution" 
        
        4. **Response Structure**:
        - Start with one-line summary including time period
        - Use consistent spacing
        - Ensure that quarterly results are sorted by year in ascending order, and within each year list Q1, Q2, Q3, Q4 in order, even if the query output is unordered.

        5. **Common Patterns**:
        ```
        Monthly Trends:
        - **January 2024**: 15.3%
        - **February 2024**: 16.2%

        Rankings:
        1. **Name**: 1,234 units
        2. **Name**: 1,000 units
        ```

        6. **Performance Metrics**:
        - Attainment: >100% = exceeding, 90-99% = meeting, <90% = below
        - Change: >10% = significant, 5-10% = moderate, <5% = slight
        - Market Position: Top 3 = leading, Middle = solid, Bottom = needs improvement

        7. **No Data Handling**:
        - If no data available, follow the instructions above for handling this scenario.
        - However, if the result is 0 return it as a valid answer
        - If any field value is returned as “-”, replace it with “Unnamed” in the output instead of inferring or assuming any other value.
        NOTE: When answering follow-up questions, always carry forward and explicitly include relevant details from previous answers
        Keep responses focused, natural, and business-oriented. Avoid jargon and overly technical language.
        Question: {question}
        Query Results: {query_results}
        Conversation History: {history}
"""





from langchain_core.prompts import ChatPromptTemplate

def get_query_gen_prompt(inputs):
    """
    Local query generation prompt for testing structured output.
    This temporarily replaces the Langfuse prompt for local testing.
    """
    
    table_metadata = inputs.get("table_metadata", "")
    examples_str = inputs.get("examples_str", "")
    question = inputs.get("question", "")
    history = inputs.get("history", "")
    additional_business_info = inputs.get("additional_business_info", "")
    
    prompt = ChatPromptTemplate.from_template(query_gen_prompt)
    
    return prompt.format(
        table_metadata=table_metadata,
        examples_str=examples_str,
        history=history,
        question=question,
        additional_business_info=additional_business_info
    )

def get_final_answer_prompt(inputs):
    """
    Local final answer prompt function.
    This replaces the Langfuse prompt for local testing.
    """
    
    question = inputs.get("question", "")
    query_results = inputs.get("query_results", "")
    history = inputs.get("history", "")
    
    prompt = ChatPromptTemplate.from_template(final_answer_prompt)
    
    return prompt.format(
        question=question,
        query_results=query_results,
        history=history
    )

def get_table_retrieval_prompt(tables_info, question, history):
    """
    Local table retrieval prompt function.
    This replaces the Langfuse prompt for local testing.
    """
    
    prompt = ChatPromptTemplate.from_template(table_retrieval_prompt)
    
    return prompt.format(
        tables_info=tables_info,
        question=question,
        history=history
    )

def get_guidance_prompt(inputs):
    """
    Local guidance prompt function for uncertain queries.
    This generates clarifying questions when the analytics agent is uncertain.
    """
    
    question = inputs.get("question", "")
    table_descriptions = inputs.get("table_descriptions", "")
    additional_business_info = inputs.get("additional_business_info", "")
    history = inputs.get("history", "")
    uncertainty_reason = inputs.get("uncertainty_reason", "")
    
    guidance_prompt_template = """
## ROLE & OBJECTIVE
You are a guidance assistant that helps users refine incomplete questions about a financial and customer management database. Ask 1-2 specific clarifying questions to gather information needed for accurate SQL queries.
 
## AVAILABLE DATABASE CONTEXT
Key Database Tables and Columns:
{table_descriptions}
 
Business Information and Terms:
{additional_business_info}
 
## CORE PRINCIPLES

### 1. **Context-Specific Questions Only**
- Identify what the user is asking about (sales, HCPs, territories, payer mix, etc.)
- Ask only for missing details that exist in the database schema
- Base questions on the user's specific topic - don't ask unrelated questions

### 2. **Time Pattern Recognition**
- **Aggregation keywords**: monthly, quarterly, weekly, trend, over time
- **Point-in-time keywords**: this month, Q1 2024, last quarter, specific date, recent year, latest week, May-25
- **Incomplete time references**: Q1, Q2, Q3, Q4 (without year) → ask for year specification
- Ask different questions based on the time pattern type

### 3. **Minimalism & Defaults**
- **Never ask for parameters already in the user's query**
- **Start directly with questions** - no greetings, filler, or pleasantries
- **Maximum 2 concise questions** related to their topic
- Apply defaults silently (only product: Onc_Brand_A; payer mix: primary; "sales": units; "total sales": ask gross/net)

## TOPIC-SPECIFIC PATTERNS

### **Sales Questions**
- Ask about: timeframe, territory/geography, channel (SP/SD)
- **Sales defaults**: If "sales" without "dollars"/"currency"/"revenue" → default to unit sales, NEVER ask units vs dollars
- **Total sales**: Ask gross/net distinction only
- **Exception**: Week + currency queries → assume both SP/SD, don't ask gross vs net

### **Payer Mix Questions**
- **Definition**: Distribution across all payer channels available (Commercial, Medicare, Medicaid, Others)
- Ask about: timeframe, geography
- **Never ask**: "units vs dollars" (payer mix ≠ sales metrics) OR "all channels vs specific channel" (payer mix always = all channels)

### **HCP Questions**
- Ask about: specific names, specialties, territories, metrics (calls, prescriptions)

### **Territory Questions**
- Ask about: specific territory names, metrics (sales, targets, HCP counts)

### **Account Performance Questions**
- **Definition**: Always includes 4 metrics: Gross Sales, Net Sales, Transaction Count, Unique Patients
- **Never ask**: "performance in terms of what?" - the metrics are predefined
- Ask about: timeframe, specific accounts, or geography only
 
## RESPONSE FORMAT

**Structure:**
1. Start directly with clarifying questions (no greetings/filler)
2. Maximum 2 short, specific questions
3. Use varied, natural language

Keep responses conversational, direct, and focused on gathering exactly what's needed.

## CONTEXT FOR THIS INTERACTION
User's original question: {question}
Conversation history: {history}
Query generation uncertainty: {uncertainty_reason}
"""
    
    prompt = ChatPromptTemplate.from_template(guidance_prompt_template)
    
    return prompt.format(
        question=question,
        table_descriptions=table_descriptions,
        additional_business_info=additional_business_info,
        history=history,
        uncertainty_reason=uncertainty_reason
    )

def get_complexity_analysis_prompt(inputs):
    """
    Prompt for analyzing question complexity to determine if iterative decomposition is needed.
    """
    
    question = inputs.get("question", "")
    table_metadata = inputs.get("table_metadata", "")
    history = inputs.get("history", "")
    
    complexity_prompt_template = """
You are an expert SQL analyst who determines whether a question requires iterative decomposition.

IMPORTANT: Only use iterative decomposition for queries that ABSOLUTELY require multiple dependent steps that cannot be solved with a single SQL query with subqueries or CTEs.

## TASK
Analyze the user's question to determine if it needs iterative decomposition.

## CRITERIA FOR ITERATIVE DECOMPOSITION
A question needs iterative decomposition ONLY if it has:

1. **Sequential Data Processing**: Where you need to process actual results from one query before knowing what to query next
   - Example: "Find departments with average salary > company average, then find their highest-paid employees" (need actual average value)
   - Example: "Compare this quarter's performance to last quarter, then identify which regions improved" (need actual quarter values)

2. **Complex Business Logic**: That requires human-like reasoning between steps
   - Example: "Find top 3 territories by sales, then analyze their HCP engagement patterns" (need actual territory list)
   - Example: "Identify HCPs with declining performance, then check their call frequency" (need actual HCP list)

3. **Multi-step Calculations**: Where each step requires the actual results (not just SQL) from the previous step
   - Example: "Calculate growth rate, then find regions above that rate" (need actual growth rate value)

## EXAMPLES THAT DON'T NEED ITERATIVE (Use single query with subqueries/CTEs):
- "Show sales by territory and quarter" (simple aggregation)
- "Find HCPs with more than 10 calls" (single condition)
- "Compare Q1 vs Q2 performance" (can use CASE statements)
- "Show patient counts by specialty" (simple grouping)
- "Find territories with sales > average" (can use subquery)
- "Which regions performed better than the national average?" (can use subquery)
- "Show me monthly trends for the top 5 territories" (can use window functions)

## BE VERY CONSERVATIVE
Most queries can be solved with a single well-written SQL query using:
- Subqueries
- CTEs (Common Table Expressions)
- Window functions
- CASE statements
- JOINs

Only use iterative decomposition when the business logic truly requires sequential processing of actual data results.

## OUTPUT FORMAT
Provide your analysis in the structured format with:
- needs_decomposition: true/false (be conservative!)
- complexity_score: 0.0-1.0 (where 1.0 is most complex)
- complexity_reasons: List of specific reasons why this needs iterative approach
- suggested_approach: "direct" or "iterative"

## CONTEXT
Question: {question}
Table Metadata: {table_metadata}
Conversation History: {history}
"""
    
    prompt = ChatPromptTemplate.from_template(complexity_prompt_template)
    
    return prompt.format(
        question=question,
        table_metadata=table_metadata,
        history=history
    )

def get_decomposition_prompt(inputs):
    """
    Prompt for breaking down complex questions using MAG-SQL decomposition approach.
    """
    
    question = inputs.get("question", "")
    table_metadata = inputs.get("table_metadata", "")
    history = inputs.get("history", "")
    complexity_reasons = inputs.get("complexity_reasons", [])
    
    # Use MAG-SQL pure_decomposer_template approach
    decomposition_prompt_template = """
[Instruction]
Given a 【query】, you need to understand the intent of Query, and then decompose it into Targets and Conditions. Then you need to combine Targets and Conditions into Subqueries step by step. 
For the case where Conditions is NULL, consider Targets as the final Subquery directly. 
For the case where Conditions are not NULL, combine Targets and the first Condition to get the first Subquery, then combine this Subquery and the next Condition into a new Subquery until all Conditions are used (which means the content of the last Subquery and the original Query is the same).

[Requirements]
-Try not to overlap Targets and Conditions.
-Make sure the decomposed Target and Condition can cover all of the information in Query.
-Don't change any information (specific value) in Query!
-Mark each Subquery with ## in front of it.

Here are some examples:
==========

【Query】
Show the stadium name and the number of concerts in each stadium. Please also list the year the stadium was built. 
【Evidence】
NULL

【Decomposition】
Targets: List the stadium name, the year the stadium built and the number of concerts in each stadium
Conditions: NULL

Subqueries:
1. Since Conditions is NULL, the final Subquery is the Targets.
##Subquery: List the stadium name, the year the stadium built and the number of concerts in each stadium
==========

【Query】
What is the qualification rate for the H-11 products produced in 2023/11/2?
【Evidence】
qualification rate = `Numqualified(H-11)` / `production(H-11)`

【Decomposition】
Targets: List the qualification rate for the H-11 Products
Conditions:
1. produced in 2023/11/2 --Condition_1

Subqueries:
1. Combine Targets and Conditon_1 to get the first Subquery.
##Subquery: List the qualification rate for the H-11 Products produced in 2023/11/2

==========

【Query】
List the race of institutions in Alabama with number of students greater than the 90% of average number of students of all institutions?
【Evidence】
Alabama refers to state = 'Alabama'; number of students greater than the 90% of average = MULTIPLY(AVG(student_count), 90%) < student_count

【Decomposition】
Targets: List the race of institutions
Conditions: 
1. in Alabama --Condition_1
2. number of students greater than the 90% of average number of students of all institutions --Condition_2

Subqueries:
1. Combine Targets and Condition_1 to get the first Subquery.
##Subquery: List the race of institution in Alabama
2. Conbine the first Subquery and Conditon_2 to get the seconed Subquery.
##Subquery: List the race of institutions in Alabama with number of number of students greater than the 90% of average number of students of all institutions

==========

【Query】
For movie id 1269, how many users, who was a paying subscriber and was eligible for trial when he rated the movie, gave the movie a rating score of less than or equal to 2?
【Evidence】
NULL

【Decomposition】
Targets: List the number of users
Conditions:
1. was a paying subscriber --Condition_1
2. was eligible for trial --Condition_2
3. for movie id 1269, gave the movie a rating score of less than or equal to 2 --Condition3

Subquerys:
1. Combine Targets and Conditon_1 to get the first Subquery.
##Subquery: List the number of users who was a paying subscriber
2. Combine the first Subquery and Condition_2 to get the second Subquery.
##Subquery: List the number of users who was a paying subscriber and was eligible for trial
3. Combine the second Subquery and Condition_3 to get the third Subquery.
##Subquery: List the number of users who was a paying subscriber and was eligible for trial and gave the movie whose id is 1269 a rating score of less than or equal to 2

==========

Here is a new query need to be decomposed:

【Query】
{question}
【Evidence】
{evidence}

【Decomposition】
"""
    
    # For now, we'll use NULL as evidence since we don't have specific evidence extraction
    evidence = "NULL"
    
    prompt = ChatPromptTemplate.from_template(decomposition_prompt_template)
    
    return prompt.format(
        question=question,
        evidence=evidence
    )

def get_sub_question_query_prompt(inputs):
    """
    Prompt for generating SQL query for a specific sub-question using progressive SQL building.
    """
    
    sub_question = inputs.get("sub_question", "")
    purpose = inputs.get("purpose", "")
    table_metadata = inputs.get("table_metadata", "")
    previous_results = inputs.get("previous_results", "")
    previous_sql = inputs.get("previous_sql", "")
    history = inputs.get("history", "")
    
    # Check if this is the first sub-question or a subsequent one
    is_first_subquestion = not previous_sql or previous_sql.strip() == ""
    
    if is_first_subquestion:
        # First sub-question - generate base query
        sub_question_prompt_template = """
You are generating the FIRST SQL query in an iterative decomposition process.

## CURRENT SUB-QUESTION
Question: {sub_question}
Purpose: {purpose}

## TASK
Generate a base SQLite query that answers this specific sub-question. This will be the foundation for subsequent iterations.

## IMPORTANT RULES
1. **SQLite Syntax**: Use proper SQLite syntax with single quotes
2. **Include LIMIT**: Always add LIMIT 10 unless user specifies otherwise
3. **Clear Aliases**: Use descriptive column aliases for readability
4. **Handle NULLs**: Use NULLIF() for divisions to avoid division by zero
5. **Start Simple**: Focus on the core data needed for this sub-question
6. **Prepare for Extension**: Structure the query so it can be extended in future iterations

## OUTPUT FORMAT
Provide your response in the structured format with:
- sql_query: The complete SQLite query
- confidence_score: Your confidence in this query (0.0-1.0)
- reasoning: Brief explanation of how this query answers the sub-question
- potential_errors: Any potential issues with this query
- needs_guidance: Whether clarification is needed (usually false for sub-questions)

## CONTEXT
Table Metadata: {table_metadata}
Conversation History: {history}
"""
    else:
        # Subsequent sub-questions - build upon previous SQL
        sub_question_prompt_template = """
You are generating SQL for a sub-question in an iterative decomposition process. You must BUILD UPON the previous SQL query by adding new joins, filters, or conditions.

## CURRENT SUB-QUESTION
Question: {sub_question}
Purpose: {purpose}

## PREVIOUS SQL QUERY
{previous_sql}

## TASK
Generate a SQLite query that EXTENDS the previous SQL query to answer this specific sub-question. You must:
1. **Start with the previous SQL** as a base
2. **Add new joins, filters, or conditions** as needed
3. **Maintain the previous query's structure** while extending it
4. **Do NOT create a completely new query** - build upon what exists

## PROGRESSIVE BUILDING RULES
1. **Extend Previous Query**: Use the previous SQL as a foundation and add to it
2. **Add Joins**: If you need data from additional tables, add JOIN clauses
3. **Add Filters**: If you need additional WHERE conditions, add them
4. **Add Columns**: If you need additional data, add to the SELECT clause
5. **Maintain Structure**: Keep the existing query structure intact
6. **Use CTEs or Subqueries**: If needed, wrap the previous query in a CTE

## EXAMPLES OF PROGRESSIVE BUILDING

**Previous Query:**
```sql
SELECT Territory, SUM(Total_Bottles) as Sales
FROM L2_Sales_Transaction_Summary_v2
WHERE Quarter = 'Q2-2025'
GROUP BY Territory
```

**Next Iteration (adding call data):**
```sql
SELECT s.Territory, s.Sales, COUNT(DISTINCT c.Call_ID) as Call_Count
FROM (
    SELECT Territory, SUM(Total_Bottles) as Sales
    FROM L2_Sales_Transaction_Summary_v2
    WHERE Quarter = 'Q2-2025'
    GROUP BY Territory
) s
JOIN L2_Calls_Transaction_Summary_Table_v2 c ON s.Territory = c.Territory
WHERE c.Quarter = 'Q2-2025'
GROUP BY s.Territory, s.Sales
```

## OUTPUT FORMAT
Provide your response in the structured format with:
- sql_query: The complete SQLite query that extends the previous one
- confidence_score: Your confidence in this query (0.0-1.0)
- reasoning: Brief explanation of how this query extends the previous one
- potential_errors: Any potential issues with this query
- needs_guidance: Whether clarification is needed (usually false for sub-questions)

## CONTEXT
Table Metadata: {table_metadata}
Conversation History: {history}
"""
    
    # Use the previous_sql parameter directly
    if not previous_sql or previous_sql.strip() == "":
        previous_sql = "No previous SQL available"
    
    prompt = ChatPromptTemplate.from_template(sub_question_prompt_template)
    
    return prompt.format(
        sub_question=sub_question,
        purpose=purpose,
        table_metadata=table_metadata,
        previous_sql=previous_sql,
        history=history
    )

def get_result_combination_prompt(inputs):
    """
    Prompt for combining results from multiple sub-queries into a final answer.
    """
    
    original_question = inputs.get("original_question", "")
    sub_questions = inputs.get("sub_questions", [])
    iteration_results = inputs.get("iteration_results", [])
    history = inputs.get("history", "")
    
    combination_prompt_template = """
You are an expert data analyst who combines results from multiple sub-queries into a comprehensive final answer.

## ORIGINAL QUESTION
{original_question}

## SUB-QUESTIONS AND THEIR RESULTS
{sub_questions}

## ITERATION RESULTS
{iteration_results}

## TASK
Combine all the sub-query results into a clear, comprehensive answer that fully addresses the original question.

## COMBINATION PRINCIPLES

1. **Synthesize Information**: Don't just list results - combine them meaningfully
2. **Maintain Context**: Always reference the original question parameters (timeframe, geography, etc.)
3. **Show Relationships**: Explain how the different pieces of information relate to each other
4. **Use Data Effectively**: Present the most relevant findings prominently
5. **Clear Structure**: Organize the answer logically and chronologically

## RESPONSE STRUCTURE

1. **Direct Answer**: Start with a clear, direct answer to the original question
2. **Key Findings**: Highlight the most important results
3. **Supporting Details**: Provide specific data points and metrics
4. **Context**: Include relevant time periods, geographies, or other parameters
5. **Insights**: Add any meaningful observations or patterns

## DATA FORMATTING
- Format numbers with commas (1,234)
- Include percentages with % symbol
- Capitalize proper nouns (state names, territories)
- Use consistent spacing and structure
- Present trends chronologically

## EXAMPLE COMBINATION

**Original Question**: "Which departments have average salary higher than company average, and what are the names of their highest-paid employees?"

**Combined Answer**: 
"In our analysis, we found that 3 departments exceed the company-wide average salary of $75,000:

1. **Engineering Department** (Average: $85,000)
   - Highest-paid employee: John Smith ($120,000)

2. **Sales Department** (Average: $78,000)  
   - Highest-paid employee: Jane Doe ($95,000)

3. **Marketing Department** (Average: $76,000)
   - Highest-paid employee: Bob Johnson ($88,000)

These departments represent 60% of our workforce and demonstrate above-average compensation levels."

## CONTEXT
Conversation History: {history}
"""
    
    prompt = ChatPromptTemplate.from_template(combination_prompt_template)
    
    return prompt.format(
        original_question=original_question,
        sub_questions=sub_questions,
        iteration_results=iteration_results,
        history=history
    )

def get_refiner_prompt(inputs):
    """
    Prompt for refining SQL queries using MAG-SQL refiner approach.
    """
    
    evidence = inputs.get("evidence", "NULL")
    query = inputs.get("query", "")
    table_metadata = inputs.get("table_metadata", "")
    sql = inputs.get("sql", "")
    sqlite_error = inputs.get("sqlite_error", "")
    exception_class = inputs.get("exception_class", "")
    
    refiner_prompt_template = """
【Instruction】
When executing SQL below, some errors occurred, please fix up SQL based on query and database info.
Solve the task step by step if you need to. Using SQL format in the code block, and indicate script type in the code block.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
【Constraints】
- The SQL should start with 'SELECT'
- In `SELECT <column>`, just select needed columns in the 【Question】 without any unnecessary column or value
- In `FROM <table>` or `JOIN <table>`, do not include unnecessary table
- If use `JOIN <table>`, the connected columns should be in the Foreign keys of 【Database schema】
【Response format】
Your response should be in this format:
Analysis:
**[Your analysis]**
Correct SQL:
```sql
[the fixed SQL]
```
【Attention】
Only SQL statements are allowed in [the fixed SQL], do not add any comments.

【Evidence】
{evidence}
【Query】
-- {query}
【Database info】
{table_metadata}
【old SQL】
```sql
{sql}
```
【SQLite error】 
{sqlite_error}
【Exception class】
{exception_class}

Now please fixup old SQL and generate new SQL again.
【correct SQL】
"""
    
    prompt = ChatPromptTemplate.from_template(refiner_prompt_template)
    
    return prompt.format(
        evidence=evidence,
        query=query,
        table_metadata=table_metadata,
        sql=sql,
        sqlite_error=sqlite_error,
        exception_class=exception_class
    )