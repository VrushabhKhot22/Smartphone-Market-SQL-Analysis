📱 Smartphone Sales Data Engineering & Analytics
🎯 Project Overview
This project simulates a real-world retail analytics environment. I designed a Star Schema database architecture, generated 1,200+ sales records using Python, and implemented advanced SQL scripts to track store performance and product rankings.

🏗️ Data Architecture (Star Schema)
To ensure optimized query performance, I implemented a dimensional model:

Fact Table: fact_sales (Orders, Quantity, Revenue, Profit)

Dimension Tables: dim_phones (Product specs), dim_stores (Location and Type)

🛠️ Advanced SQL Features
Data Modeling: Used Primary Keys and Foreign Keys to establish relationships between sales and products.

CTE & Window Functions: Used WITH clauses and DENSE_RANK() to identify the top 3 best-selling smartphone models per store location.

Stored Procedures: Built CheckStoreTarget to automate performance tracking against business targets.

Views: Created v_executive_summary to join multiple tables into a single source of truth for reporting.

Conditional Logic: Implemented CASE statements to categorize store performance status.

🚀 Automation
Python Integration: Used a Python script to programmatically populate the 1,200+ records into the database, ensuring realistic data distribution for analysis.
