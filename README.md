📱 Smartphone Sales Data Engineering & Analytics

📊 Project at a Glance
Built an end-to-end SQL pipeline to analyze 1,200+ sales records. Designed a Star Schema to transform raw data into business insights.

![Market Analysis Dashboard](Dashboard (2).png)

🏗️ Database Architecture
Fact Table: fact_sales (Sales, Revenue, Profit)

Dimension Tables: dim_phones & dim_stores

Method: Star Schema (Optimized for Query Performance)

🛠️ Technical Highlights
Ranking: Used DENSE_RANK() to find the Top 3 models per store location.

Logic: Created CTEs and Views for a clean executive summary.

Automation: Developed a Stored Procedure to track sales vs. targets.

Data Seeding: Python script used to inject 1,200 records into MySQL.

💡 Key Business Metrics
Revenue & Profit Margin %

Store-wise Performance Status (Target vs. Actual)

Product Popularity Ranking
