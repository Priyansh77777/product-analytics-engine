
# Product Analytics Engine: Funnel & Cohort Analysis

A product analytics project built to process high-volume eCommerce event logs, analyze event-based conversion metrics, segment user behavior, and identify potential opportunities to improve the shopping experience.

## Project Overview

This project analyzes five months of Cosmetics eCommerce event logs (approximately 2.5 GB and 20M+ source records). A Python/Pandas pipeline selects relevant columns and samples sessions separately from each monthly file. The sampled event data is then analyzed using SQLite and SQL to calculate session-level event counts and segment users based on recorded behavior.

The analysis identifies a substantial gap between sessions with cart activity and sessions with purchase activity. Behavioral segmentation also highlights a sample-based cohort with a high share of recorded interactions relative to its population size. These observations inform proposed product experiments to investigate checkout friction and cart inactivity.

## Core Business Insights

- **Cart-to-Purchase Event-Count Gap:** The existing analysis reports 32,595 distinct sessions with cart events and 5,091 distinct sessions with purchase events. The difference is equivalent to an 84.4% gap relative to the cart-session count. The current SQL query counts sessions independently by event type and does not enforce chronological funnel progression, so this should not be interpreted as a verified sequential cart-abandonment rate.
- **Behavioral Cohort Discovery:** The existing cohort summary reports that "Cart Abandoners" account for 16% of observed users and 52.8% of recorded interactions in the analyzed sample. In the current implementation, this cohort consists of users with cart activity but no purchase recorded in the sampled event data. Because sessions are sampled before user-level aggregation, this classification may not reflect a user's complete purchase history.

## Product Strategy Recommendations

The following are hypotheses for further investigation and experimentation, not interventions whose impact has already been proven.

1. **Simplified Guest Checkout:** Investigate whether mandatory account creation, excessive form fields, or other checkout steps create unnecessary friction. If the evidence supports this hypothesis, test a simplified guest-checkout experience and measure completed-purchase conversion alongside relevant guardrail metrics.
2. **Cart-Idle Incentive Experiment:** Evaluate whether a targeted incentive can increase completed purchases among eligible sessions with cart activity. A 10% discount after more than two hours of inactivity is a proposed starting hypothesis, not an experimentally established optimal discount or timing threshold. Measure incremental purchases and profitability against an appropriate control group.

## Data Engineering & Analytics Pipeline

### 1. Data Processing (`data_pipeline.py`)

The pipeline processes five monthly CSV files separately, loads selected columns, samples up to 30,000 distinct non-null session IDs per month without replacement, and retains the event records associated with those selected sessions.

The intended sampling target is up to 150,000 sessions across the five months, subject to the availability of eligible sessions in each file. The sampled event records are combined into `stratified_funnel_data.csv` and can be compressed for storage.

The implementation reads each monthly file into a DataFrame; it does not use chunked CSV reading. It deletes the full monthly DataFrame and calls `gc.collect()` after filtering to help manage memory.

The sampling procedure applies a fixed target per month. Equal allocation does not necessarily preserve the original traffic proportions across months, and the current code does not set a random seed. The resulting sample should therefore be treated as an exploratory analysis dataset rather than assumed to be a statistically representative sample of the entire five-month population.

### 2. SQL Analytics (`sql_analytics.py` & `sql_cohorts.py`)

The sampled data is loaded into a local SQLite database named `ecommerce_analytics.db`.

- **Event-Type Session Analysis:** `sql_analytics.py` groups records by `event_type` and counts distinct `user_session` values. This provides the number of sessions associated with each event type. It does not enforce a chronological `View → Cart → Purchase` sequence or independently calculate a strict sequential funnel.
- **Cohort Segmentation:** `sql_cohorts.py` uses Common Table Expressions (CTEs), conditional aggregation and `CASE WHEN` rules to assign users to four mutually exclusive behavioral cohorts based on their recorded purchases, cart events and views.

The cohort classification is based on observed activity in the sampled event records. A user with no recorded purchase in the sample may still have purchased during a session that was not sampled.

### 3. Python Cohort Analysis (`cohort_segmentation.py`)

The Python script uses a pivot table to calculate event counts per user, applies the same four cohort rules, computes total recorded interactions, and exports user-level results to `user_segments.csv`.

The SQL and Python implementations provide complementary ways to analyze and summarize user behavior. Their cohort counts and interaction metrics should be reconciled before the findings are used for formal business reporting.

### 4. Planned Executive Dashboard (Power BI)

The processed datasets are intended for use in Power BI to create an executive dashboard with:

- A sequential funnel chart showing validated session progression and stage-to-stage conversion.
- Comparative charts showing cohort population share versus engagement share.
- Supporting metric definitions and notes on sample-based cohort classification.

The repository contains the data-processing scripts and exported datasets; the Power BI report file is not included in the current repository.

## Repository Structure

```text
product-analytics-engine/
│
├── data_pipeline.py
├── sql_analytics.py
├── sql_cohorts.py
├── cohort_segmentation.py
├── user_segments.csv
├── stratified_funnel_data.zip
└── README.md
```

## Technologies Used

- **Python:** Pandas, NumPy, garbage collection and data processing.
- **SQL:** SQLite, CTEs, conditional aggregation, grouping and distinct counts.
- **Data Analytics:** Funnel metrics, behavioral segmentation and engagement-share analysis.
- **Planned Visualization:** Power BI for executive reporting.
