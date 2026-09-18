import pandas as pd
import numpy as np

# 1. Load the funnel data
df = pd.read_csv('stratified_funnel_data.csv')

# 2. Pivot the data to get event counts per user
user_metrics = df.pivot_table(index='user_id', 
                              columns='event_type', 
                              values='event_time', 
                              aggfunc='count', 
                              fill_value=0).reset_index()

# Ensure all event columns exist even if some are 0
for col in ['view', 'cart', 'remove_from_cart', 'purchase']:
    if col not in user_metrics.columns:
        user_metrics[col] = 0

# 3. Define Segmentation Logic
def assign_cohort(row):
    if row['purchase'] > 0:
        return "High-Intent Buyers"
    elif row['cart'] > 0 and row['purchase'] == 0:
        return "Cart Abandoners"
    elif row['view'] > 2 and row['cart'] == 0:
        return "Window Shoppers"
    else:
        return "Bouncers (Low Engagement)"

# 4. Apply logic and calculate engagement score (total actions)
user_metrics['Cohort'] = user_metrics.apply(assign_cohort, axis=1)
user_metrics['Total_Interactions'] = user_metrics['view'] + user_metrics['cart'] + user_metrics['remove_from_cart'] + user_metrics['purchase']

# 5. Summarize the business impact
cohort_summary = user_metrics.groupby('Cohort').agg(
    Total_Users=('user_id', 'count'),
    Total_Engagement=('Total_Interactions', 'sum')
).reset_index()

cohort_summary['Engagement_Share (%)'] = (cohort_summary['Total_Engagement'] / cohort_summary['Total_Engagement'].sum() * 100).round(1)

# 6. Export for Power BI
user_metrics.to_csv('user_segments.csv', index=False)

print("Segmentation Complete. Data saved to 'user_segments.csv'.")
print("\n--- Business Impact Summary ---")
print(cohort_summary.sort_values(by='Total_Engagement', ascending=False).to_string(index=False))
