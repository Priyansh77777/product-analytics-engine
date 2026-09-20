# Product Analytics Engine: Funnel & Cohort Analysis

An enterprise-grade product analytics project built to process high-volume eCommerce event logs, track conversion funnels, segment behavioral cohorts, and identify critical UI/UX bottlenecks. This project moves from raw, memory-heavy event data to actionable product management strategies.

## Project Overview

Understanding user drop-off and engagement distribution is critical for product growth. This project analyzes 5 months of Cosmetics eCommerce event logs (originally ~2.5GB, 20M+ rows). By building a memory-efficient data pipeline, conducting SQL-based funnel analysis, and visualizing the outputs, this engine identifies exact points of user friction and quantifies the behavior of distinct user segments.

## Core Business Insights

* **Top-of-Funnel Drop-off:** There is a severe bottleneck between the `Cart` (32,595 unique sessions) and `Purchase` (5,091 unique sessions) stages. The absolute drop-off rate from Cart to Purchase is **84.4%**.
* **Cohort Discovery:** Behavioral segmentation revealed that **"Cart Abandoners"** (users who add to cart but record 0 purchases) make up only **16%** of the total user base, yet they generate a massive **52.8%** of all platform interactions.

## Product Strategy Recommendations

Based on the data, the following product interventions are proposed to recover lost revenue at the bottom of the funnel:

1. **1-Click Guest Checkout:** Reduce friction for the 84.4% of users abandoning their carts by minimizing mandatory form fields and account creation walls.
2. **Time-Delayed Exit-Intent Discounts:** Implement automated CRM triggers offering a 10% discount for carts that remain idle for >2 hours, specifically targeting the highly active "Cart Abandoners" cohort.

## Data Engineering & Analytics Pipeline

### 1. Data Engineering (`data_pipeline.py`)

Processing a 2.5GB dataset requires memory optimization. A Python/Pandas script was built to iterate through the raw CSV in chunks, forcing garbage collection (`gc.collect()`), and applying stratified sampling. This resulted in a statistically balanced dataset of 150,000 unique user sessions without exhausting local memory limits.

### 2. SQL Analytics (`sql_analytics.py` & `sql_cohorts.py`)

The sampled data is ingested into a local SQLite database (`ecommerce_analytics.db`).

* **Funnel Analysis:** Tracks unique sessions strictly across the AARRR funnel sequence (`View` → `Cart` → `Purchase`).
* **Cohort Segmentation:** Utilizes Common Table Expressions (CTEs) and `CASE WHEN` logic to group users into 4 distinct behavioral cohorts based on event frequencies and conversion history.

### 3. Executive Dashboarding (Power BI)

The exported datasets (`stratified_funnel_data.zip` and `user_segments.csv`) are modeled in **Power BI** to generate the final executive dashboard. This includes:

* A visual **Funnel Chart** tracking distinct session progression.
* Comparative **Donut Charts** mapping population size versus engagement share across user cohorts.

## Repository Structure

```text
product-analytics-engine/
│
├── data_pipeline.py             # Memory-efficient chunking and stratified sampling logic
├── sql_analytics.py             # SQL queries for tracking session-level conversion funnels
├── sql_cohorts.py               # SQL logic utilizing CTEs for behavioral segmentation
├── cohort_segmentation.py       # Python script for generating final segment aggregations
├── user_segments.csv            # Processed output: aggregated user cohorts
├── stratified_funnel_data.zip   # Processed output: compressed sample of funnel event logs
└── README.md                    # Project documentation

```

## Technologies Used

* **Python:** Pandas, memory management (`gc`), chunking operations.
* **SQL:** SQLite, CTEs, conditional aggregations.
* **Power BI:** Data visualization and executive dashboarding.
