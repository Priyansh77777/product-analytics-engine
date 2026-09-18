import sqlite3
import pandas as pd

conn = sqlite3.connect('ecommerce_analytics.db')

sql_query = """
    WITH UserMetrics AS (
        SELECT 
            user_id,
            SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) as purchases,
            SUM(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) as carts,
            SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) as views,
            COUNT(event_type) as total_interactions
        FROM events
        GROUP BY user_id
    ),
    Cohorts AS (
        SELECT 
            user_id,
            total_interactions,
            CASE 
                WHEN purchases > 0 THEN 'High-Intent Buyers'
                WHEN carts > 0 AND purchases = 0 THEN 'Cart Abandoners'
                WHEN views > 2 AND carts = 0 THEN 'Window Shoppers'
                ELSE 'Bouncers (Low Engagement)'
            END AS cohort
        FROM UserMetrics
    )
    SELECT 
        cohort,
        COUNT(user_id) as total_users,
        SUM(total_interactions) as total_engagement
    FROM Cohorts
    GROUP BY cohort
    ORDER BY total_engagement DESC;
"""

results = pd.read_sql_query(sql_query, conn)
results['engagement_share_pct'] = (results['total_engagement'] / results['total_engagement'].sum() * 100).round(1)

print("--- SQL Cohort Segmentation Results ---")
print(results.to_string(index=False))

conn.close()
