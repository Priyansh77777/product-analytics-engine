import pandas as pd
import numpy as np
import gc

files = ['2019-Oct.csv', '2019-Nov.csv', '2019-Dec.csv', '2020-Jan.csv', '2020-Feb.csv']
cols = ['event_time', 'event_type', 'product_id', 'category_code', 'user_id', 'user_session']
master_df = []

for file in files:
    print(f"Processing {file}...")
    # Only load necessary columns to save RAM
    df = pd.read_csv(file, usecols=cols)
    
    unique_sessions = df['user_session'].dropna().unique()
    
    # Sample 30k sessions (or max available)
    sample_size = min(30000, len(unique_sessions))
    sampled_sessions = np.random.choice(unique_sessions, size=sample_size, replace=False)
    
    # Filter and append
    filtered_df = df[df['user_session'].isin(sampled_sessions)]
    master_df.append(filtered_df)
    
    # Force garbage collection to free RAM for the next 500MB file
    del df
    gc.collect()

# Combine all months
final_df = pd.concat(master_df, ignore_index=True)
final_df.to_csv('stratified_funnel_data.csv', index=False)

print(f"Processing Complete.")
print(f"Final Dataframe Shape: {final_df.shape}")
print(f"Total Unique Sessions Sampled: {final_df['user_session'].nunique()}")
