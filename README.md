# AdventureWorks Sales & Customer Analytics Platform

**End-to-End Data Analytics | SQL · Power BI · Python · Databricks · PySpark · AWS S3 · Airflow**

## Project Overview

**Adventure Works Cycles** is the fictional bicycle manufacturing company represented in Microsoft's **AdventureWorks** sample database.

The company manufactures and sells bicycles and related products across multiple geographic markets. Its operations include customers, products, sales orders, salespeople, sales territories, manufacturing, and other business functions.

For this project, I focused on the **sales and commercial side of the business**, using AdventureWorks data to analyze:

- Sales and revenue performance
- Customer value and purchasing behavior
- Customer retention and churn risk
- Product and category performance
- Geographic sales performance
- Salesperson performance
- Customer segmentation

I built an **end-to-end analytics platform** that transforms raw AdventureWorks operational data into analytics-ready datasets and interactive Power BI dashboards.

The solution combines **SQL, Power BI, dimensional modeling, Python, AWS S3, Databricks, PySpark, Delta Lake, and Apache Airflow** to simulate how a modern organization could transform operational sales data into business intelligence.

> **Goal:** Help Adventure Works understand what drives revenue, who its most valuable customers are, which products and territories perform best, and where opportunities exist to improve commercial performance.

---

# Business Scenario

Adventure Works operates in the bicycle industry, selling products across different categories, customers, territories, and markets.

As the company grows, analyzing commercial performance directly from operational data becomes increasingly difficult.

Management needs a consolidated analytical view capable of answering questions such as:

- Is revenue growing or declining?
- Which products generate the most sales?
- Which product categories contribute the most revenue?
- Who are the company's most valuable customers?
- Which customers are becoming inactive?
- Which customer groups should receive more attention?
- Which territories are growing fastest?
- Which salespeople outperform their regional benchmarks?
- Are there seasonal patterns affecting bicycle sales?
- Which products are frequently purchased together?

This project transforms the underlying operational data into a structured **analytics environment** designed to answer these questions.

---

# Business Questions

The analysis focuses on four major areas of commercial performance.

### Sales Performance

- How is revenue changing over time?
- What is the month-over-month growth rate?
- Which months generate the strongest sales?
- Are there identifiable seasonal sales patterns?
- Which days of the week generate stronger sales?

### Customer Analytics

- Who are the highest-value customers?
- How much revenue do top customers contribute?
- Which customers are at risk of churn?
- Which customers have become inactive?
- How frequently do different customer groups purchase?
- How can customers be segmented according to purchasing behavior?

### Product Analytics

- Which bicycle and product categories generate the most revenue?
- Which products consistently perform well?
- Which products are frequently purchased together?
- Which high-revenue products have relatively low margins?
- How does product performance change over time?

### Sales Organization

- Which sales territories generate the most revenue?
- Which territories are growing or declining year over year?
- Which salespeople generate the most revenue?
- Which salespeople outperform the average performance of their territory?

---

# Power BI Dashboards

The final Power BI solution contains **six analytical dashboard pages**, each designed around a different business area.

---

## 1. Executive Sales Dashboard

![Executive Sales Dashboard](docs/dashboards/executive_sales_dashboard.png)

The Executive Sales Dashboard provides a high-level view of Adventure Works' overall commercial performance.

### Analysis Included

- Monthly revenue trends
- Month-over-month revenue growth
- Sales trend classification
- Sales performance by day of the week
- Seasonal sales patterns

### Business Purpose

This dashboard allows management to quickly understand how the bicycle business is performing over time and identify periods of growth, decline, or unusual sales behavior.

It provides the starting point for deeper investigation into customers, products, territories, and salespeople.

---

## 2. Customer Analytics

![Customer Analytics](docs/dashboards/customer_analytics.png)

The Customer Analytics dashboard evaluates the value and purchasing behavior of Adventure Works customers.

### Analysis Included

- Top customers by lifetime revenue
- Customer lifetime value
- Cumulative revenue contribution
- Customer churn-risk distribution
- Customers inactive during the last 12 months
- Average purchase interval
- Customer behavioral segmentation

### Business Purpose

Not every customer contributes equally to revenue.

This analysis helps Adventure Works identify its **highest-value customers** while also detecting customers whose purchasing activity has declined.

These insights could support:

- Customer retention initiatives
- Re-engagement campaigns
- Account prioritization
- CRM segmentation
- Personalized marketing strategies

---

## 3. Product Analytics

![Product Analytics](docs/dashboards/product_analytics.png)

The Product Analytics dashboard evaluates the performance of Adventure Works' bicycle and related product portfolio.

### Analysis Included

- Revenue by product category
- Category contribution to total revenue
- Top products by month
- Product performance over time
- Frequently purchased product combinations
- High-revenue products with relatively low margins

### Business Purpose

This analysis helps the business understand **which products actually drive commercial performance**.

The insights can support decisions related to:

- Product portfolio strategy
- Pricing
- Inventory planning
- Cross-selling
- Product bundling
- Merchandising
- Margin optimization

The frequently purchased product analysis can also reveal opportunities to recommend complementary products to customers.

---

## 4. Sales Territory Analysis

![Sales Territory](docs/dashboards/sales_territory.png)

Adventure Works sells products across multiple geographic territories.

This dashboard compares commercial performance across those markets.

### Analysis Included

- Revenue by sales territory
- Territory contribution to sales
- Year-over-year revenue growth
- Current-year vs. previous-year revenue
- Identification of growing and declining territories

### Business Purpose

Geographic analysis helps management understand where the company is performing strongly and where commercial performance may require attention.

This can support decisions involving:

- Regional sales strategy
- Territory prioritization
- Resource allocation
- Market expansion
- Sales targets

---

## 5. Salesperson Performance

![Salesperson Performance](docs/dashboards/salesperson_performance.png)

The Salesperson Performance dashboard evaluates individual sales representatives and compares their results with their respective territories.

### Analysis Included

- Revenue by salesperson
- Territory average revenue
- Salesperson vs. territory benchmark
- Identification of above-average performers

### Business Purpose

Comparing salespeople only by total revenue can be misleading because territories have different levels of opportunity.

This analysis introduces a regional benchmark so individual performance can be evaluated in the context of the salesperson's territory.

It helps identify:

- High-performing representatives
- Underperforming representatives
- Territory-specific performance differences
- Potential coaching or best-practice opportunities

---

## 6. Customer Segmentation

![Customer Segmentation](docs/dashboards/customer_segmentation.png)

The Customer Segmentation dashboard uses **RFM Analysis** to classify customers according to their purchasing behavior.

### RFM Framework

**Recency**  
How recently did the customer purchase?

**Frequency**  
How often does the customer purchase?

**Monetary Value**  
How much revenue has the customer generated?

Customers receive scores based on these dimensions and are grouped into meaningful behavioral segments.

### Analysis Included

- Customer distribution by RFM segment
- Revenue generated by customer segment
- Customer value distribution
- Customer segment progression

### Business Purpose

RFM segmentation converts raw transaction history into actionable customer groups.

Adventure Works could use these segments to support:

- Targeted marketing
- Customer retention
- Loyalty strategies
- Re-engagement campaigns
- High-value customer prioritization
- CRM personalization

---

# SQL Business Analysis

The project goes beyond basic reporting by creating business-focused analytical models in SQL.

The SQL analytical layer answers questions related to customers, products, sales trends, territories, and salespeople.

### Sales Analysis

- Monthly revenue trends
- Month-over-month revenue growth
- Weekday sales patterns
- Seasonal sales patterns

### Customer Analysis

- Top customers by lifetime value
- Cumulative customer revenue contribution
- Customer churn risk
- Inactive customers
- Average purchase interval
- RFM customer segmentation
- Customer segment progression

### Product Analysis

- Revenue by product category
- Category percentage contribution
- Top products by month
- Frequently purchased product combinations
- High-revenue / low-profit products

### Territory & Salesperson Analysis

- Revenue by territory
- Territory year-over-year growth
- Current-year vs. previous-year performance
- Salesperson revenue
- Salesperson vs. territory-average performance

---

# SQL Techniques Used

The analytical models demonstrate practical SQL skills commonly required in Data Analyst and BI Analyst roles.

```text
CTEs
Window Functions
LAG()
LEAD()
DENSE_RANK()
NTILE()
CASE Expressions
Self Joins
Subqueries
Aggregations
Date Functions
GROUP BY
HAVING
JOINs
```

These techniques are used to solve business problems rather than only demonstrate SQL syntax.

---

# Data Model

The analytical layer uses a **Star Schema** designed specifically for reporting and business analysis.

![Star Schema](docs/architecture/star_schema.png)

Operational AdventureWorks data is transformed into an analytics-ready dimensional model containing fact and dimension tables.

The model simplifies analytical queries and provides a clean structure for Power BI.

### Why a Star Schema?

The dimensional model provides:

- Simpler business queries
- Consistent dimensions across analyses
- Easier Power BI relationships
- Clear separation between dimensions and metrics
- Better analytical usability
- Scalable reporting structure

---

# End-to-End Architecture

![Architecture Diagram](docs/architecture/architecture_diagram.png)

The project simulates a modern cloud analytics workflow.

```text
AdventureWorks
Operational CSV Data
        │
        ▼
     AWS S3
   Raw Storage
        │
        ▼
Python Data Ingestion
        │
        ├── File Validation
        ├── Metadata Validation
        └── Logging
        │
        ▼
     Databricks
       PySpark
        │
        ▼
┌─────────────────────────┐
│      BRONZE LAYER       │
│        Raw Data         │
├─────────────────────────┤
│      SILVER LAYER       │
│   Cleaned & Validated   │
├─────────────────────────┤
│       GOLD LAYER        │
│      Star Schema        │
└─────────────────────────┘
        │
        ▼
   SQL Analytics
        │
        ▼
     Power BI
        │
        ▼
Business Insights
```

**Apache Airflow** orchestrates the workflow from ingestion through analytical processing.

![Airflow Pipeline](docs/architecture/airflow_pipeline.png)

---

# Technology Stack

| Area | Technologies |
|---|---|
| Data Analysis | SQL, Power BI |
| Business Intelligence | Power BI |
| Data Visualization | Power BI |
| Data Modeling | Star Schema, Dimensional Modeling |
| Programming | Python |
| Data Transformation | PySpark |
| Cloud Storage | AWS S3 |
| Data Platform | Databricks |
| Storage | Delta Lake |
| Data Governance | Unity Catalog |
| Pipeline Orchestration | Apache Airflow |
| Version Control | Git, GitHub |

---

# End-to-End Data Pipeline

## 1. Source Data

The project uses operational data derived from Microsoft's **AdventureWorks** dataset.

The dataset represents different areas of the bicycle company's operations, including:

- Customers
- People
- Products
- Product categories
- Product subcategories
- Sales orders
- Sales order details
- Salespeople
- Sales territories
- Employees
- Addresses
- States and provinces
- Countries and regions

These operational datasets form the foundation of the analytical platform.

---

## 2. AWS S3 — Raw Storage

Source files are stored in **AWS S3**, which acts as the cloud-based raw data layer.

This separates source storage from downstream processing and simulates a common cloud analytics architecture.

---

## 3. Python Data Ingestion

Python scripts manage the ingestion workflow.

The ingestion process includes:

- Source file extraction
- File validation
- Metadata validation
- Logging
- Upload to Databricks

This creates a repeatable ingestion process instead of relying on manual file movement.

---

## 4. Databricks Bronze Layer

Raw source data is loaded into the **Bronze Layer**.

The purpose of Bronze is to preserve source data with minimal transformation.

This provides:

- Raw-data traceability
- Reprocessing capability
- Separation between source and transformed data

---

## 5. Databricks Silver Layer

The **Silver Layer** cleans and standardizes the raw datasets using PySpark.

Transformations include:

- Data type conversion
- Null handling
- Data validation
- Column standardization
- Business-rule transformations
- Preparation for dimensional modeling

The result is a collection of reliable, cleaned datasets.

---

## 6. Databricks Gold Layer

The **Gold Layer** transforms cleaned data into a dimensional **Star Schema** optimized for analytics.

This layer provides business-ready fact and dimension tables that support SQL analysis and Power BI reporting.

---

## 7. SQL Analytics Layer

Advanced SQL models are built on top of the Gold Layer.

These models calculate business metrics and analytical datasets related to:

- Revenue
- Growth
- Customers
- Customer behavior
- Products
- Product combinations
- Territories
- Salespeople
- Seasonality

---

## 8. Power BI

Power BI consumes the analytics-ready data and presents the results through six business-focused dashboards:

1. Executive Sales Dashboard
2. Customer Analytics
3. Product Analytics
4. Sales Territory Analysis
5. Salesperson Performance
6. Customer Segmentation

The dashboards transform analytical outputs into visual information that business users can explore and use for decision-making.

---

## 9. Apache Airflow

Apache Airflow orchestrates the end-to-end workflow.

The pipeline coordinates the different stages of data ingestion and processing, reducing manual execution and demonstrating how an analytics workflow can be automated.

---

# Repository Structure

```text
AdventureWorks/
│
├── airflow/
│   └── dags/
│       └── adventureworks_pipeline.py
│
├── config/
│   ├── __init__.py
│   ├── config.py
│   └── logger.py
│
├── data/
│   └── raw/
│       ├── address/
│       ├── country_region/
│       ├── customer/
│       ├── employee/
│       ├── person/
│       ├── product/
│       ├── product_category/
│       ├── product_subcategory/
│       ├── sales_order_detail/
│       ├── sales_order_header/
│       ├── sales_person/
│       ├── sales_territory/
│       └── state_province/
│
├── databricks/
│   ├── 01_bronze.py
│   ├── 02_silver.py
│   ├── 03_gold.py
│   └── 04_sql_analytics.py
│
├── docs/
│   ├── architecture/
│   │   ├── airflow_pipeline.png
│   │   ├── architecture_diagram.png
│   │   └── star_schema.png
│   │
│   └── dashboards/
│       ├── customer_analytics.png
│       ├── customer_segmentation.png
│       ├── executive_sales_dashboard.png
│       ├── product_analytics.png
│       ├── sales_territory.png
│       └── salesperson_performance.png
│
├── ingestion/
│   ├── run_pipeline.py
│   └── scripts/
│       ├── __init__.py
│       ├── s3_extractor.py
│       └── upload_to_databricks_volume.py
│
├── powerbi/
│   └── AdventureWorksDashboard.pbix
│
├── scripts/
│   ├── __init__.py
│   ├── s3_extractor.py
│   └── upload_to_databricks_volume.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Skills Demonstrated

This project demonstrates practical skills relevant to **Junior Data Analyst and BI Analyst roles**.

### Data Analysis & Business Intelligence

- Translating business problems into analytical questions
- SQL business analysis
- Power BI dashboard development
- KPI analysis
- Trend analysis
- Month-over-month analysis
- Year-over-year analysis
- Customer lifetime value analysis
- Customer churn analysis
- RFM customer segmentation
- Product performance analysis
- Geographic sales analysis
- Salesperson performance analysis
- Data visualization
- Data storytelling

### Data Preparation & Modeling

- Data cleaning
- Data validation
- Data transformation
- Star Schema design
- Dimensional modeling
- Fact and dimension tables
- Analytics-ready data preparation

### Data Engineering

- Python-based data ingestion
- ETL pipeline development
- AWS S3
- Databricks
- PySpark transformations
- Delta Lake
- Medallion Architecture
- Apache Airflow orchestration

---

# Project Highlights

- Built an **end-to-end sales analytics platform** using Microsoft's AdventureWorks dataset
- Transformed operational bicycle sales data into actionable business insights
- Developed business-focused analytical models using **SQL**
- Designed an analytics-ready **Star Schema**
- Built **6 Power BI dashboard pages**
- Analyzed sales trends and month-over-month growth
- Evaluated customer lifetime value and churn risk
- Implemented **RFM customer segmentation**
- Analyzed bicycle and product category performance
- Identified frequently purchased product combinations
- Evaluated territory year-over-year growth
- Benchmarked salesperson performance against territory averages
- Implemented a **Bronze → Silver → Gold Medallion Architecture**
- Built automated ingestion workflows using **Python**
- Processed and transformed data using **PySpark and Databricks**
- Integrated **AWS S3** for cloud storage
- Orchestrated the workflow using **Apache Airflow**

---

# Future Improvements

Potential future improvements include:

- Incremental data loading
- Automated data-quality monitoring
- CI/CD with GitHub Actions
- Docker containerization
- Infrastructure as Code with Terraform
- Power BI Service deployment
- Automated dashboard refresh
- Additional customer cohort analysis

---

# About the Dataset

This project is based on Microsoft's **AdventureWorks** sample database.

AdventureWorks is designed to represent the operations of the fictional **Adventure Works Cycles** company and provides realistic relational data that can be used to practice database development, data analysis, data warehousing, and Business Intelligence.

For this portfolio project, I used the dataset as the foundation for a custom end-to-end analytics architecture focused specifically on **sales, customers, products, territories, and commercial performance**.

---

# About This Project

This project was developed as part of my data analytics portfolio to demonstrate how **SQL, Power BI, business analysis, and dimensional modeling** can be combined with modern data-engineering technologies to solve realistic business problems.

While the architecture demonstrates end-to-end data pipeline capabilities, the primary focus of the project is turning Adventure Works' bicycle sales data into **clear, actionable business insights** for decision-makers.
