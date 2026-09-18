import sqlite3
import pandas as pd

# 1. Load the data and connect to a local SQL database
df = pd.read_csv('stratified_funnel_data.csv')
conn = sqlite3.connect('ecommerce_analytics.db')

# 2. Upload the dataframe into the SQL database as a table named 'events'
df.to_sql('events', conn, if_exists='replace', index=False)

# 3. Write the actual SQL query
sql_query = """
    SELECT 
        event_type,
        COUNT(DISTINCT user_session) as unique_sessions
    FROM 
        events
    GROUP BY 
        event_type
    ORDER BY 
        unique_sessions DESC;
"""

# 4. Execute the SQL query and print the results
sql_results = pd.read_sql_query(sql_query, conn)
print("--- SQL Funnel Analysis Results ---")
print(sql_results.to_string(index=False))

# Close the connection
conn.close()
