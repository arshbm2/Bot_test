

additional_business_info="""                                                                 Home with solid fill, Picture 
- Week_Ending_Date does not always include the last calendar day of the month, so we must not assume it.Instead, to get metrics like "free samples issued per month", you must: 
Parse the Week_Ending_Date (which is in 'YYYY-MM-DD' format), Group by the latest parsed_date per month-year, and Sum only those rows corresponding to the latest week-ending per month. 
- The last date in the data is 30th May,2025 or 2025-05-30. 
- "Market Share": The share of the company's product in number of patients compared to the total patients in the market (which includes competitor patients). Calculated as Market Share = (Number of Patients who are prescribed Onc_Brand_A* 100) / Total patients in market. 
- "Attainment": The achievement of sales as a percentage of set targets, calculated as Attainment = (Actual Sales * 100) / Target Sales. Attainment is a relevant attribute for the company as a whole and also for individual territories. Achieving high attainment could be an indicator of high performance. 
- "Bottles": Is the same as the number of units. Bottles may be either categorized as SP (Specialty Pharmacy) and SD (Specialty Distribution) bottles. 
- "Volume": Refers to the total count of Bottles(SP Bottles+SD Bottles), indicating the quantity of product distributed or sold. If used along with the term "patient", then it refers to the number of total patients (without competitor patients) that are prescribed the specified product. If used along with sales it indicates the total gross sales. 
- "GTN" : (Gross to Net) Refers to the calculation from gross sales to net sales, considering deductions like discounts, returns, and allowances. 
- "Rx": An abbreviation for 'prescription', typically referring to the amount of medication prescribed or dispensed. It is also sometimes referred to as script. Script volume or Rx volume. 
- "Quarter": Denotes a three-month period within a fiscal year used for financial reporting, typically divided as Q1 (January-March), Q2 (April-June), Q3 (July-September), and Q4 (October-December). 
- "Untapped Potential" or "Untapped Opportunity": Denotes volume of the market that is not yet captured by the specified product. It is calculated by subtracting the Bottles of the specified product from the Total bottles, including competitor product. Indicates areas or markets where the current market share is low, suggesting a high potential for growth or increased sales. 
- "Good Results": There are many measures for results. Some of the measures for good results can include 
a) Attainment is higher than 100% or the sales volume is higher than target (or goals) 
b) The growth in sales is higher than the national average 
- "Performance": When discussing the performance of anything, we need to provide information only on their sales attainment to provide a view of their business activities. 
- "Forecast": Often used interchangeably with "Target" or "Goal", this term refers to projected sales or performance metrics in specific time frames. 
- "Units": Interchangeably used with "Volume" or "Bottles" to indicate the quantity of a product, especially in terms of sales or distribution. Sometimes units may also be referred to as "unit sales" or "sales in units". 
- "Region": This term is used synonymously with "Territory" from the data and refers to a specific geographical area assigned to an entity. 
- "Sub-nation": This term is used synonymously with "Territory" from the data and refers to a specific geographical area assigned to an entity. 
- "SD": Specialty Distributor 
- "SP": Specialty Pharmacy 
- "Channel": Sales channel, representing the different channels from which the sales are achieved. It could be either payer channels (Commercial, Medicare, Medicaid, Others) or Specialty Pharmacy/Specialty Distributor. Use Specialty Pharmacy/Specialty Distributor as channels unless specified. 
- "Payer Mix": It refers to the percentage of patients or units across different payer channels (Commercial, Medicare, Medicaid, Others). Unless otherwise specified, use the distribution of sales as default for payer mix 
- "Distribution Channel Mix": It refers to the percentage of patients or units by Specialty Pharmacy/Specialty Distributor. 
- "Sold": Total number of bottles sold by HCPs or by accounts. It can also be referred to as prescriptions written or prescribed. 
- "Specialty Mix": Distribution of the Total Gross Sales or bottles/units across the different HCP specialties. Unless specified, use total gross sales (SP and SD combined) to show the specialty mix. 
- "HCP": HCP refers to an individual medical professional involved in prescribing, diagnosing, treating, or managing patients. HCPs are central entities for sales, engagement, and targeting analytics. The term "HCP" broadly includes doctors (MDs, etc), specialists such as oncologists or endocrinologists, nurse practitioners (NPs), physician assistants (PAs), registered nurses (RNs) involved in therapeutic decision-making or care coordination, and other licensed prescribers or certified medical staff who are eligible to interact with pharma products or representatives. 
- "Growth": Absolute increase between two time periods. Formula: Growth = Value at T2 - Value at T1. For example: If SP_Bottles in Q1 = 1,000 and in Q2 = 1,500, then Growth = 500. 
- "Growth Rate": Percentage change between two time periods. Formula: Growth Rate = ((T2 - T1) / T1) × 100. For example: ((1,500 - 1,000) / 1,000) × 100 = 50%. 
- "New Patient Starts": Refers to count of patients with New_Patient_Flag = 1 from the L2_Sales_Transaction_Summary_v2 table. Represents initiation of treatment of new patients. 
- "Existing Patients": When a user mentions existing patient count for a specific time period, first maximum of 'New_Patient_Flag' will be calculated for each 'Patient_ID' in that time period and then distinct count of 'Patient_ID' where maximum of 'New_Patient_flag' is 0, is used to get existing patient count. 
-"Monthly Average": Mean of a selected metric grouped by Month. For example: Average SP_Bottles per month for 2024. 
- "Quarterly Average": Mean of a selected metric grouped by Quarter. For example: Average Total_Gross per quarter across all territories. 
- "Top": Implies best or most in a certain category for example, "Top 5 HCPs" → Rank HCPs by SP_Bottles or Total_Gross or "Top products in Q1 2024" can be calculated using filter by Quarter and rank by Total_Gross. Ask clarifying questions like Top by what metric? Over what time period? 
-"Worst": refers to the lowest-ranked entity in a given metric, dimension, or time period. It must always be tied to a metric (sales, calls, prescriptions, attainment), an entity (HCP, territory, brand), and a timeframe. If no rank count is specified, default to bottom 5.
-"Open Rate": refers to the percentage of emails that were opened by recipients. This metric must specify the entity (e.g., HCPs, accounts, campaign,area,region,territory) and timeframe (e.g., this month, last quarter). Use Publisher column to filter open or sent emails. Calculation of Open Rate: Count of Emails with Publisher as open / Count of Emails with Publisher as sent from the L2_HCP_Events_Table_v2 table.
-"Attendees": refers to the count of HCPs who attended Speaker Programs. It is calculated as the distinct count of HCPs who attended a speaker program event. Use the Event columns to filter out Speaker program channel.
-"Click Rate": refers to the percentage of emails that were clicked by recipients. It can also be referred as Click through or Click through rate. This metric must specify the entity (e.g., HCPs, accounts,region, campaign), and timeframe (e.g., this month, last quarter). Calculation of Click Rate: Count of Emails with Publisher as Click / Count of Emails with Published as sent from the L2_HCP_Events_Table_v2 table.
- "Highest": Maximum value in a metric, for example "Highest grossing product last quarter" can be calculated using Total_Gross grouped by Product_Name, filter by quarter or "Highest prescriber of new patients" you can Use New_Patient_Flag = 1, group by HCP, rank by count. 
- "Lowest": Minimum value in a metric, for example "Lowest performing region" can be calculated using group by Region_Name, rank by Total_Gross or New_Patient_Flag or "Account with lowest sales in June" you can filter by Month, group by Account_Name, sort by Total_Gross. 
- Do not use SQLite's built-in date and time functions such as DATE('now') or strftime() to generate current dates dynamically. Instead, examine the actual data within the table to identify and use the most recent date that exists in the data. 
- "Account Performance": For any query asking about account performance, always calculate four key metrics: Gross Sales (SUM(Total_Gross)), Net Sales (SUM(Total_Net)), Transaction Count (COUNT(*)), and Unique Patients (COUNT(DISTINCT Patient_ID)), grouped appropriately by account (and time period if specified). Transaction Count represents the total number of sales transactions/records for that account. Unique Patients represents the distinct count of individual patients served by that account. Ensure correct chronological ordering when time periods are involved. 
- When handling queries about specific time periods such as 'this week,' 'this month,' 'this year,' 'last year,''last month,' 'last 2 months,' and 'last 3 weeks,' ensure that the time periods correspond to the latest date from the tables. Additionally, extract and include the corresponding **month name and year**, when asked 'last month', 'last 2 months' etc for clarity in the text answer. 
- If the output of the SQL query created is empty, It means that there is no data for that particular question. 
- The sales of an entity/area is defined as the sum of sales from SP bottles and sales from SD bottles. 
- Additionally, ensure that the answers include the appropriate units such as '$', 'bottles', 'units', etc., wherever applicable, to provide complete and accurate information. 
- It is intended for the float numbers to be rounded to two decimal places. 
- When referring to fields like HCP, account, or territory, ensure that you use the LOWER() function in the SQL query to handle case-insensitive comparisons. 
- When the word 'trend' is mentioned in a question without further detail (such as monthly or weekly), provide the trend in quarterly terms. 
- When the word 'trend' and 'recent' is mentioned in a question without specifying a time period (such as monthly or weekly), provide weekly data for the most recent quarter. Use the latest quarter to group the data and present weekly trends from that quarter. Ensure that the latest quarter is identified based on the date and that weekly data is shown for each 'Week Ending Date' within that quarter. 
- do not put any curly brackets or box brackets in the answer. 
- Provide only the final answer required to answer the user's question, without showing any intermediate steps, calculations, or extra information. 
- When generating text answers, ensure that the first letter of each U.S. state name is capitalized. 
- Whenever ask for weekly sales for any account type, always consider the weekly sales for the year 2025.
- **Descriptive Periods**: LTD (Launch to Date): Covers performance metrics from product launch to the current date , YTD (Year to Date): Covers metrics for the current calendar year up to the current date, QTD (Quarter to Date): Covers metrics for the current quarter up to the current date.
- **CRITICAL SALES FORMATTING RULE**:
a) When a user asks about "sales" without mentioning currency/dollars, you MUST use the exact phrase "sales in units" in your response. For any person/entity, the response format must be: "[Name] made [number] sales in units." This rule overrides all other formatting guidelines. 
b)When a user asks about "sales in dollars" or similar currency-related sales queries (e.g., "sales done by [name] in dollars", "revenue", "sales amount"), you MUST always return BOTH gross sales and net sales separately. Use the columns: Total_Gross (or SP_Gross + SD_Gross) for gross sales, and Total_Net (or SP_Net + SD_Net) for net sales. The query should select both values, for example: SUM(Total_Gross) AS gross_sales, SUM(Total_Net) AS net_sales. This applies to all sales dollar queries regardless of whether the user specifically asks for both metrics. 
c) When the query returns both gross_sales and net_sales (or similar gross/net columns), you MUST present both values clearly. Format as: "[Entity] made $[gross_amount] in gross sales and $[net_amount] in net sales." For example: "Iris Wertheim made $4,500,000 in gross sales and $4,319,999 in net sales." Always include both metrics even if the user's original question only mentioned "sales in dollars" generally. 
- When a user asks about “quarter over quarter” (QoQ) performance, interpret this as a request to return results for all quarters Launch to Date (LTD)

 ***MANDATORY RULE for SQL Generation(do not remove , always use)***:
  -- When counting ID-like columns (Call_ID, Patient_ID, HCP_ID,Account_ID), use COUNT(DISTINCT ...) to avoid duplication unless explicitly told to include duplicates.
  -- 1) For any query that counts calls (tables: L2_Calls_Transaction_Summary_Table_v2 or any table containing Call_ID/Call_Type), NEVER  use COUNT(*) or SUM(CASE ... THEN 1).
   ALWAYS use one of:
     - COUNT(DISTINCT Call_ID)
     - COUNT(DISTINCT CASE WHEN <condition> THEN Call_ID ELSE NULL END)"""

table_descriptions={ 

    "L2_Sales_Transaction_Summary_v2": ( 

        """ The table contains comprehensive information about patient shipments, including patient enrolment de tails, prescription data, product information, healthcare providers, geographical territories, insurance payers, and financial transactions. It supports patient care and sales reporting in a healthcare or pharmaceutical context. This table should be used for all sales and revenue-related questions. Use the 'Total_bottles' field for sales questions and the 'Total_Gross' field for revenue questions. If the question specifies SP_bottles, SD_bottles, SP_Gross, SD_Gross, SP_Net, or SD_Net, use the appropriate field as indicated in the question. This table should be used to answer all questions related to the number of new patients and the total number of patients. Patient information is available only in SP data, so this field is populated only when the Shipment_type is SP. For SD records, it is shown as a dash (-). Dash represents that the record is from SP and no information is available. Any data or metric at the HCP or Account level should be pulled from this table. " 
        Key fields include Shipment_Type, Shipment_ID, First_Shipment_Date,Shipment_Date, Invoice_ID, Invoice_Date, Patient_ID, New_Patient_Flag,  
        Prescriber_Source, Rx_No, First_Enrollment_Date, Prescription_Date, Authorized_Refills,   Fill_number, Days_to_fill, Product_ID, Product_Name, NDC, Product_Description, Strength,  
        Dosage_Form, ICD_Code, Competitor_Flag, Product_Group, Market_ID,Market_Name, Product_Days_of_Supply, SP_Bottles, SD_Bottles, Total_Bottles,  
        Days_of_Supply, Off_label_flag, SP_ID, SP_Name, SP_Location, SD_ID,SD_Location, Week_Ending_Date, Week_Number, Month, Quarter, Year, HCP_ID,  
        NPI, HCP_Name, HCP_Address, HCP_City, HCP_State, HCP_ZIP, HCP_Specialty,HCP_Specialty_Group, HCP_Decile, HCP_Segment, Target_Flag, AMA_Flag,  
        PDRP_Flag, KOL, Email, Phone_number, Territory_ID, Territory_Name, Region_ID,Region_Name, Area_ID, Area_Name, Rep_Name, Rep_Rank, Rep_Vacancy,  
        Primary_Payer_ID, Primary_Payer_Name, Primary_Payer_Channel,Primary_Plan_ID, Primary_Plan_Name, Secondary_Payer_ID,Secondary_Payer_Name, Secondary_Payer_Channel, Secondary_Plan_ID,  
        Secondary_Plan_Name, New_Account_Flag, Account_ID, Account_Name, Account_Address, Account_City, Account_State, Account_ZIP, Account_CoT,  
        Account_Decile, Account_Segment, SP_Gross, SD_Gross, Total_Gross, SP_Net,SD_Net, Total_Net """ 
    ), 

    "L2_Calls_Transaction_Summary_Table_v2": ( 
        """ The table contains comprehensive information about sales representative calls or interactions with healthcare providers, including call details, promoted products, Indication priority, HCP information, geographical territories, and interaction specifics. It supports call activity tracking, marketing analysis, and territory management in a healthcare or pharmaceutical context. This table should be used for all calls related questions. This table includes both call_detail_id and call_id. A single call_id may be associated with multiple call_detail_id entries, depending on the indication_priority. For reporting purposes, calls made to an HCP should be counted based on the distinct call_id. " 
        Key fields include  Call_Detail_ID, Call_ID, Call_Date, Product_ID, Product_Name,Product_Description, Dosage_Form, Competitor_Flag, Product_Group,  
        Product_Days_of_Supply, Market_ID, Market_Name, Priority, Indication, Audience, Interaction_focus, Call_Type, HCP_ID, NPI, HCP_Name, HCP_Address, HCP_City,  
        HCP_State, HCP_ZIP, HCP_Specialty, HCP_Specialty_Group, HCP_Decile, HCP_Segment, Target_Flag, AMA_Flag, PDRP_Flag, KOL, Email, Phone_number,  
        Emp_ID, Emp_Name, Emp_Role, Emp_Email, Territory_ID, Territory_Name,Region_ID, Region_Name, Area_ID, Area_Name, Week_Ending_Date, Week_Number, Month, Quarter, Year """ 
    ), 

    "L2_HCP_Events_Table_v2": ( 
        """ The table contains detailed information about events involving healthcare providers, such as speaker programs, including event details, HCP participation, geographical territories, and time dimensions. It supports marketing analysis, event tracking, and territory management in a healthcare or pharmaceutical context. This table should be used for all engagement-related questions. To answer questions related to a specific event, such as a speaker program or email campaign, we should filter the table on the event column based on the event of interest. " 
        Key fields include Record_ID, Event, Event_ID, NPI, Date, Week_Ending_Date, Week_Number, Month, Quarter, Quarter_Start_Date, Quarter_End_Date, Year,  
        Channel, Engagement_type, Publisher, Speaker_Name, Event_Type, Event_City,Event_State, HCP_ID, HCP_Name, HCP_Address, HCP_City, HCP_State, HCP_ZIP,
        HCP_Specialty, HCP_Specialty_Group, HCP_Decile, HCP_Segment, Target_Flag, AMA_Flag, PDRP_Flag, KOL, Email, Phone_number,  Territory_ID, Territory_Name, Region_ID, Region_Name, Area_ID, Area_Name""" 
    )
    , 

    "L2_Patient_Status_Summary_Table_v2": ( 
        """The table contains detailed information about patient status updates, including patient demographics, status details, specialty pharmacy information, and time dimensions. It supports patient care tracking, referral management, and status monitoring in a healthcare or pharmaceutical context. This table should be used to track the status of the patient.	 " 
        Key fields include  Record_ID, Patient_ID, Gender, Age, Birth_Year, SP_ID, SP_Name, Status_Date, Week_Ending_Date, Week_Number, Month, Quarter,  
        Quarter_Start_Date, Quarter_End_Date, Year, Prescriber_Source, Status,Status_Code, Status_Description""" 
    ), 

    "L3_Enrollment_Table_v2": ( 
        """The table contains detailed information about patient enrolments in a healthcare or pharmaceutical system, including enrolment dates, prescriber details, diagnosis codes, product information, prescription status, and payer details. It supports patient care tracking, prescription management, and financial analysis." 
        Key fields include Enrollment_ID, Patient_ID, Enrollment_Date, NPI,  
        Prescriber_Source, ICD_Code, Product_ID, Product_Name, NDC, Off_label_flag,  
        Rx_No, Authorized_Refills, Status, Status_Code, Status_Description, Status_Date,  
        Primary_Payer_ID, Primary_Payer_Name, Primary_Payer_Channel, Primary_Copay,  
        Primary_OOP, Secondary_Payer_ID, Secondary_Payer_Name,  
        Secondary_Payer_Channel, Secondary_Copay, Secondary_OOP""" 
   ), 

    "L3_Geography_v2": ( 
        "The table contains hierarchical geographical information used in sales and distribution, defining areas, regions, and territories to support territory management, sales reporting, and resource allocation." 
        "Key fields include Area_ID, Area_Name, Region_ID, Region_Name, Territory_ID, Territory_Name " 
    ), 

    "L3_HCO_Master_v2": ( 

        "The table contains detailed information about healthcare organizations or accounts, including identifiers, addresses, classifications, and segmentation data to support account management, sales targeting, and reporting in a healthcare context." 
        "Key fields include Account_ID, Account_Name, Account_Address, Account_City, Account_State, Account_ZIP, Account_CoT, Account_Decile, Account_Segment " 

    ), 

    "L3_HCP_Master_v2": ( 
        "The table contains detailed information about healthcare providers, including identifiers, contact details, specialties, and flags for program participation or statuses. " 
        "Key fields include  HCP_ID, NPI, HCP_Name, HCP_Address, HCP_City, HCP_State, HCP_ZIP, HCP_Specialty, HCP_Specialty_Group, HCP_Decile, HCP_Segment, Target_Flag, AMA_Flag, PDRP_Flag, KOL, Email, Phone_number" 
    ), 

    "L3_ICD_Mapping_v2": ( 
        "The table maps ICD codes to their descriptions and associated market names for medical diagnosis categorization. " 
        "Key fields include ICD_Code, Description, Market_Name" 
    ), 

    "L3_Inventory_Table_v2": ( 
        "The table tracks inventory levels, receipts, and shipments for products at specific locations, identified by NDC and location IDs. " 
        "Key Fields include Week_Ending_Date, SP_SD_ID, NDC, SP_SD_Location, SP_SD_Inventory, Qty_Received, Qty_Shipped" 
    ), 

    "L3_Patient_Level_Master_v2": ( 
        "The table contains demographic information about patients, including gender, age, and birth year. " 
        "Key fields include Patient_ID, Gender, Age, Birth_Year" 
    ), 

    "L3_Payer_Master_v2": ( 
        "The table lists insurance payers, their names, and the channels they operate in. " 
        "Key fields include Payer_ID, Payer_Name, Payer_Channel" 
    ), 

    "L3_Plan_Master_v2": ( 
        "The table details insurance plans offered by payers, including plan IDs, names, and the number of covered lives. " 
        "Key fields include Payer_Name, Plan_ID, Plan_Name, Covered_lives" 
    ), 

    "L3_Product_Master_v2": ( 
        "The table catalogs products, including their NDC, product IDs, names, descriptions, strengths, dosage forms, and market information. " 
        "Key fields include NDC, Product_ID, Product_Name, Product_Description, Strength, Dosage_Form, Competitor_Flag, Product_Group, Market_ID, Market_Name, Product_Days_of_Supply" 
    ), 

    "L3_Roster_v2": ( 
        "The table consists of detailed information about employee assignments to geographical areas, capturing employee details, roles, and dates related to employment and vacancies to support workforce management and territory coverage analysis. " 
        "Key fields include Geo_level, Geo_ID, Geo_Name, Emp_ID, Emp_Name, Emp_Role, Emp_Email, Emp_Start_date, Emp_End_date, IC_Start_Date, IC_End_Date, Vacancy_Start_date, Vacancy_End_date, Data_feed_date" 
    ), 

    "L3_SD_Master_v2": ( 
        "The table consists of detailed information about Specialty distributors, including their identifiers and locations to support inventory and shipment tracking. " 
        "Key fields include SD_ID, SD_Location" 
    ), 

    "L3_SD_Shipment_Table_v2": ( 
        "The table consists of detailed information about shipments from Specialty distributors, capturing shipment and invoice details, product information, and account details to support supply chain management and financial reporting. " 
        "Key fields include Shipment_ID, Shipment_Date, Invoice_ID, Invoice_Date, Product_ID, Product_Name, NDC, SD_Bottles, Account_ID, Account_Name, SD_ID, SD_Location" 
    ), 

    "L3_SP_Master_v2": ( 
        "The table consists of detailed information about specialty pharmacies, including their identifiers, names, and locations to support specialty product distribution and patient care. " 
        "Key fields include SP_ID, SP_Name, SP_Location" 
    ), 

    "L3_SP_Shipment_Table_v2": ( 
        """The table consists of detailed information about shipments from specialty pharmacies, capturing patient and prescriber details, product information, and payer information to support patient care, inventory management, and financial reporting. " 
          Key fields includes  Shipment_ID, Shipment_Date, First_Shipment_Date, New_Patient_Flag, Patient_ID, HCP_ID, NPI, Rx_No, Prescriber_Source, SP_Bottles, Days_of_Supply, Authorized_Refills, Fill_number, Off_label_flag, Product_ID, Product_Name, NDC, ICD_Code, SP_ID, SP_Name, SP_Location, Primary_Payer_ID, Primary_Plan_ID, Secondary_Payer_ID, Secondary_Plan_ID """ 
    ), 

    "L3_Target_and_Free_Sample_v2": ( 
        "The table consists of detailed information about sales targets and free samples distributed, associated with territories and time periods to support sales performance tracking and marketing analysis. " 
        "Key fields include Territory_ID, Territory_Name, Week_Ending_Date, Target_new_patients, Total_Target_patients, Target_Bottles, Free_samples, Target_Gross_Sales, Target_Net_Sales" 
    ), 

    "L3_Time_v2": ( 
        "The table consists of a time dimension with various date-related attributes, including week, month, quarter, and year, to support time-based analysis and reporting. " 
        "Key fields include Date, Week_Ending_Date, Week_Number, Month, Quarter, Quarter_Start_Date, Quarter_End_Date, Year" 
    ), 

    "L3_ZTT_Table_v2": ( 
        "The table consists of detailed information mapping ZIP codes to territories, regions, and areas, providing a geographical hierarchy to support territory alignment and sales analysis. " 
        "Key fields include  ZIP, State, City, Territory_ID, Territory_Name, Region_ID, Region_Name, Area_ID, Area_Name" 
    ), 

    "L3_Call_Detail_Table_v2": ( 
        "The table contains detailed information about specific call details, focusing on products discussed during sales representative interactions with healthcare providers, including call identifiers, dates, priorities, medical indications, and product details. It supports sales activity tracking and product promotion analysis in a healthcare or pharmaceutical context." 
        "Key fields include  Call_Detail_ID, Call_ID, Call_Date, Priority, Indication, Product_ID, Product_Name" 
    ), 

    "L3_Call_Table_v2": ( 
        "The table contains information about sales representative calls to healthcare providers, including call identifiers, dates, employee and HCP details, geographical territories, audience, interaction focus, call type, and market information. It supports sales activity tracking, territory management, and marketing analysis in a healthcare or pharmaceutical context." 
        "Key fields include  Call_ID, Call_Date, Territory_ID, Emp_ID, Emp_Name, NPI, HCP_Name, HCP_State, Decile, Audience, Interaction_Focus, Call_Type, Market_ID, Market_Name" 
    ), 

    "L3_Digital_Campaigns_v2": ( 
        "The table contains information about digital marketing campaigns targeting healthcare providers, including campaign events, engagement types, and publisher details. It supports digital marketing analysis and campaign performance tracking in a healthcare or pharmaceutical context." 
        "Key fields include Record_ID, Event_ID, NPI, Date, Engagement_type, Publisher, Channel" 
    ), 

    "L3_Email_Campaigns_v2": ( 
        "The table contains information about email marketing campaigns targeting healthcare providers, including campaign events, engagement types, channels, and publisher details. It supports email marketing analysis and campaign performance tracking in a healthcare or pharmaceutical context." 
        "Key fields include  Record_ID, Date, NPI, Channel, Engagement_Type, Publisher, Event_ID" 
    ), 

  "L3_Speaker_Program_v2": ( 
        "The table contains information about speaker programs involving healthcare providers, including event details, speaker names, event types, locations, and HCP identifiers. It supports event tracking, marketing analysis, and speaker program management in a healthcare or pharmaceutical context." 
        "Key fields include Record_ID, Date, Event_ID, Speaker_Name, Event_Type, Event_City, Event_State, NPI " 
    ), 

    "L3_Patient_Status_table_v2": 

    ( 
     """The table contains detailed information about patient status tracking and progression, capturing status updates, prescriber sources, specialty pharmacy assignments, and comprehensive status codes to support patient care monitoring, referral management, and care coordination tracking in a healthcare or pharmaceutical context. 
        Key fields include Record_ID, Patient_ID, SP_ID, Status_Date, Prescriber_Source, Status, Status_Code, Status_Description """ 
    ), 

    "L3_Competitor_Table_v2":( 
        """ 
        Stores detailed information about the usage of competitor products by healthcare providers, capturing the number of patients, new prescriptions (NBRx), and patients new to therapy, aggregated by quarter and week. It supports competitive analysis, market share tracking, and sales strategy development in a healthcare or pharmaceutical context. 
        Key fields include Quarter, Week_Ending_Date, NPI, Num_Patients_Competitor_Products, NBRx, New_to_Therapy 
        """ 
    ) 

}   
 

Table_Metadata  ={ 


"L2_Sales_Transaction_Summary_v2": """Stores detailed information about patient shipments, including shipment details, patient, prescription, product, healthcare provider, territory, payer, and financial data to support patient care, inventory management, and sales reporting in a healthcare or pharmaceutical context. 
    Here is the schema information of the Table along with descriptions of each column: 
    - "Shipment_Type": TEXT – Type of shipment, e.g., 'SP' or 'SD'. SP is Specialty Pharmacy and SD is Specialty Distribution. 
    - "Shipment_ID": INTEGER – Unique identifier for the shipment. 
    - "First_Shipment_Date": DATE – Date when the first shipment for the patient occurred. Patient information is available only in SP data, so this field is populated only when the Shipment_type is SP. For SD records, it is shown as a dash (-). Dash represents that the record is from SP and no information is available. 
    - "Shipment_Date": DATE – Date when the shipment occurred. You can use this to extract information like the date, week, month and year of the data collection from this. 
    - "Invoice_ID": TEXT – Unique identifier for the invoice associated with the shipment. 
    - "Invoice_Date": DATE – Date when the invoice was issued. 
    - "Patient_ID": TEXT – Unique identifier for the patient receiving the shipment. Patient information is available only in SP data, so this field is populated only when the Shipment_type is SP. For SD records, it is shown as a dash (-). Dash represents that the record is from SP and no information is available. 
    - "New_Patient_Flag": TEXT – Indicates if the patient is new '1' or existing '0'. Patient information is available only in SP data, so this field is populated only when the Shipment_type is SP. For SD records, it is shown as a dash (-). Dash represents that the record is from SP and no information is available. 
    - "Prescriber_Source": TEXT – Source of the prescription, such as 'PRESCRIBER' or 'HUB'. 
    - "Rx_No": TEXT – Prescription number, often hashed or encrypted for privacy. One patient can have multiple Rx_numbers, as each represents a prescription ID, and a patient can have multiple prescriptions. 
    - "First_Enrollment_Date": DATE – Date when the patient was first enrolled. 
    - "Prescription_Date": DATE – Date when the prescription was originally written or issued by the healthcare provider. 
    - "Authorized_Refills": TEXT – Number of authorized refills for the prescription. This can be used to calculate unfilled bottles or unfilled prescriptions, as it represents the total number of authorized bottles. It is unique for each Rx_No. To calculate unfilled bottles, group by Rx_No and Authorized_Refills, and take the sum of Total_Bottles. The sum of Total_Bottles gives the filled prescription count. Subtracting this from the Authorized_Refills will give the unfilled prescription count. 
    - "Fill_number": TEXT – The fill number for the prescription (e.g., 1 for first fill, 2 for refill). 
    - "Days_to_fill": TEXT – Number of days taken to fill the prescription. It is a measure of operational efficiency. This represents the number of days it took for the first shipment after the prescription was written. It is unique for each Rx_No, i.e., each prescription.    
    - "Product_ID": TEXT – Unique identifier for the product. 
    - "Product_Name": TEXT – Name of the product, e.g., 'Product_X'. 
    - "NDC": TEXT – National Drug Code for the product. 
    - "Product_Description": TEXT – Description of the product, e.g., 'AROMATASE INHIB'. 
    - "Strength": TEXT – Strength of the product, e.g., '10 ml'. 
    - "Dosage_Form": TEXT – Form of the dosage, e.g., 'Injection'. 
    - "ICD_Code": TEXT – International Classification of Diseases code for the diagnosis. 
    - "Competitor_Flag": INTEGER – Indicates if the product is from a competitor (1) or not (0). 
    - "Product_Group": TEXT – Group or category of the product, e.g., 'Targeted Therapy'. 
    - "Market_ID": TEXT – Identifier for the market. 
    - "Market_Name": TEXT – Name of the market, e.g., 'OVARIAN'. 
    - "Product_Days_of_Supply": INTEGER – Days of supply for the product. 
    - "SP_Bottles": REAL – Number of bottles from specialty pharmacy. This is bottle count that is shipped to the patient in that shipment by the SP. 
    - "SD_Bottles": INTEGER – Number of the specialty distribution bottles distributed or sold to the account. 
    - "Total_Bottles": REAL – Total number of bottles (SP and SD combined) 
    - "Days_of_Supply": TEXT – Total days of supply for the shipment. 
    - "Off_label_flag": TEXT – Indicates if the use is off-label, e.g., 'N' for no. 
    - "SP_ID": TEXT – Identifier for the specialty pharmacy. 
    - "SP_Name": TEXT – Name of the specialty pharmacy, e.g., 'CVS CAREMARK'. 
    - "SP_Location": TEXT – Location of the specialty pharmacy. 
    - "SD_ID": TEXT – Identifier for the specialty distributor. 
    - "SD_Location": TEXT – Location of the specialty distributor. 
    - "Week_Ending_Date": DATE – Closing date of the recorded week, marking the end of the data period. stored as a string in YYYY-MM-DD format. The last day of the week is considered as the Friday of that week. You can use this to extract information like the date, week, month and year of the data collection from this. Use this field if the question specifies a week, such as the latest week, recent week, or a specific week ending (e.g., 2024/13/6). 
    - "Week_Number": TEXT – Week number, e.g., 'W1-2024'. 
    - "Month": TEXT – Month of the shipment, e.g., 'Jan-24', 'Feb-25', 'Mar-24', 'Apr-24', 'Jun-25', 'Jul-24'. Use this field if the question specifies a month, such as the latest month, recent month, or a specific month (e.g., Jan 2024). 
    - "Quarter": TEXT – Denotes a three-month period within a fiscal year used for financial reporting, typically divided as Q1 (January-March), Q2 (April-June), Q3 (July-September), and Q4 (October-December). This field contains values such as Q1-2024, Q2-2024, Q3-2024, Q4-2024, Q1-2025, and so on. Use this field if the question specifies a quarter, such as the latest quarter, recent quarter, or a specific quarter (e.g., Q1-2024). 
    - "Year": INTEGER – Year of the shipment. Use this field if the question specifies a year, such as the latest year, recent year, or a specific year (e.g., 2024). 
    - "HCP_ID": TEXT – Unique identifier for the healthcare provider. HCP information is available only in SP data, so this field is populated only when the Shipment_type is SP. For SD records, it is shown as a dash (-). Dash represents that the record is from SP and no information is available. 
    - "NPI": TEXT – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits. HCP information is available only in SP data, so this field is populated only when the Shipment_type is SP. For SD records, it is shown as a dash (-). Dash represents that the record is from SP and no information is available. 
    - "HCP_Name": TEXT – Name of the healthcare professional. Terms like HCP, healthcare provider, doctor or MD are used synonymously with healthcare professionals. 
    - "HCP_Address": TEXT – Complete US address where the healthcare professional practices. 
    - "HCP_City": TEXT – City where the healthcare provider is located. 
    - "HCP_State": TEXT – State where the healthcare professional’s practice is located.This field contains the abbreviations for U.S. state names, such as NY for New York, FL for Florida, TX for Texas, CA for California, IL for Illinois, NC for North Carolina, ND for North Dakota, KY for Kentucky, NJ for New Jersey, NM for New Mexico, MT for Montana, WA for Washington, GA for Georgia, and so on. 
    - "HCP_ZIP": TEXT – US Postal code of the healthcare professional’s practice. These are postal codes are generally of 5 digits 
    - "HCP_Specialty": TEXT – Specialty of the healthcare provider, e.g., 'GYNECOLOGICAL ONCOLOGY'. This column identifies the area in which the HCP is certified, licensed, or primarily operates.  
    - "HCP_Specialty_Group": TEXT – Group of the specialty. Include "FM/IM" for Family Medicine/Internal Medicine, "NP/PA" for Nurse Practitioner/Physician Assistant, "Oncs" for Oncologists, "PCP" for Primary Care Physicians, and "Others" for all other specialties not separately listed. 
    - "HCP_Decile": TEXT – Decile ranking of the healthcare provider. 
    - "HCP_Segment": TEXT – Segment classification of the healthcare provider, e.g., 'L'. 
    - "Target_Flag": TEXT – Indicates if the healthcare provider is a target, e.g., 'Y' or 'N'. 
    - "AMA_Flag": TEXT – American Medical Association flag, possibly indicating membership or status. 
    - "PDRP_Flag": TEXT – Flag for participation in a program, possibly related to data sharing or privacy. 
    - "KOL": TEXT – Indicates if the healthcare provider is a Key Opinion Leader, e.g., 'Y' or 'N'.  
    - "Email": TEXT – Email address of the healthcare provider. 
    - "Phone_number": TEXT – Phone number of the healthcare provider. 
    - "Territory_ID": TEXT – Identifier for the sales territory. 
    - "Territory_Name": TEXT – Name of the sales territory, e.g., 'Syracuse-Albany'. The territory refers to a specific geographical area assigned in which the sales representatives operate. A group of ZIPs forms a territory. All ZIPs within a territory can be found in the L3_ZTT table. 
    - "Region_ID": TEXT – Identifier for the region. 
    - "Region_Name": TEXT – Name of the region, e.g., 'New England'. A group of Territories forms a Region. 
    - "Area_ID": TEXT – Identifier for the area. 
    - "Area_Name": TEXT – Name of the area, e.g., 'East'. A group of regions forms an Area. 
    - "Rep_Name": TEXT – Name of the sales representative. 
    - "Rep_Rank": TEXT – Rank or position of the sales representative. 
    - "Rep_Vacancy": INTEGER – Indicates if the representative position is vacant (1) or not (0) on Shipment date. 
    - "Primary_Payer_ID": TEXT – Identifier for the primary insurance payer. 
    - "Primary_Payer_Name": TEXT – Name of the primary insurance payer, e.g., 'Hamaspik Choice'. 
    - "Primary_Payer_Channel": TEXT – Categorization of the insurance types (Commercial, Medicare, Medicaid, Others) of  primary payer. 
    - "Primary_Plan_ID": TEXT – Identifier for the primary insurance plan. 
    - "Primary_Plan_Name": TEXT – Name of the primary insurance plan, e.g., 'Hamaspik Choice Plan'. 
    - "Secondary_Payer_ID": TEXT – Identifier for the secondary insurance payer. 
    - "Secondary_Payer_Name": TEXT – Name of the secondary insurance payer, e.g., 'California Health'. 
    - "Secondary_Payer_Channel": TEXT – Categorization of the insurance types (Commercial, Medicare, Medicaid, Others) of secondary payer.   
    - "Secondary_Plan_ID": TEXT – Identifier for the secondary insurance plan. 
    - "Secondary_Plan_Name": TEXT – Name of the secondary insurance plan, e.g., 'California Health Plan'. 
    - "New_Account_Flag": INTEGER – Indicates whether the account has sold an SP bottle for the first time. 
    - "Account_ID": INTEGER – Unique identifier for the account. 
    - "Account_Name": TEXT – Identifies the Account name through which the healthcare product was sold. Terms such as Hospital or L1 are used synonymously with the term Account. e.g., 'ROSWELL PARK COMPREHENSIVE CANCER CENTER'.  
    - "Account_Address": TEXT – The primary US street address of the account's main location. 
    - "Account_City": TEXT – US City where the account is located. 
    - "Account_State": TEXT – The US state in which the account operates. This field contains the abbreviations for state names, for example, NY for New York, FL for Florida and so on.   
    - "Account_ZIP": INTEGER – US Postal code for the account's location, essential for regional analysis. These postal codes are generally of 5 digits.   
    - "Account_CoT": TEXT – Class of Trade which categorizes the type of business operation (e.g., Hospital, Clinic). 
    - "Account_Decile": INTEGER – Decile ranking of the account. 
    - "Account_Segment": TEXT – Segment classification of the account, e.g., 'L'. 
    - "SP_Gross": REAL – Gross sales for the SP bottles in US dollars. 
    - "SD_Gross": INTEGER – Gross sales for the SD bottles in US dollars. 
    - "Total_Gross": REAL– Total gross sales in US dollars, from the total bottles (SP and SD combined). 
    - "SP_Net": REAL – Net sales after deductions, reflecting the actual earnings from product sales for the SP bottles in US dollars. 
    - "SD_Net": INTEGER – Net sales in US dollars after deductions, reflecting the actual earnings from the SD bottles sold to the account. 
    - "Total_Net": REAL – Total net sales in Us Dollars after deductions, reflecting the actual earnings from product sales. 

        """, 

 

"L2_Calls_Transaction_Summary_Table_v2": """Stores detailed information about sales representative calls or interactions with healthcare providers, capturing call details, promoted products, healthcare provider information, employee details, and geographical hierarchy to support sales activity tracking, marketing analysis, and territory management in a healthcare or pharmaceutical context. 
    Here is the schema information of the Table along with descriptions of each column: 
    - "Call_Detail_ID": TEXT – Unique identifier for the call detail record. Single Call_Detail_ID can have multiple Call_ID.  
    - "Call_ID": TEXT – Unique identifier for the call. 
    - "Call_date": DATE – Date when the call or interaction occurred. 
    - "Product_ID": TEXT – Unique identifier for the promoted product. 
    - "Product_Name": TEXT – Name of the promoted product, e.g., ' Onc_Brand_A’. 
    - "Product_Description": TEXT – Description of the product, e.g., 'AROMATASE INHIB'. 
    - "Dosage_Form": TEXT – Form of the dosage, e.g., 'Injection'. 
    - "Competitor_Flag": INTEGER – Indicates if the product is from a competitor (1) or not (0). 
    - "Product_Group": TEXT – Group or category of the product, e.g., 'Targeted Therapy'. 
    - "Product_Days_of_Supply": INTEGER – Days of supply for the product. 
    - "Market_ID": TEXT – Identifier for the market. 
    - "Market_Name": TEXT – Name of the market, e.g., 'OVARIAN'. 
    - "Priority": TEXT – Priority level of the call, e.g., 'P1'. 
    - "Indication": TEXT – Medical indication for the product, e.g., 'ER/PR+' or 'BRCA1/BRCA'. 
    - "Audience": TEXT – Target audience for the call, e.g., 'Front desk'. 
    - "Interaction_focus": TEXT – Focus of the interaction, e.g., 'Promotional'. 
    - "Call_type": TEXT – Type of call, e.g., 'In-person' or 'Virtual'. 
    - "HCP_ID": TEXT – Unique identifier for the healthcare provider. 
    - "NPI": INTEGER – National Provider Identifier for the healthcare provider. 
    - "HCP_Name": TEXT – Name of the healthcare professional. Terms like HCP, healthcare provider, doctor or MD are used synonymously with healthcare professionals. 
    - "HCP_Address": TEXT – Complete US address where the healthcare professional practices. 
    - "HCP_City": TEXT – US City where the healthcare provider is located. 
    - "HCP_State": TEXT – US State where the healthcare professional’s practice is located. This field contains the abbreviations for U.S. state names, such as NY for New York, FL for Florida, TX for Texas, CA for California, IL for Illinois, NC for North Carolina, ND for North Dakota, KY for Kentucky, NJ for New Jersey, NM for New Mexico, MT for Montana, WA for Washington, GA for Georgia, and so on.  
    - "HCP_ZIP": INTEGER – US Postal code of the healthcare professional’s practice. These are postal codes are generally of 5 digits.  
    - "HCP_Specialty": TEXT – Specialty of the healthcare provider, e.g., 'GYNECOLOGICAL ONCOLOGY'. This column identifies the area in which the HCP is certified, licensed, or primarily operates. 
    - "HCP_Specialty_Group": TEXT – Group of the specialty. Include "FM/IM" for Family Medicine/Internal Medicine, "NP/PA" for Nurse Practitioner/Physician Assistant, "Oncs" for Oncologists, "PCP" for Primary Care Physicians, and "Others" for all other specialties not separately listed. 
    - "HCP_Decile": INTEGER – Decile ranking of the healthcare provider. 
    - "HCP_Segment": TEXT – Segment classification of the healthcare provider, e.g., 'L' or 'M'. 
    - "Target_Flag": TEXT – Indicates if the healthcare provider is a target, e.g., 'Y' or 'N'. 
    - "AMA_Flag": TEXT – American Medical Association flag, possibly indicating membership or status. 
    - "PDRP_Flag": TEXT – Flag for participation in a program, possibly related to data sharing or privacy. 
    - "KOL": TEXT – Indicates if the healthcare provider is a Key Opinion Leader, e.g., 'Y' or 'N'.  
    - "Email": TEXT – Email address of the healthcare provider. 
    - "Phone_number": INTEGER – Phone number of the healthcare provider. 
    - "Emp_ID": TEXT – Unique identifier for the employee making the call. 
    - "Emp_Name": TEXT – Name of the employee. 
    - "Emp_Role": TEXT – Role of the employee, e.g., 'Sales Representative'. 
    - "Emp_Email": TEXT – Email address of the employee. 
    - "Territory ID": TEXT – Identifier for the sales territory. 
    - "Territory_Name": TEXT – Specifies the sales or operational territory of the account. The territory is used synonymously with "Region" and refers to a specific geographical area assigned in which the sales representatives operate, e.g., 'South Jersey'.  
    - "Region_ID": TEXT – Identifier for the region. 
    - "Region_Name": TEXT – Name of the region, e.g., 'Atlantic Coastal'. 
    - "Area_ID": TEXT – Identifier for the area. 
    - "Area_Name": TEXT – Name of the area, e.g., 'East'. 
    - "Week_Ending_Date": DATE – Closing date of the recorded week, marking the end of the data period. stored as a string in MM-DD-YYYY format. The last day of the week is considered as the Friday of that week. You can use this to extract information like the date, week, month and year of the data collection from this. Use this field if the question specifies a week, such as the latest week, recent week, or a specific week ending (e.g., 6/13/2024). 
    - "Week_Number": TEXT – Week number, e.g., 'W1-2024'. 
    - "Month": TEXT – Month of the shipment, e.g., 'Jan-2024', 'Feb-2025', 'Mar-2024', 'Apr-2024', 'Jun-2025', 'Jul-2024'. Use this field if the question specifies a month, such as the latest month, recent month, or a specific month (e.g., Jan 2024). 
    - "Quarter": TEXT – Denotes a three-month period within a fiscal year used for financial reporting, typically divided as Q1 (January-March), Q2 (April-June), Q3 (July-September), and Q4 (October-December). This field contains values such as Q1-2024, Q2-2024, Q3-2024, Q4-2024, Q1-2025, and so on. Use this field if the question specifies a quarter, such as the latest quarter, recent quarter, or a specific quarter (e.g., Q1-2024). 
    - "Year": INTEGER – Year of the shipment. Use this field if the question specifies a year, such as the latest year, recent year, or a specific year (e.g., 2024). 
    """
    # , 

 

# "L2_HCP_Events_Table_v2": """Stores detailed information about events involving healthcare providers, such as speaker programs, capturing event details, healthcare provider participation, geographical hierarchy, and time dimensions to support marketing analysis, event tracking, and territory management in a healthcare or pharmaceutical context. 
#     Here is the schema information of the Table along with descriptions of each column: 
#    - "Record_ID": TEXT – Unique identifier for the event record.  
#     - "Event": TEXT – Name or type of the event, e.g., 'Speaker Program'. We should filter the table on this column based on the event of interest. 
#     - "Event_ID": TEXT – Unique identifier for the event.  
#     - "NPI": INTEGER – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits.   
#     - "Date": DATE– Date when the event occurred.  
#     - "Week_Ending_Date": DATE – Closing date of the recorded week, marking the end of the data period. stored as a string in MM-DD-YYYY format. The last day of the week is considered as the Friday of that week. You can use this to extract information like the date, week, month and year of the data collection from this.   
#     - "Week_Number": TEXT – Week number, e.g., 'W1-2024'.  
#     - "Month": TEXT – Month of the event, e.g., 'Jan-24'. Use this field if the question specifies a month, such as the latest month, recent month, or a specific month (e.g., Jan 2024).  
#     - "Quarter": TEXT – Denotes a three-month period within a fiscal year used for financial reporting, typically divided as Q1 (January-March), Q2 (April-June), Q3 (July-September), and Q4 (October-December). This field contains values such as Q1-2024, Q2-2024, Q3-2024, Q4-2024, Q1-2025, and so on. Use this field if the question specifies a quarter, such as the latest quarter, recent quarter, or a specific quarter (e.g., Q1 2024). 
#     - "Quarter_Start_Date": DATE – Start date of the quarter.  
#     - "Quarter_End_Date": DATE – End date of the quarter.  
#     - "Year": INTEGER – Year of the event. Use this field if the question specifies a year, such as the latest year, recent year, or a specific year (e.g., 2024).  
#     - "Channel": TEXT – Channel through which the event was conducted, if applicable. Channel Information is available only in Email and Digital Campaigns, so this field is populated only when the Event is ‘Email Campaign’ or ‘Digital Campaign’. For Speaker Program records, it is shown as a blank.  
#     - "Engagement_type": TEXT – Type of engagement, if specified. This Information is available only in Email and Digital Campaigns, so this field is populated only when the Event is ‘Email Campaign’ or ‘Digital Campaign’. For Speaker Program records, it is shown as a blank. 
#     - "Publisher": TEXT – Publisher or organizer of the event, if applicable. Publisher Information is available only in Email and Digital Campaigns, so this field is populated only when the Event is ‘Email Campaign’ or ‘Digital Campaign’. For Speaker Program records, it is shown as a blank. 
#     - "Speaker_Name": TEXT – Name of the speaker at the event, e.g., 'Ethan Lee'. This Information is available only in Speaker Program, so this field is populated only when the Event is ‘Speaker Program’. For other records, it is shown as a blank.  
#     - "Event_Type": TEXT – Type of event, e.g., 'In-Person'. This Information is available only in Speaker Program, so this field is populated only when the Event is ‘Speaker Program’. For other records, it is shown as a blank. 
#     - "Event_City": TEXT – City where the event took place. This Information is available only in Speaker Program, so this field is populated only when the Event is ‘Speaker Program’. For other records, it is shown as a blank. 
#     - "Event_State": TEXT – State where the event took place. This Information is available only in Speaker Program, so this field is populated only when the Event is ‘Speaker Program’. For other records, it is shown as a blank.  
#     - "HCP_ID": TEXT – Unique identifier for the healthcare provider.  
#     - "HCP_Name": TEXT – Name of the healthcare professional. Terms like HCP, healthcare provider, doctor or MD are used synonymously with healthcare professionals.   
#     - "HCP_Address": TEXT – Complete US address where the healthcare professional practices.    
#     - "HCP_City": TEXT – US City where the healthcare provider is located.  
#     - "HCP_State": TEXT – US State where the healthcare professional's practice is located. This field contains the abbreviations for U.S. state names, such as NY for New York, FL for Florida, TX for Texas, CA for California, IL for Illinois, NC for North Carolina, ND for North Dakota, KY for Kentucky, NJ for New Jersey, NM for New Mexico, MT for Montana, WA for Washington, GA for Georgia, and so on.  
#     - "HCP_ZIP": INTEGER – US Postal code of the healthcare professional's practice. These are postal codes are generally of 5 digits   
#     - "HCP_Specialty": TEXT – Medical specialty of the healthcare professional, helping to understand the areas of expertise. This column identifies the area in which the HCP is certified, licensed, or primarily operates. 
#     - "HCP_Specialty_Group": TEXT – Group of the specialty, e.g., 'Oncs' for oncologists. Include "FM/IM" for Family Medicine/Internal Medicine, "NP/PA" for Nurse Practitioner/Physician Assistant, "Oncs" for Oncologists, "PCP" for Primary Care Physicians, and "Others" for all other specialties not separately listed. 
#     - "HCP_Decile": INTEGER – Decile ranking of the healthcare provider.  
#     - "HCP_Segment": TEXT – Segment classification of the healthcare provider, e.g., 'L' or 'H'.  
#     - "Target_Flag": TEXT – Indicates if the HCP is identified as a target for the sales representatives to call on or reach. Eg. Y or N. 
#     - "AMA_Flag": TEXT – American Medical Association flag, possibly indicating membership or status. 
#     - "PDRP_Flag": TEXT – Flag for participation in a program, possibly related to data sharing or privacy. 
#     - "KOL": TEXT – Indicates if the healthcare provider is a Key Opinion Leader, e.g., 'Y' or 'N'.  
#     - "Email": TEXT – Email address of the healthcare provider. 
#     - "Phone_number": INTEGER – Phone number of the healthcare provider. 
#     - "Territory_ID": TEXT – Identifier for the sales territory.  
#     - "Territory_Name": TEXT – Specifies the sales or operational territory of the account. The territory is used synonymously with "Region" and refers to a specific geographical area assigned in which the sales representatives operate, e.g., 'Springfield-Providence'.  
#     - "Region_ID": TEXT – Identifier for the region.  
#     - "Region_Name": TEXT – Name of the region, e.g., 'New England'.  
#     - "Area_ID": TEXT – Identifier for the area.  
#     - "Area_Name": TEXT – Name of the area, e.g., 'East'.  
#     """, 

 

# "L2_Patient_Status_Summary_Table_v2": """Stores detailed information about patient status updates, capturing patient demographics, status details, specialty pharmacy information, prescriber source, and time dimensions to support patient care tracking, referral management, and status monitoring in a healthcare or pharmaceutical context. 
#     Here is the schema information of the Table along with descriptions of each column: 
#     - "Record_ID": TEXT – Unique identifier for the status record.  
#     - "Patient_ID": INTEGER – Unique identifier for the patient.  
#     - "Gender": TEXT – Gender of the patient, e.g., 'Male' or 'Female'.  
#     - "Age": INTEGER – Age of the patient.  
#     - "Birth_Year": INTEGER – Year of birth of the patient.  
#     - "SP_ID": TEXT – Identifier for the specialty pharmacy, if applicable.  
#     - "SP_Name": TEXT – Name of the specialty pharmacy, if applicable.  
#     - "Status_Date": DATE Date when the status was updated.  
#     - "Week_Ending_Date": DATE – Closing date of the recorded week, marking the end of the data period. stored as a string in MM-DD-YYYY format. The last day of the week is considered as the Friday of that week. You can use this to extract information like the date, week, month and year of the data collection from this.   
#     - "Week_Number": TEXT – Week number, e.g., 'W47-2023'.  
#     - "Month": TEXT – Month of the status update, e.g., 'Nov-23'. Use this field if the question specifies a month, such as the latest month, recent month, or a specific month (e.g., Jan 2024).  
#     - "Quarter": TEXT – Denotes a three-month period within a fiscal year used for financial reporting, typically divided as Q1 (January-March), Q2 (April-June), Q3 (July-September), and Q4 (October-December).  This field contains values such as Q1-2024, Q2-2024, Q3-2024, Q4-2024, Q1-2025, and so on. Use this field if the question specifies a quarter, such as the latest quarter, recent quarter, or a specific quarter (e.g., Q1 2024). 
#     - "Quarter_Start_Date": DATE– Start date of the quarter.  
#     - "Quarter_End_Date": DATE End date of the quarter.  
#     - "Year": INTEGER – Year of the status update. Use this field if the question specifies a year, such as the latest year, recent year, or a specific year (e.g., 2024). 
#     - "Prescriber_Source": TEXT – Source of the prescription, e.g., 'Hub'.  
#     - "Status": TEXT – Current status of the patient, e.g., 'Pending'.  
#     - "Status_Code": TEXT – Code representing the status, e.g., 'P100'.  
#     - "Status_Description": TEXT – Description of the status, e.g., 'REFERRAL CREATED'.  
#   """, 

 

# "L3_Enrollment_Table_v2": """Stores detailed information about patient enrollments, including enrollment dates, prescriber details, diagnosis codes, product information, prescription status, and payer details to support patient care tracking, prescription management, and financial analysis in a healthcare or pharmaceutical context. 
# Here is the schema information of the Table along with descriptions of each column: 
#     -"Enrollment_ID": TEXT – Unique identifier for the enrollment record.   
#     - "Patient_ID": INTEGER – Unique identifier for the patient.   
#     - "Enrollment_Date": DATE– Date when the patient was enrolled.   
#     - "NPI": INTEGER – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits.  
#     - "Prescriber_Source": TEXT – Source of the prescription, such as 'PRESCRIBER' or 'HUB'.   
#     - "ICD_Code": TEXT – International Classification of Diseases code for the diagnosis.   
#     - "Product_ID": TEXT – Unique identifier for the product.   
#     - "Product_Name": TEXT – Name of the product, e.g., 'Onc_Brand_A'.   
#     - "NDC": TEXT – National Drug Code for the product.  
#     - "Off_label_flag": TEXT – Indicates if the use is off-label, e.g., 'N' for no.   
#     - "Rx_No": TEXT – Prescription number, often hashed or encrypted for privacy.   
#     - "Authorized_Refills": INTEGER – Number of authorized refills for the prescription.   
#     - "Status": TEXT – Current status of the enrollment, e.g., 'Active'.   
#     - "Status_Code": TEXT – Code representing the status, e.g., 'PA0301' or 'A01'.   
#     - "Status_Description": TEXT – Description of the status, e.g., 'ACTIVE:ON THERAPY:SHIPMENT CONFIRMED' or 'Order Shipped'.   
#     - "Status_Date": TEXT – Date when the status was updated.   
#     - "Primary_Payer_ID": INTEGER – Identifier for the primary insurance payer.   
#     - "Primary_Payer_Name": TEXT – Name of the primary insurance payer, e.g., 'Hamaspik Choice'.  
#     - "Primary_Payer_Channel": TEXT – Categorization of the insurance types (Commercial, Medicare, Medicaid, Others) of primary payer.  
#     - "Primary_Copay": INTEGER – Copay amount for the primary payer.   
#     - "Primary_OOP": INTEGER – Out-of-pocket amount for the primary payer.   
#     - "Secondary_Payer_ID": INTEGER – Identifier for the secondary insurance payer.   
#     - "Secondary_Payer_Name": TEXT – Name of the secondary insurance payer, e.g., 'California Health'.   
#     - "Secondary_Payer_Channel": TEXT – Categorization of the insurance types (Commercial, Medicare, Medicaid, Others) of secondary payer.  
#     - "Secondary_Copay": INTEGER – Copay amount for the secondary payer.   
#     - "Secondary_OOP": INTEGER – Out-of-pocket amount for the secondary payer.  
#     """, 

 

# "L3_Geography_v2": """Stores hierarchical geographical information defining areas, regions, and territories for sales and distribution purposes, supporting territory management, sales reporting, and resource allocation. 
#     Here is the schema information of the Table along with descriptions of each column: 
#     - "Area_ID": TEXT – Unique identifier for the area.  
#     - "Area_Name": TEXT – Name of the area, e.g., 'East'.  
#     - "Region_ID": TEXT – Unique identifier for the region within the area.  
#     - "Region_Name": TEXT – Name of the region, e.g., 'Kentucky'.   
#     - "Territory_ID": TEXT – Unique identifier for the territory within the region.  
#     - "Territory_Name": TEXT – Specifies the sales or operational territory of the account. The territory is used synonymously with "Region" and refers to a specific geographical area assigned in which the sales representatives operate, e.g., 'Atlanta'. 
# """, 

# "L3_HCO_Master_v2": """Stores detailed information about healthcare organizations or accounts, including identifiers, addresses, classifications, and segmentation data to support account management, sales targeting, and reporting. 
# Here is the schema information of the Table along with descriptions of each column: 
#     - "Account_ID": INTEGER – Unique identifier for the account.   
#     - "Account_Name": TEXT – Identifies the Account name through which the healthcare product was sold. Terms such as Hospital or L1 are used synonymously with the term Account., e.g., 'ABDUL G. MUNDIA PHYSICIAN'.   
#     - "Account_Address": TEXT – The primary US street address of the account's main location.  
#     - "Account_City": TEXT – US City where the account is located.   
#     - "Account_State": TEXT – US state in which the account operates. This field contains the abbreviations for state names, for example, NY for New York, FL for Florida and so on.  
#     - "Account_ZIP": INTEGER – US Postal code for the account's location, essential for regional analysis. These postal codes are generally of 5 digits.  
#     - "Account_CoT": TEXT – Class of Trade which categorizes the type of business operation (e.g., Hospital, Clinic).    
#     - "Account_Decile": INTEGER – Decile ranking of the account, possibly indicating size or importance.   
#     - "Account_Segment": TEXT – Segment classification of the account, e.g., 'L'.  
# """, 

# "L3_HCP_Master_v2": """Stores detailed information about healthcare providers, including identifiers, contact details, specialties, segmentation, flags for program participation or statuses, and Key Opinion Leader status to support HCP management, sales targeting, and marketing analysis in a healthcare or pharmaceutical context. 
# Here is the schema information of the Table along with descriptions of each column: 
#     - "HCP_ID": TEXT – Unique identifier for the healthcare provider.  
#     - "NPI": INTEGER – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits.  
#     - "HCP_Name": TEXT – Name of the healthcare professional. Terms like HCP, healthcare provider, doctor or MD are used synonymously with healthcare professionals.  e.g., 'PAUL TIMOTHY MORRIS'.  
#     - "HCP_Address": TEXT – Address of the healthcare provider.  
#     - "HCP_City": TEXT – US City where the healthcare provider is located.  
#     - "HCP_State": TEXT – State where the healthcare provider is located, e.g., 'HI'.  
#     - "HCP_ZIP": INTEGER – US Postal code of the healthcare professional's practice. These are postal codes are generally of 5 digits.  
#     - "HCP_Specialty": TEXT – This column identifies the area in which the HCP is certified, licensed, or primarily operates.   
#     - "HCP_Specialty_Group": TEXT – Group of the specialty. Include "FM/IM" for Family Medicine/Internal Medicine, "NP/PA" for Nurse Practitioner/Physician Assistant, "Oncs" for Oncologists, "PCP" for Primary Care Physicians, and "Others" for all other specialties not separately listed.   
#     - "HCP_Decile": INTEGER - Decile ranking of the healthcare provider.  
#     - "HCP_Segment": TEXT – Segment classification of the healthcare provider, e.g., 'M'.  
#     - "Target_Flag": TEXT – Indicates if the HCP is identified as a target for the sales representatives to call on or reach. Eg. Y or N  
#     - "AMA_Flag": TEXT – American Medical Association flag, possibly indicating membership or status.  
#     - "PDRP_Flag": TEXT – Flag for participation in a program, possibly related to data sharing or privacy.  
#     - "Email": TEXT – Email address of the healthcare provider.  
#     - "Phone_number": INTEGER – Phone number of the healthcare provider.  
#     - "KOL": TEXT – Indicates if the healthcare provider is a Key Opinion Leader, e.g., 'Y' or 'N'.  
#     """, 

 

# "L3_ICD_Mapping_v2": """Stores mappings of ICD codes to their descriptions and associated market names for medical diagnosis categorization. 
# Here is the schema information of the Table along with descriptions of each column: 
# - "ICD_Code": TEXT – International Classification of Diseases code. 
# - "Description": TEXT – Description of the ICD code, e.g., 'MALIGNANT NEOPLASM OF LEFT FALLOPIAN TUBE'. 
# - "Market_Name": TEXT – Name of the market associated with the ICD code, e.g., 'OVARIAN'. 

# """, 

 

# "L3_Inventory_Table_v2": """Stores inventory data, including levels, receipts, and shipments for products at specific locations, identified by NDC and location IDs. 
# Here is the schema information of the Table along with descriptions of each column: 
#     - "Week_Ending_Date": DATE – Closing date of the recorded week, marking the end of the data period. stored as a string in MM-DD-YYYY format. The last day of the week is considered as the Friday of that week. You can use this to extract information like the date, week, month and year of the data collection from this.  
#     - "SP_SD_ID": TEXT – Unique identifier for the specialty pharmacy or specialty distributor. 
#     - "NDC": TEXT – National Drug Code for the product.  
#     - "SP_SD_Location": TEXT – Location of the specialty pharmacy or specialty distributor.  
#     - "SP_SD_Inventory": REAL – Total inventory of the specified healthcare product available at the specialty pharmacy and specialty distributor in the week across all territories.  
#     - "Qty_Received":– REAL Quantity of product received during the week.  
#     - "Qty_Shipped": – REAL Quantity of product shipped during the week 
# """, 

 

# "L3_Patient_Level_Master_v2": """Stores demographic information about patients, including gender, age, and birth year. 
# Here is the schema information of the Table along with descriptions of each column: 
# - "Patient_ID": INTEGER – Unique identifier for the patient. 
# - "Gender": TEXT – Gender of the patient, e.g., 'Male', 'Female'. 
# - "Age": INTEGER – Age of the patient. 
# - "Birth_Year": INTEGER – Year of birth of the patient. 
# """, 

 

# "L3_Payer_Master_v2": """Stores information about insurance payers, including their names and the channels they operate in. 
# Here is the schema information of the Table along with descriptions of each column: 
# - "Payer_ID": INTEGER – Unique identifier for the payer. 
# - "Payer_Name": TEXT – Name of the payer, e.g., 'Advanced Health'. 
# - "Payer_Channel": TEXT – Channel of the payer, e.g., 'Commercial', 'Medicaid'. 
# """, 

# "L3_Plan_Master_v2": """Stores details about insurance plans offered by payers, including plan IDs, names, and the number of covered lives. 
# Here is the schema information of the Table along with descriptions of each column: 
# - "Payer_Name": TEXT – Name of the payer offering the plan. 
# - "Plan_ID": TEXT – Unique identifier for the plan. 
# - "Plan_Name": TEXT – Name of the plan, e.g., 'Advanced Health Plan'. 
# - "Covered_lives": INTEGER – Number of insured individuals covered under the payer.    
# """, 

 

# "L3_Product_Master_v2": """Stores catalog information about products, including their NDC, product IDs, names, descriptions, strengths, dosage forms, and market information. 
# Here is the schema information of the Table along with descriptions of each column: 
#     - "NDC": TEXT – National Drug Code for the product. 
#     - "Product_ID": TEXT – Unique identifier for the product. 
#     - "Product_Name": TEXT – Name of the product, e.g., 'Product_X'. 
#     - "Product_Description": TEXT – Description of the product, e.g., 'AROMATASE INHIB'. 
#     - "Strength": TEXT – Strength of the product, e.g., '5 ml'. 
#     - "Dosage_Form": TEXT – Form of the dosage, e.g., 'Injection'. 
#     - "Competitor_Flag": INTEGER – Indicates if the product is from a competitor (1) or not (0). 
#     - "Product_Group": TEXT – Group or category of the product, e.g., 'Targeted Therapy'. 
#     - "Market_ID": TEXT – Identifier for the market. 
#     - "Market_Name": TEXT – Name of the market, e.g., 'OVARIAN'. 
#     - "Product_Days_of_Supply": INTEGER – Days of supply for the product. 

# """, 

# "L3_Roster_v2": """Stores detailed information about employee assignments to geographical areas, including employee details, roles, and dates related to employment and vacancies. 
# Here is the schema information of the Table along with descriptions of each column: 
#     - "Geo_level": TEXT – The level of geography, such as 'National'. 
#     - "Geo_ID": TEXT – Unique identifier for the geographical area. 
#     - "Geo_Name": TEXT – Name of the geographical area, e.g., 'East'. 
#     - "Emp_ID": TEXT – Unique identifier for the employee. 
#     - "Emp_Name": TEXT – Name of the employee. 
#     - "Emp_Role": TEXT – Role of the employee, e.g., 'NSD'. 
#     - "Emp_Email": TEXT – Email address of the employee. 
#     - "Emp_Start_date": DATE – Start date of the employee's assignment. 
#     - "Emp_End_date": DATE – End date of the employee's assignment, if applicable. 
#     - "IC_Start_Date": DATE – Start date for incentive compensation, if applicable. 
#     - "IC_End_Date": DATE – End date for incentive compensation, if applicable. 
#     - "Vacancy_Start_date": DATE – Start date of a vacancy period. 
#     - "Vacancy_End_date": DATE – End date of a vacancy period. 
#     - "Data_feed_date": DATE – Date when the data was fed or updated. 

# """, 

 

# "L3_SD_Master_v2": """Stores detailed information about specialty distributors, including their identifiers and locations. 
# Here is the schema information of the Table along with descriptions of each column: 
# - "SD_ID": TEXT – Unique identifier for the specialty distributor. 
# - "SD_Location": TEXT – Location of the specialty distributor. 
# """, 

 

# "L3_SD_Shipment_Table_v2": """Stores detailed information about shipments from standard distributors, capturing shipment and invoice details, product information, and account details. 
# Here is the schema information of the Table along with descriptions of each column: 
# - "Shipment_ID": INTEGER – Unique identifier for the shipment. 
# - "Shipment_Date": DATE – Date when the shipment was sent. 
# - "Invoice_ID": TEXT – Identifier for the invoice associated with the shipment. 
# - "Invoice_Date": DATE – Date of the invoice. 
# - "Product_ID": TEXT – Unique identifier for the product. 
# - "Product_Name": TEXT – Name of the product. 
# - "NDC": TEXT – National Drug Code for the product. 
# - "SD_Bottles": INTEGER – Number of the SD bottles distributed or sold to the account. 
# - "Account_ID": INTEGER – Unique identifier for the account. 
# - "Account_Name": TEXT – Identifies the Account name through which the healthcare product was sold. Terms such as Hospital or L1 are used synonymously with the term Account. 
# - "SD_ID": TEXT – Identifier for the specialty distributor. 
# - "SD_Location": TEXT – Location of the specialty distributor. 
# """, 

 

# "L3_SP_Master_v2": """Stores detailed information about specialty pharmacies, including their identifiers, names, and locations. 
# Here is the schema information of the Table along with descriptions of each column: 
# - "SP_ID": TEXT – Unique identifier for the specialty pharmacy. 
# - "SP_Name": TEXT – Name of the specialty pharmacy. 
# - "SP_Location": TEXT – Location of the specialty pharmacy. 
# """, 

 

# "L3_SP_Shipment_Table_v2": """Stores detailed information about shipments from specialty pharmacies, capturing patient and prescriber details, product information, and payer information. 
#     Here is the schema information of the Table along with descriptions of each column: 
#     - "Shipment_ID": INTEGER – Unique identifier for the shipment. 
#     - "Shipment_Date": DATE – Date when the shipment was sent. 
#     - "First_Shipment_Date": DATE – Date of the first shipment for the patient or prescription. 
#     - "New_Patient_Flag": INTEGER – Indicates if the patient is new (1) or existing (0). 
#     - "Patient_ID": INTEGER – Unique identifier for the patient. 
#     - "HCP_ID": TEXT – Unique identifier for the healthcare provider. 
#     - "NPI": INTEGER – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits.  
#     - "Rx_No": TEXT – Prescription number. 
#     - "Prescriber_Source": TEXT – Source of the prescription, e.g., 'PRESCRIBER', 'HUB'. 
#     - "SP_Bottles": REAL – Number of bottles shipped from the specialty pharmacy. 
#     - "Days_of_Supply": INTEGER – Days of supply for the shipment. 
#     - "Authorized_Refills": INTEGER – Number of authorized refills. 
#     - "Fill_number": INTEGER – The fill number for the prescription. 
#     - "Off_label_flag": TEXT – Indicates if the use is off-label, e.g., 'N' for no. 
#     - "Product_ID": TEXT – Unique identifier for the product. 
#     - "Product_Name": TEXT – Name of the product. 
#     - "NDC": TEXT – National Drug Code for the product. 
#     - "ICD_Code": TEXT – International Classification of Diseases code. 
#     - "SP_ID": TEXT – Identifier for the specialty pharmacy. 
#     - "SP_Name": TEXT – Name of the specialty pharmacy. 
#     - "SP_Location": TEXT – Location of the specialty pharmacy. 
#     - "Primary_Payer_ID": INTEGER – Identifier for the primary insurance payer. 
#     - "Primary_Plan_ID": TEXT – Identifier for the primary insurance plan. 
#     - "Secondary_Payer_ID": INTEGER – Identifier for the secondary insurance payer. 
#     - "Secondary_Plan_ID": TEXT – Identifier for the secondary insurance plan. 

# """, 

 

# "L3_Target_and_Free_Sample_v2": """Stores detailed information about sales targets and free samples distributed, associated with territories and time periods. 
# Here is the schema information of the Table along with descriptions of each column: 
#     - "Territory_ID": TEXT – Unique identifier for the territory.  
#     - "Territory_Name": TEXT – Specifies the sales or operational territory of the account. The territory is used synonymously with "Region" and refers to a specific geographical area assigned in which the sales representatives operate.  
#     - "Week_Ending_Date": DATE Closing date of the recorded week, marking the end of the data period. stored as a string in MM-DD-YYYY format. The last day of the week is considered as the Friday of that week. You can use this to extract information like the date, week, month and year of the data collection from this.  
#     - "Target_new_patients": INTEGER – Target number of new patients.  
#     - "Total_Target_patients": INTEGER – Total target number of patients.  
#     - "Target_Bottles": INTEGER – Target number of bottles.  
#     - "Free_samples": INTEGER – Number of free samples distributed during the week to the HCPs in the specified territory, often used as a promotional tactic.    
#     - "Target_Gross_Sales": INTEGER – Gross sales for the Target bottles in US dollars. 
#     - "Target_Net_Sales": INTEGER – Net sales after deductions, reflecting the actual earnings from product sales for the target bottles in US dollars . 
# """,  

 

# "L3_Time_v2": """Stores a time dimension with various date-related attributes, including week, month, quarter, and year. 
#     Here is the schema information of the Table along with descriptions of each column: 
#     - "Date": DATE The specific date.  
#     - "Week_Ending_Date": DATE date of the recorded week, marking the end of the  
#     data period. stored as a string in MM-DD-YYYY format. The last day of the week is  
#     considered as the Friday of that week. You can use this to extract information like the  
#     date, week, month and year of the data collection from this.  
#     - "Week_Number": TEXT – Week number, e.g., 'W1-2010'.  
#     - "Month": TEXT – Month of the shipment, e.g., 'January-2024', 'February-2025', 'March-2024', 'April-2024', 'June-2025', 'July-2024'. Use this field if the question specifies a month, such as the latest month, recent month, or a specific month (e.g., Jan 2024). 
#     - "Quarter": TEXT – Denotes a three-month period within a fiscal year used for financial reporting, typically divided as Q1 (January-March), Q2 (April-June), Q3 (July-September), and Q4 (October-December). This field contains values such as Q1-2024, Q2-2024, Q3-2024, Q4-2024, Q1-2025, and so on.  Use this field if the question specifies a quarter, such as the latest quarter, recent quarter, or a specific quarter (e.g., Q1 2024). 
#     - "Quarter_Start_Date": DATE Start date of the quarter.  
#     - "Quarter_End_Date": DATE End date of the quarter.  
#     - "Year": INTEGER – Year of the shipment. Use this field if the question specifies a year, such as the latest year, recent year, or a specific year (e.g., 2024). 

# """,  

 

# "L3_ZTT_Table_v2": """Stores detailed information mapping ZIP codes to territories, regions, and areas, providing a geographical hierarchy. 
# Here is the schema information of the Table along with descriptions of each column: 
#     - "ZIP": INTEGER – ZIP code.  
#     - "State": TEXT – State abbreviation.  
#    - "City": TEXT – City name.  
#     - "Territory_ID": TEXT – Unique identifier for the territory.  
#     - "Territory_Name": TEXT –Specifies the sales or operational territory of the account. The  
#     territory is used synonymously with "Region" and refers to a specific geographical area  
#     assigned in which the sales representatives operate.  
#     - "Region_ID": TEXT – Unique identifier for the region.  
#     - "Region_Name": TEXT – Name of the region.  
#     - "Area_ID": TEXT – Unique identifier for the area.  
#     - "Area_Name": TEXT – Name of the area.  
# """,   

 

# "L3_Call_Detail_Table_v2": """Stores detailed information about specific call details, capturing products discussed during sales representative interactions with healthcare providers, including call identifiers, dates, priorities, medical indications, and product details to support sales activity tracking and product promotion analysis in a healthcare or pharmaceutical context. 
#     Here is the schema information of the Table along with descriptions of each column: 
#     - "Call_Detail_ID": TEXT – Unique identifier for the call detail record. 
#     - "Call_ID": TEXT – Unique identifier for the call, linking to the parent call record. 
#     - "Call_Date": DATE – Date when the call or interaction occurred. 
#     - "Priority": TEXT – Priority level of the call, e.g., 'P1'. 
#     - "Indication": TEXT – Medical indication for the product discussed, e.g., 'ER/PR+' or 'BRCA1/BRCA'. 
#     - "Product_ID": TEXT – Unique identifier for the product discussed. 
#     - "Product_Name": TEXT – Name of the product discussed, e.g., 'Onc_Brand_A'. 
#     """, 

 

# "L3_Call_Table_v2": """Stores information about sales representative calls to healthcare providers, capturing call identifiers, dates, employee and healthcare provider details, geographical territories, audience, interaction focus, call type, and market information to support sales activity tracking, territory management, and marketing analysis in a healthcare or pharmaceutical context. 
#     Here is the schema information of the Table along with descriptions of each column: 
#     - "Call_ID": TEXT – Unique identifier for the call. 
#     - "Call_date": DATE – Date when the call or interaction occurred. 
#     - "Territory ID": TEXT – Identifier for the sales territory. 
#     - "Emp_ID": TEXT – Unique identifier for the employee making the call. 
#     - "Emp_Name": TEXT – Name of the employee, e.g., 'Michelle Rivera'. 
#     - "NPI": INTEGER – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits. 
#     - "HCP_Name": TEXT – Name of the healthcare professional. Terms like HCP, healthcare provider, doctor or MD are used synonymously with healthcare professionals. e.g., 'BRIAN KEITH TURPIN'.  
#     - "HCP_State": TEXT – State where the healthcare provider is located, e.g., 'OH'. 
#     - "Decile": INTEGER – Decile ranking of the healthcare provider. 
#     - "Audience": TEXT – Target audience for the call, e.g., 'MD'. 
#     - "Interaction_focus": TEXT – Focus of the interaction, e.g., 'Educational'. 
#     - "Call_Type": TEXT – Type of call, e.g., 'Virtual'. 
#     - "Market_ID": TEXT – Identifier for the market. 
#     - "Market_Name": TEXT – Name of the market, e.g., 'OVARIAN'. 
#     """, 
 

# "L3_Digital_Campaigns_v2": """Stores information about digital marketing campaigns targeting healthcare providers, capturing campaign event identifiers, healthcare provider identifiers, dates, engagement types, and publisher details to support digital marketing analysis and campaign performance tracking in a healthcare or pharmaceutical context. 
#     Here is the schema information of the Table along with descriptions of each column: 
#     - "Record_ID": TEXT – Unique identifier for the campaign record. 
#     - "Event_ID": TEXT – Unique identifier for the digital campaign event. 
#     - "NPI": INTEGER – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits.   
#     - "Date": DATE – Date when the engagement occurred. 
#     - "Engagement_type": TEXT – Type of engagement, e.g., 'Impression' or 'Click'. 
#     - "Publisher": TEXT – Name of the publisher or platform, e.g., 'Pulse Point'. 
#     - "Channel": TEXT – Channel used for the campaign, e.g., 'Display'. 
#     """, 

 

# "L3_Email_Campaigns_v2": """Stores information about email marketing campaigns targeting healthcare providers, capturing campaign event identifiers, healthcare provider identifiers, dates, engagement types, channels, and publisher details to support email marketing analysis and campaign performance tracking in a healthcare or pharmaceutical context. 
#    Here is the schema information of the Table along with descriptions of each column: 
#     - "Record_ID": TEXT – Unique identifier for the email campaign record. 
#     - "Date": DATE – Date when the engagement occurred. 
#     - "NPI": INTEGER – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits. 
#     - "Channel": TEXT – Channel used for the campaign, e.g., 'Email'. 
#     - "Engagement_Type": TEXT – Type of engagement, e.g., 'Sent' or 'Open'. 
#     - "Publisher": TEXT – Name of the publisher or platform, e.g., 'ASCO'. 
#     - "Event_ID": TEXT – Unique identifier for the email campaign event. 
#    """, 

 

# "L3_Speaker_Program_v2": """Stores information about speaker programs involving healthcare providers, capturing event details, speaker names, event types, locations, and healthcare provider identifiers to support event tracking, marketing analysis, and speaker program management in a healthcare or pharmaceutical context. 

 

# Here is the schema information of the Table along with descriptions of each column: 
# - "Record_ID": TEXT – Unique identifier for the speaker program record. 
# - "Event_Date": TEXT – Date when the speaker program occurred. 
# - "Speaker_Program_ID": TEXT – Unique identifier for the speaker program event. 
# - "Speaker_Name": TEXT – Name of the speaker, e.g., 'Ethan Lee'. 
# - "Event_Type": TEXT – Type of event, e.g., 'In-Person'. 
# - "Event_City": TEXT – City where the event took place, e.g., 'Boston'. 
# - "Event_State": TEXT – State where the event took place, e.g., 'Massachusetts'. 
# - "NPI": INTEGER – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits.   

# """, 

 

# "L3_Patient_Status_table_v2": """Stores detailed information about patient status tracking and progression, capturing status updates, prescriber sources, specialty pharmacy assignments, and comprehensive status codes to support patient care monitoring, referral management, and care coordination tracking in a healthcare or pharmaceutical context.  
#     Here is the schema information of the Table along with descriptions of each column:  
#         - "Record_ID": TEXT – Unique identifier for each status record, e.g., 'R1000001'.  
#         - "Patient_ID": INTEGER – Unique identifier for the patient, e.g., '1000001'.  
#         - "SP_ID": TEXT – Identifier for the specialty pharmacy, if applicable, e.g., 'SP00001'. Can be empty for certain status types.  
#         - "Status_Date": DATE Date when the status was recorded or updated, e.g., '11/19/2023'.  
#         - "Prescriber_Source": TEXT – Source of the prescription or referral, e.g., 'Hub', 'Prescriber'.  
#         - "Status": TEXT – Current status category of the patient, e.g., 'Pending', 'Active', 'Discontinued', 'Cancelled'.  
#         - "Status_Code": TEXT – Specific code representing the detailed status, e.g., 'P100', 'PA0301', 'A01', 'DC23'.  
#        - "Status_Description": TEXT – Detailed description of the status, e.g., 'REFERRAL REFERRAL CREATED', 'ACTIVE:ON THERAPY:SHIPMENT CONFIRMED', 'Order Shipped', 'Patient Choice - Other'.  

#         """, 

 

# "L3_Competitor_Table_v2":""" 
# Stores detailed information about the usage of competitor products by healthcare providers, including the number of patients using competitor products, new prescriptions (NBRx), and patients new to therapy, aggregated by quarter and week. This table supports competitive analysis, market share tracking, and sales strategy development in a healthcare or pharmaceutical context. 
#     Here is the schema information of the Table along with descriptions of each column: 
#     - Quarter: TEXT – Denotes a three-month period within a fiscal year used for financial reporting, typically divided as Q1 (January-March), Q2 (April-June), Q3 (July-September), and Q4 (October-December), e.g., 'Q1-2024'. This field contains values such as Q1-2024, Q2-2024, Q3-2024, Q4-2024, Q1-2025, and so on. Use this field if the question specifies a quarter, such as the latest quarter, recent quarter, or a specific quarter (e.g., Q1 2024). 
#    - Week_Ending_Date: DATE – Closing date of the recorded week, marking the end of the data period. stored as a string in YYYY-MM-DD  format. The last day of the week is considered as the Friday of that week. You can use this to extract information like the date, week, month and year of the data collection from this. 
#     - NPI: INTEGER – Unique identifier for each healthcare professional as per the National Provider Identifier standard. The NPI ID is generally of 10 digits, e.g., '1003023045'. 
#     - Num_Patients_Competitor_Products: INTEGER – Number of patients using competitor products prescribed by the healthcare provider during the specified week, e.g., '18'. 
#     - NBRx: INTEGER – Number of new prescriptions written for competitor products by the healthcare provider during the specified week, e.g., '8'. 
#     - New_to_Therapy: INTEGER – Number of patients who are new to therapy with competitor products during the specified week, e.g., '4'. """ 

 

} 

def get_metadata(table_names):
    """
    Retrieve table metadata for given tables.
    
    Args:
        table_names (list): List of table names to get metadata for
        
    Returns:
        str: Formatted metadata section with table descriptions
    """
    # Create metadata section for the provided tables
    metadata_section = "\n".join(
        [f"{table}: {table_descriptions[table]}" for table in table_names if table in table_descriptions]
    )
    
    return metadata_section

def get_additional_business_info():
    """Return the additional business information metadata"""
    return additional_business_info

def get_table_descriptions():
    """Return the table descriptions dictionary"""
    return table_descriptions
