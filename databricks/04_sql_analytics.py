# Databricks notebook source
# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 1
# MAGIC -- What are the monthly sales and month-over-month growth rate
# MAGIC -- over the last three years?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_monthly_sales_growth AS
# MAGIC
# MAGIC -- CTE: Calculate total sales for each month
# MAGIC WITH monthly_sales AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         d.Year,
# MAGIC         d.Month,
# MAGIC         CONCAT(d.Year, '-', LPAD(d.Month, 2, '0')) AS YearMonth,
# MAGIC
# MAGIC         -- Aggregation: Calculate monthly sales
# MAGIC         SUM(f.LineTotal) AS MonthlySales
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join date dimension to get year and month
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     -- Date Function: Keep only the last three years
# MAGIC     WHERE d.Year >= (
# MAGIC         SELECT MAX(Year) - 2
# MAGIC         FROM gold.dim_date
# MAGIC     )
# MAGIC
# MAGIC     -- GROUP BY: Aggregate sales by month
# MAGIC     GROUP BY
# MAGIC         d.Year,
# MAGIC         d.Month
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     Year,
# MAGIC     Month,
# MAGIC     YearMonth,
# MAGIC     MonthlySales,
# MAGIC
# MAGIC     -- Window Function + LAG():
# MAGIC     -- Get the previous month's sales
# MAGIC     LAG(MonthlySales) OVER (
# MAGIC         ORDER BY Year, Month
# MAGIC     ) AS PreviousMonthSales,
# MAGIC
# MAGIC     -- Calculate month-over-month growth percentage
# MAGIC     ROUND(
# MAGIC         (
# MAGIC             MonthlySales -
# MAGIC             LAG(MonthlySales) OVER (
# MAGIC                 ORDER BY Year, Month
# MAGIC             )
# MAGIC         ) * 100.0
# MAGIC         /
# MAGIC         LAG(MonthlySales) OVER (
# MAGIC             ORDER BY Year, Month
# MAGIC         ),
# MAGIC         2
# MAGIC     ) AS MoMGrowthRate
# MAGIC
# MAGIC FROM monthly_sales;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_monthly_sales_growth
# MAGIC
# MAGIC -- Show results in chronological order
# MAGIC ORDER BY
# MAGIC     Year,
# MAGIC     Month;
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 2
# MAGIC -- Which product categories contribute the highest percentage
# MAGIC -- of total revenue each year?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View  
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_category_revenue_percentage AS
# MAGIC
# MAGIC -- CTE: Calculate total revenue by category and year
# MAGIC WITH category_sales AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         d.Year,
# MAGIC         p.Category,
# MAGIC
# MAGIC         -- Aggregation: Calculate total revenue
# MAGIC         SUM(f.LineTotal) AS TotalRevenue
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join product dimension to get category
# MAGIC     JOIN gold.dim_product p
# MAGIC         ON f.ProductKey = p.ProductKey
# MAGIC
# MAGIC     -- Join date dimension to get year
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate revenue by year and category
# MAGIC     GROUP BY
# MAGIC         d.Year,
# MAGIC         p.Category
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     Year,
# MAGIC     Category,
# MAGIC     TotalRevenue,
# MAGIC
# MAGIC     -- Window Function + Percentage Calculation:
# MAGIC     -- Calculate each category's share of yearly revenue
# MAGIC     ROUND(
# MAGIC         TotalRevenue * 100.0 /
# MAGIC         SUM(TotalRevenue) OVER (PARTITION BY Year),
# MAGIC         2
# MAGIC     ) AS RevenuePercentage
# MAGIC
# MAGIC FROM category_sales;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_category_revenue_percentage
# MAGIC
# MAGIC -- Sort categories by highest revenue percentage each year
# MAGIC ORDER BY
# MAGIC     Year,
# MAGIC     RevenuePercentage DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 3
# MAGIC -- Who are the top 20 customers by lifetime value, and what
# MAGIC -- percentage of total company revenue do they represent?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_top_20_customers_lifetime_value AS
# MAGIC
# MAGIC -- CTE: Calculate lifetime revenue for each customer
# MAGIC WITH customer_revenue AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         c.CustomerKey,
# MAGIC         c.CustomerName,
# MAGIC
# MAGIC         -- Aggregation: Calculate lifetime revenue
# MAGIC         SUM(f.LineTotal) AS LifetimeRevenue
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join customer dimension to get customer name
# MAGIC     JOIN gold.dim_customer c
# MAGIC         ON f.CustomerKey = c.CustomerKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate revenue by customer
# MAGIC     GROUP BY
# MAGIC         c.CustomerKey,
# MAGIC         c.CustomerName
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     CustomerKey,
# MAGIC     CustomerName,
# MAGIC     LifetimeRevenue,
# MAGIC
# MAGIC     -- Window Function + Percentage Calculation:
# MAGIC     -- Calculate each customer's percentage of total company revenue
# MAGIC     ROUND(
# MAGIC         LifetimeRevenue * 100.0 /
# MAGIC         SUM(LifetimeRevenue) OVER (),
# MAGIC         2
# MAGIC     ) AS RevenuePercentage,
# MAGIC
# MAGIC     -- Window Function:
# MAGIC     -- Calculate the cumulative revenue percentage
# MAGIC     ROUND(
# MAGIC         SUM(LifetimeRevenue) OVER (
# MAGIC             ORDER BY LifetimeRevenue DESC
# MAGIC             ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
# MAGIC         ) * 100.0
# MAGIC         /
# MAGIC         SUM(LifetimeRevenue) OVER (),
# MAGIC         2
# MAGIC     ) AS CumulativeRevenuePercentage
# MAGIC
# MAGIC FROM customer_revenue;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_top_20_customers_lifetime_value
# MAGIC
# MAGIC -- Show the top 20 customers by lifetime revenue
# MAGIC ORDER BY
# MAGIC     LifetimeRevenue DESC
# MAGIC
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 4
# MAGIC -- Which customers have not purchased anything in the last
# MAGIC -- 12 months but were previously active?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_inactive_customers_last_12_months AS
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     c.CustomerKey,
# MAGIC     c.CustomerName
# MAGIC
# MAGIC FROM gold.dim_customer c
# MAGIC
# MAGIC -- Subquery:
# MAGIC -- Return only customers who have made at least one purchase
# MAGIC WHERE EXISTS (
# MAGIC
# MAGIC     SELECT 1
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     WHERE f.CustomerKey = c.CustomerKey
# MAGIC
# MAGIC )
# MAGIC
# MAGIC -- NOT EXISTS:
# MAGIC -- Exclude customers who purchased during the last 12 months
# MAGIC AND NOT EXISTS (
# MAGIC
# MAGIC     SELECT 1
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     WHERE f.CustomerKey = c.CustomerKey
# MAGIC
# MAGIC     -- Date Function:
# MAGIC     -- Keep purchases made in the last 12 months
# MAGIC     AND TO_DATE(CAST(d.DateKey AS STRING), 'yyyyMMdd') >= DATEADD(
# MAGIC         MONTH,
# MAGIC         -12,
# MAGIC         (
# MAGIC             SELECT MAX(
# MAGIC                 TO_DATE(CAST(DateKey AS STRING), 'yyyyMMdd')
# MAGIC             )
# MAGIC             FROM gold.dim_date
# MAGIC         )
# MAGIC     )
# MAGIC
# MAGIC );
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_inactive_customers_last_12_months
# MAGIC
# MAGIC -- Sort customers alphabetically
# MAGIC ORDER BY
# MAGIC     CustomerName;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 5
# MAGIC -- Which products consistently rank in the Top 10 by monthly
# MAGIC -- revenue?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_top_10_monthly_products AS
# MAGIC
# MAGIC -- CTE: Calculate monthly revenue for each product
# MAGIC WITH product_monthly_sales AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         d.Year,
# MAGIC         d.Month,
# MAGIC         p.ProductKey,
# MAGIC         p.ProductName,
# MAGIC
# MAGIC         -- Aggregation: Calculate monthly revenue
# MAGIC         SUM(f.LineTotal) AS MonthlyRevenue
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join product dimension to get product name
# MAGIC     JOIN gold.dim_product p
# MAGIC         ON f.ProductKey = p.ProductKey
# MAGIC
# MAGIC     -- Join date dimension to get year and month
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate revenue by month and product
# MAGIC     GROUP BY
# MAGIC         d.Year,
# MAGIC         d.Month,
# MAGIC         p.ProductKey,
# MAGIC         p.ProductName
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC -- Window Function + DENSE_RANK():
# MAGIC -- Rank products by monthly revenue
# MAGIC ranked_products AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         Year,
# MAGIC         Month,
# MAGIC         ProductKey,
# MAGIC         ProductName,
# MAGIC         MonthlyRevenue,
# MAGIC
# MAGIC         DENSE_RANK() OVER (
# MAGIC             PARTITION BY Year, Month
# MAGIC             ORDER BY MonthlyRevenue DESC
# MAGIC         ) AS RevenueRank
# MAGIC
# MAGIC     FROM product_monthly_sales
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     Year,
# MAGIC     Month,
# MAGIC     ProductKey,
# MAGIC     ProductName,
# MAGIC     MonthlyRevenue,
# MAGIC     RevenueRank
# MAGIC
# MAGIC FROM ranked_products
# MAGIC
# MAGIC -- Keep only the Top 10 products each month
# MAGIC WHERE RevenueRank <= 10;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_top_10_monthly_products
# MAGIC
# MAGIC -- Sort results by month and rank
# MAGIC ORDER BY
# MAGIC     Year,
# MAGIC     Month,
# MAGIC     RevenueRank,
# MAGIC     MonthlyRevenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 6
# MAGIC -- Which products are frequently purchased together
# MAGIC -- in the same order?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_products_frequently_purchased_together AS
# MAGIC
# MAGIC -- CTE: Generate product pairs from the same order
# MAGIC WITH product_pairs AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         f1.ProductKey AS Product1Key,
# MAGIC         p1.ProductName AS Product1,
# MAGIC
# MAGIC         f2.ProductKey AS Product2Key,
# MAGIC         p2.ProductName AS Product2
# MAGIC
# MAGIC     FROM gold.fact_sales f1
# MAGIC
# MAGIC     -- Self Join: Match products from the same order
# MAGIC     JOIN gold.fact_sales f2
# MAGIC         ON f1.SalesOrderID = f2.SalesOrderID
# MAGIC
# MAGIC         -- Pair Generation: Avoid duplicate and reversed pairs
# MAGIC         AND f1.ProductKey < f2.ProductKey
# MAGIC
# MAGIC     -- Join product dimension to get first product name
# MAGIC     JOIN gold.dim_product p1
# MAGIC         ON f1.ProductKey = p1.ProductKey
# MAGIC
# MAGIC     -- Join product dimension to get second product name
# MAGIC     JOIN gold.dim_product p2
# MAGIC         ON f2.ProductKey = p2.ProductKey
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     Product1,
# MAGIC     Product2,
# MAGIC
# MAGIC     -- Aggregation: Count how many orders contain the pair
# MAGIC     COUNT(*) AS TimesPurchasedTogether
# MAGIC
# MAGIC FROM product_pairs
# MAGIC
# MAGIC -- GROUP BY: Aggregate by product pair
# MAGIC GROUP BY
# MAGIC     Product1,
# MAGIC     Product2;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_products_frequently_purchased_together
# MAGIC
# MAGIC -- Show the most frequently purchased pairs first
# MAGIC ORDER BY
# MAGIC     TimesPurchasedTogether DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 7
# MAGIC -- Which sales territories have experienced the highest
# MAGIC -- year-over-year growth?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_territory_yoy_growth AS
# MAGIC
# MAGIC -- CTE: Calculate total revenue for each territory by year
# MAGIC WITH territory_sales AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         d.Year,
# MAGIC         t.TerritoryKey,
# MAGIC         t.Territory,
# MAGIC
# MAGIC         -- Aggregation: Calculate yearly revenue
# MAGIC         SUM(f.LineTotal) AS TotalRevenue
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join territory dimension to get territory name
# MAGIC     JOIN gold.dim_territory t
# MAGIC         ON f.TerritoryKey = t.TerritoryKey
# MAGIC
# MAGIC     -- Join date dimension to get year
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate revenue by year and territory
# MAGIC     GROUP BY
# MAGIC         d.Year,
# MAGIC         t.TerritoryKey,
# MAGIC         t.Territory
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     Year,
# MAGIC     Territory,
# MAGIC     TotalRevenue,
# MAGIC
# MAGIC     -- Window Function + LAG():
# MAGIC     -- Get the previous year's revenue for each territory
# MAGIC     LAG(TotalRevenue) OVER (
# MAGIC         PARTITION BY TerritoryKey
# MAGIC         ORDER BY Year
# MAGIC     ) AS PreviousYearRevenue,
# MAGIC
# MAGIC     -- Calculate year-over-year growth percentage
# MAGIC     ROUND(
# MAGIC         (
# MAGIC             TotalRevenue -
# MAGIC             LAG(TotalRevenue) OVER (
# MAGIC                 PARTITION BY TerritoryKey
# MAGIC                 ORDER BY Year
# MAGIC             )
# MAGIC         ) * 100.0
# MAGIC         /
# MAGIC         LAG(TotalRevenue) OVER (
# MAGIC             PARTITION BY TerritoryKey
# MAGIC             ORDER BY Year
# MAGIC         ),
# MAGIC         2
# MAGIC     ) AS YoYGrowthRate
# MAGIC
# MAGIC FROM territory_sales;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_territory_yoy_growth
# MAGIC
# MAGIC -- Show territories with the highest growth first
# MAGIC ORDER BY
# MAGIC     YoYGrowthRate DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 8
# MAGIC -- Which salespeople consistently outperform the average
# MAGIC -- sales performance of their territory?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_salespeople_above_territory_average AS
# MAGIC
# MAGIC -- CTE: Calculate total revenue for each salesperson
# MAGIC WITH salesperson_sales AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         s.SalesPersonKey,
# MAGIC         s.SalesPersonName,
# MAGIC         t.Territory,
# MAGIC         t.TerritoryKey,
# MAGIC
# MAGIC         -- Aggregation: Calculate total sales by salesperson
# MAGIC         SUM(f.LineTotal) AS TotalRevenue
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join salesperson dimension
# MAGIC     JOIN gold.dim_salesperson s
# MAGIC         ON f.SalesPersonKey = s.SalesPersonKey
# MAGIC
# MAGIC     -- Join territory dimension
# MAGIC     JOIN gold.dim_territory t
# MAGIC         ON f.TerritoryKey = t.TerritoryKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate sales by salesperson and territory
# MAGIC     GROUP BY
# MAGIC         s.SalesPersonKey,
# MAGIC         s.SalesPersonName,
# MAGIC         t.TerritoryKey,
# MAGIC         t.Territory
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC -- Window Function + AVG():
# MAGIC -- Calculate the average revenue for each territory
# MAGIC territory_average AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         *,
# MAGIC         AVG(TotalRevenue) OVER (
# MAGIC             PARTITION BY TerritoryKey
# MAGIC         ) AS TerritoryAverageRevenue
# MAGIC
# MAGIC     FROM salesperson_sales
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     SalesPersonName,
# MAGIC     Territory,
# MAGIC     TotalRevenue,
# MAGIC     TerritoryAverageRevenue
# MAGIC
# MAGIC FROM territory_average
# MAGIC
# MAGIC -- Keep only salespeople above their territory average
# MAGIC WHERE TotalRevenue > TerritoryAverageRevenue;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_salespeople_above_territory_average
# MAGIC
# MAGIC -- Show the highest-performing salespeople first
# MAGIC ORDER BY
# MAGIC     TotalRevenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 9
# MAGIC -- Which customers are at risk of churn based on purchase
# MAGIC -- frequency and recency?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_customer_churn_risk AS
# MAGIC
# MAGIC -- CTE: Find each customer's last purchase date
# MAGIC WITH customer_activity AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         f.CustomerKey,
# MAGIC
# MAGIC         -- Aggregation: Count total purchases
# MAGIC         COUNT(DISTINCT f.SalesOrderID) AS PurchaseFrequency,
# MAGIC
# MAGIC         -- Aggregation: Find the most recent purchase
# MAGIC         MAX(TO_DATE(CAST(d.DateKey AS STRING), 'yyyyMMdd')) AS LastPurchaseDate
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join date dimension
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate by customer
# MAGIC     GROUP BY
# MAGIC         f.CustomerKey
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC -- CTE: Calculate customer recency
# MAGIC customer_recency AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         CustomerKey,
# MAGIC         PurchaseFrequency,
# MAGIC         LastPurchaseDate,
# MAGIC
# MAGIC         -- Date Function: Calculate days since last purchase
# MAGIC         DATEDIFF(
# MAGIC             (
# MAGIC                 SELECT MAX(
# MAGIC                     TO_DATE(CAST(DateKey AS STRING), 'yyyyMMdd')
# MAGIC                 )
# MAGIC                 FROM gold.dim_date
# MAGIC             ),
# MAGIC             LastPurchaseDate
# MAGIC         ) AS DaysSinceLastPurchase
# MAGIC
# MAGIC     FROM customer_activity
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     c.CustomerKey,
# MAGIC     c.CustomerName,
# MAGIC     PurchaseFrequency,
# MAGIC     LastPurchaseDate,
# MAGIC     DaysSinceLastPurchase,
# MAGIC
# MAGIC     -- CASE Expression:
# MAGIC     -- Classify customers by churn risk
# MAGIC     CASE
# MAGIC
# MAGIC         WHEN DaysSinceLastPurchase > 365
# MAGIC             THEN 'High Risk'
# MAGIC
# MAGIC         WHEN DaysSinceLastPurchase > 180
# MAGIC             THEN 'Medium Risk'
# MAGIC
# MAGIC         ELSE 'Low Risk'
# MAGIC
# MAGIC     END AS ChurnRisk
# MAGIC
# MAGIC FROM customer_recency r
# MAGIC
# MAGIC -- Join customer dimension
# MAGIC JOIN gold.dim_customer c
# MAGIC     ON r.CustomerKey = c.CustomerKey;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_customer_churn_risk
# MAGIC
# MAGIC -- Show highest-risk customers first
# MAGIC ORDER BY
# MAGIC     DaysSinceLastPurchase DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 10
# MAGIC -- What is the average time between customer purchases,
# MAGIC -- and how does it vary by customer segment?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_avg_purchase_interval_by_segment AS
# MAGIC
# MAGIC -- CTE: Get each customer's purchase history
# MAGIC WITH customer_orders AS (
# MAGIC
# MAGIC     SELECT DISTINCT
# MAGIC
# MAGIC         f.CustomerKey,
# MAGIC         TO_DATE(CAST(d.DateKey AS STRING), 'yyyyMMdd') AS OrderDate,
# MAGIC         f.LineTotal
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join date dimension
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC -- CTE: Calculate days between purchases
# MAGIC purchase_intervals AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         CustomerKey,
# MAGIC         OrderDate,
# MAGIC
# MAGIC         -- Window Function + LAG():
# MAGIC         -- Get the previous purchase date
# MAGIC         LAG(OrderDate) OVER (
# MAGIC             PARTITION BY CustomerKey
# MAGIC             ORDER BY OrderDate
# MAGIC         ) AS PreviousPurchaseDate,
# MAGIC
# MAGIC         -- Date Function:
# MAGIC         -- Calculate days between purchases
# MAGIC         DATEDIFF(
# MAGIC             OrderDate,
# MAGIC             LAG(OrderDate) OVER (
# MAGIC                 PARTITION BY CustomerKey
# MAGIC                 ORDER BY OrderDate
# MAGIC             )
# MAGIC         ) AS DaysBetweenPurchases,
# MAGIC
# MAGIC         LineTotal
# MAGIC
# MAGIC     FROM customer_orders
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC -- CTE: Calculate customer lifetime revenue
# MAGIC customer_segment AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         CustomerKey,
# MAGIC
# MAGIC         -- Aggregation: Calculate lifetime revenue
# MAGIC         SUM(LineTotal) AS LifetimeRevenue,
# MAGIC
# MAGIC         -- CASE Expression:
# MAGIC         -- Classify customers into segments
# MAGIC         CASE
# MAGIC
# MAGIC             WHEN SUM(LineTotal) >= 10000 THEN 'High Value'
# MAGIC             WHEN SUM(LineTotal) >= 5000 THEN 'Medium Value'
# MAGIC             ELSE 'Low Value'
# MAGIC
# MAGIC         END AS CustomerSegment
# MAGIC
# MAGIC     FROM customer_orders
# MAGIC
# MAGIC     -- GROUP BY: Aggregate revenue by customer
# MAGIC     GROUP BY
# MAGIC         CustomerKey
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     s.CustomerSegment,
# MAGIC
# MAGIC     -- Aggregation: Calculate the average days between purchases
# MAGIC     ROUND(AVG(p.DaysBetweenPurchases), 2) AS AvgDaysBetweenPurchases
# MAGIC
# MAGIC FROM purchase_intervals p
# MAGIC
# MAGIC -- Join customer segments
# MAGIC JOIN customer_segment s
# MAGIC     ON p.CustomerKey = s.CustomerKey
# MAGIC
# MAGIC -- Ignore the first purchase for each customer
# MAGIC WHERE p.DaysBetweenPurchases IS NOT NULL
# MAGIC
# MAGIC -- GROUP BY: Calculate averages by customer segment
# MAGIC GROUP BY
# MAGIC     s.CustomerSegment;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_avg_purchase_interval_by_segment
# MAGIC
# MAGIC -- Show segments with the shortest purchase intervals first
# MAGIC ORDER BY
# MAGIC     AvgDaysBetweenPurchases;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 11
# MAGIC -- Which products generate high revenue but also have
# MAGIC -- low profitability?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_high_revenue_low_profit_products AS
# MAGIC
# MAGIC -- CTE: Calculate sales and profit metrics for each product
# MAGIC WITH product_profitability AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         p.ProductKey,
# MAGIC         p.ProductName,
# MAGIC
# MAGIC         -- Aggregation: Calculate total revenue
# MAGIC         SUM(f.LineTotal) AS TotalRevenue,
# MAGIC
# MAGIC         -- Conditional Aggregation: Calculate total cost
# MAGIC         SUM(f.OrderQty * p.StandardCost) AS TotalCost,
# MAGIC
# MAGIC         -- Calculated Metric: Calculate total profit
# MAGIC         SUM(f.LineTotal) -
# MAGIC         SUM(f.OrderQty * p.StandardCost) AS TotalProfit
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join product dimension
# MAGIC     JOIN gold.dim_product p
# MAGIC         ON f.ProductKey = p.ProductKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate metrics by product
# MAGIC     GROUP BY
# MAGIC         p.ProductKey,
# MAGIC         p.ProductName
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     ProductName,
# MAGIC     TotalRevenue,
# MAGIC     TotalCost,
# MAGIC     TotalProfit,
# MAGIC
# MAGIC     -- Calculated Metric:
# MAGIC     -- Calculate profit margin percentage
# MAGIC     ROUND(
# MAGIC         TotalProfit * 100.0 / TotalRevenue,
# MAGIC         2
# MAGIC     ) AS ProfitMargin
# MAGIC
# MAGIC FROM product_profitability
# MAGIC
# MAGIC -- Keep products with high revenue but low profitability
# MAGIC WHERE
# MAGIC     TotalRevenue > 100000
# MAGIC     AND
# MAGIC     ROUND(
# MAGIC         TotalProfit * 100.0 / TotalRevenue,
# MAGIC         2
# MAGIC     ) < 20;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_high_revenue_low_profit_products
# MAGIC
# MAGIC -- Show highest revenue products first
# MAGIC ORDER BY
# MAGIC     TotalRevenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 12
# MAGIC -- Which months show unusual sales spikes or drops compared
# MAGIC -- to historical averages?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_monthly_sales_trends AS
# MAGIC
# MAGIC -- CTE: Calculate total sales for each month
# MAGIC WITH monthly_sales AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         d.Year,
# MAGIC         d.Month,
# MAGIC         CONCAT(d.Year, '-', LPAD(d.Month, 2, '0')) AS YearMonth,
# MAGIC
# MAGIC         -- Aggregation: Calculate monthly sales
# MAGIC         SUM(f.LineTotal) AS MonthlySales
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join date dimension
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate sales by month
# MAGIC     GROUP BY
# MAGIC         d.Year,
# MAGIC         d.Month
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     Year,
# MAGIC     Month,
# MAGIC     YearMonth,
# MAGIC     MonthlySales,
# MAGIC
# MAGIC     -- Window Function:
# MAGIC     -- Calculate the 3-month moving average
# MAGIC     ROUND(
# MAGIC         AVG(MonthlySales) OVER (
# MAGIC             ORDER BY Year, Month
# MAGIC             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
# MAGIC         ),
# MAGIC         2
# MAGIC     ) AS MovingAverage,
# MAGIC
# MAGIC     -- Statistical Comparison:
# MAGIC     -- Compare monthly sales to the moving average
# MAGIC     CASE
# MAGIC
# MAGIC         WHEN MonthlySales >
# MAGIC             AVG(MonthlySales) OVER (
# MAGIC                 ORDER BY Year, Month
# MAGIC                 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
# MAGIC             )
# MAGIC         THEN 'Sales Spike'
# MAGIC
# MAGIC         WHEN MonthlySales <
# MAGIC             AVG(MonthlySales) OVER (
# MAGIC                 ORDER BY Year, Month
# MAGIC                 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
# MAGIC             )
# MAGIC         THEN 'Sales Drop'
# MAGIC
# MAGIC         ELSE 'Normal'
# MAGIC
# MAGIC     END AS SalesTrend
# MAGIC
# MAGIC FROM monthly_sales;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_monthly_sales_trends
# MAGIC
# MAGIC -- Show results in chronological order
# MAGIC ORDER BY
# MAGIC     Year,
# MAGIC     Month;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 13
# MAGIC -- What are the sales trends by weekday and season, and are
# MAGIC -- there recurring seasonal patterns?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_sales_trends_by_weekday_season AS
# MAGIC
# MAGIC -- CTE: Calculate sales by weekday and season
# MAGIC WITH seasonal_sales AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         d.WeekDay,
# MAGIC
# MAGIC         -- CASE Expression:
# MAGIC         -- Assign each month to a season
# MAGIC         CASE
# MAGIC
# MAGIC             WHEN d.Month IN (12, 1, 2)
# MAGIC                 THEN 'Winter'
# MAGIC
# MAGIC             WHEN d.Month IN (3, 4, 5)
# MAGIC                 THEN 'Spring'
# MAGIC
# MAGIC             WHEN d.Month IN (6, 7, 8)
# MAGIC                 THEN 'Summer'
# MAGIC
# MAGIC             ELSE 'Autumn'
# MAGIC
# MAGIC         END AS Season,
# MAGIC
# MAGIC         -- Aggregation: Calculate total sales
# MAGIC         SUM(f.LineTotal) AS TotalSales
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join date dimension
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate sales by weekday and season
# MAGIC     GROUP BY
# MAGIC
# MAGIC         d.WeekDay,
# MAGIC
# MAGIC         CASE
# MAGIC
# MAGIC             WHEN d.Month IN (12, 1, 2)
# MAGIC                 THEN 'Winter'
# MAGIC
# MAGIC             WHEN d.Month IN (3, 4, 5)
# MAGIC                 THEN 'Spring'
# MAGIC
# MAGIC             WHEN d.Month IN (6, 7, 8)
# MAGIC                 THEN 'Summer'
# MAGIC
# MAGIC             ELSE 'Autumn'
# MAGIC
# MAGIC         END
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     WeekDay,
# MAGIC     Season,
# MAGIC     TotalSales
# MAGIC
# MAGIC FROM seasonal_sales;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_sales_trends_by_weekday_season
# MAGIC
# MAGIC -- Show highest sales first
# MAGIC ORDER BY
# MAGIC     TotalSales DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 14
# MAGIC -- Which customers moved from low-value to high-value
# MAGIC -- segments over time?
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_customer_segment_progression AS
# MAGIC
# MAGIC -- CTE: Calculate yearly revenue for each customer
# MAGIC WITH customer_sales AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         d.Year,
# MAGIC         c.CustomerKey,
# MAGIC         c.CustomerName,
# MAGIC
# MAGIC         -- Aggregation: Calculate yearly revenue
# MAGIC         SUM(f.LineTotal) AS TotalRevenue
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC     -- Join customer dimension
# MAGIC     JOIN gold.dim_customer c
# MAGIC         ON f.CustomerKey = c.CustomerKey
# MAGIC
# MAGIC     -- Join date dimension
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC     -- GROUP BY: Aggregate revenue by customer and year
# MAGIC     GROUP BY
# MAGIC         d.Year,
# MAGIC         c.CustomerKey,
# MAGIC         c.CustomerName
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC -- CTE: Assign customers to value segments
# MAGIC customer_segments AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         Year,
# MAGIC         CustomerKey,
# MAGIC         CustomerName,
# MAGIC         TotalRevenue,
# MAGIC
# MAGIC         -- Window Function + NTILE():
# MAGIC         -- Divide customers into four revenue segments each year
# MAGIC         NTILE(4) OVER (
# MAGIC             PARTITION BY Year
# MAGIC             ORDER BY TotalRevenue
# MAGIC         ) AS CustomerSegment
# MAGIC
# MAGIC     FROM customer_sales
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC -- CTE: Compare customer segments over time
# MAGIC segment_changes AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         Year,
# MAGIC         CustomerKey,
# MAGIC         CustomerName,
# MAGIC         TotalRevenue,
# MAGIC         CustomerSegment,
# MAGIC
# MAGIC         -- Window Function + LAG():
# MAGIC         -- Get the customer's previous year's segment
# MAGIC         LAG(CustomerSegment) OVER (
# MAGIC             PARTITION BY CustomerKey
# MAGIC             ORDER BY Year
# MAGIC         ) AS PreviousSegment
# MAGIC
# MAGIC     FROM customer_segments
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC     Year,
# MAGIC     CustomerName,
# MAGIC     PreviousSegment,
# MAGIC     CustomerSegment,
# MAGIC     TotalRevenue
# MAGIC
# MAGIC FROM segment_changes
# MAGIC
# MAGIC -- Keep customers who moved to a higher segment
# MAGIC WHERE PreviousSegment IS NOT NULL
# MAGIC AND CustomerSegment > PreviousSegment;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_customer_segment_progression
# MAGIC
# MAGIC -- Show largest improvements first
# MAGIC ORDER BY
# MAGIC     Year,
# MAGIC     CustomerSegment DESC,
# MAGIC     TotalRevenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ==========================================================
# MAGIC -- Business Question 15
# MAGIC -- Build a complete RFM (Recency, Frequency, Monetary)
# MAGIC -- customer segmentation model
# MAGIC -- ==========================================================
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Create View
# MAGIC -- ==========================================================
# MAGIC CREATE OR REPLACE VIEW gold.vw_customer_rfm_segmentation AS
# MAGIC
# MAGIC -- CTE: Calculate customer RFM metrics
# MAGIC WITH customer_rfm AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         c.CustomerKey,
# MAGIC         c.CustomerName,
# MAGIC
# MAGIC         -- ==================================================
# MAGIC         -- Recency:
# MAGIC         -- Days since customer's last purchase
# MAGIC         -- ==================================================
# MAGIC         DATEDIFF(
# MAGIC             CURRENT_DATE(),
# MAGIC             MAX(d.OrderDate)
# MAGIC         ) AS Recency,
# MAGIC
# MAGIC
# MAGIC         -- ==================================================
# MAGIC         -- Frequency:
# MAGIC         -- Number of orders made by each customer
# MAGIC         -- ==================================================
# MAGIC         COUNT(
# MAGIC             DISTINCT f.SalesOrderID
# MAGIC         ) AS Frequency,
# MAGIC
# MAGIC
# MAGIC         -- ==================================================
# MAGIC         -- Monetary:
# MAGIC         -- Total revenue generated by customer
# MAGIC         -- ==================================================
# MAGIC         SUM(
# MAGIC             f.LineTotal
# MAGIC         ) AS Monetary
# MAGIC
# MAGIC
# MAGIC     FROM gold.fact_sales f
# MAGIC
# MAGIC
# MAGIC     -- Join customer dimension
# MAGIC     JOIN gold.dim_customer c
# MAGIC         ON f.CustomerKey = c.CustomerKey
# MAGIC
# MAGIC
# MAGIC     -- Join date dimension
# MAGIC     JOIN gold.dim_date d
# MAGIC         ON f.DateKey = d.DateKey
# MAGIC
# MAGIC
# MAGIC     GROUP BY
# MAGIC
# MAGIC         c.CustomerKey,
# MAGIC         c.CustomerName
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC
# MAGIC -- CTE: Create RFM scores using NTILE()
# MAGIC rfm_scores AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC         CustomerKey,
# MAGIC         CustomerName,
# MAGIC
# MAGIC         Recency,
# MAGIC         Frequency,
# MAGIC         Monetary,
# MAGIC
# MAGIC
# MAGIC         -- ==================================================
# MAGIC         -- Recency Score:
# MAGIC         -- Lower days since purchase = better score
# MAGIC         -- ==================================================
# MAGIC         NTILE(5) OVER(
# MAGIC             ORDER BY Recency DESC
# MAGIC         ) AS RecencyScore,
# MAGIC
# MAGIC
# MAGIC         -- ==================================================
# MAGIC         -- Frequency Score:
# MAGIC         -- More purchases = better score
# MAGIC         -- ==================================================
# MAGIC         NTILE(5) OVER(
# MAGIC             ORDER BY Frequency ASC
# MAGIC         ) AS FrequencyScore,
# MAGIC
# MAGIC
# MAGIC         -- ==================================================
# MAGIC         -- Monetary Score:
# MAGIC         -- Higher revenue = better score
# MAGIC         -- ==================================================
# MAGIC         NTILE(5) OVER(
# MAGIC             ORDER BY Monetary ASC
# MAGIC         ) AS MonetaryScore
# MAGIC
# MAGIC
# MAGIC     FROM customer_rfm
# MAGIC
# MAGIC ),
# MAGIC
# MAGIC
# MAGIC -- CTE: Create final RFM segment classification
# MAGIC rfm_segments AS (
# MAGIC
# MAGIC     SELECT
# MAGIC
# MAGIC
# MAGIC         CustomerKey,
# MAGIC         CustomerName,
# MAGIC
# MAGIC         Recency,
# MAGIC         Frequency,
# MAGIC         Monetary,
# MAGIC
# MAGIC
# MAGIC         RecencyScore,
# MAGIC         FrequencyScore,
# MAGIC         MonetaryScore,
# MAGIC
# MAGIC
# MAGIC         -- ==================================================
# MAGIC         -- Combine scores into RFM Score
# MAGIC         -- ==================================================
# MAGIC         CONCAT(
# MAGIC             RecencyScore,
# MAGIC             FrequencyScore,
# MAGIC             MonetaryScore
# MAGIC         ) AS RFMScore,
# MAGIC
# MAGIC
# MAGIC         -- ==================================================
# MAGIC         -- Customer segmentation logic
# MAGIC         -- ==================================================
# MAGIC         CASE
# MAGIC
# MAGIC
# MAGIC             -- High-value loyal customers
# MAGIC             WHEN RecencyScore >= 4
# MAGIC              AND FrequencyScore >= 4
# MAGIC              AND MonetaryScore >= 4
# MAGIC             THEN 'Champions'
# MAGIC
# MAGIC
# MAGIC             -- Customers with good value but less recent activity
# MAGIC             WHEN MonetaryScore >= 4
# MAGIC              AND FrequencyScore >= 3
# MAGIC             THEN 'Loyal Customers'
# MAGIC
# MAGIC
# MAGIC             -- Recently acquired customers
# MAGIC             WHEN RecencyScore >= 4
# MAGIC              AND FrequencyScore <= 2
# MAGIC             THEN 'New Customers'
# MAGIC
# MAGIC
# MAGIC             -- Customers with decreasing engagement
# MAGIC             WHEN RecencyScore <= 2
# MAGIC              AND FrequencyScore >= 3
# MAGIC             THEN 'At Risk'
# MAGIC
# MAGIC
# MAGIC             -- Customers with low activity and value
# MAGIC             WHEN RecencyScore <= 2
# MAGIC              AND FrequencyScore <= 2
# MAGIC              AND MonetaryScore <= 2
# MAGIC             THEN 'Lost Customers'
# MAGIC
# MAGIC
# MAGIC             -- Remaining customers
# MAGIC             ELSE 'Potential Customers'
# MAGIC
# MAGIC
# MAGIC         END AS CustomerSegment
# MAGIC
# MAGIC
# MAGIC     FROM rfm_scores
# MAGIC
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC
# MAGIC
# MAGIC     CustomerKey,
# MAGIC     CustomerName,
# MAGIC
# MAGIC     Recency,
# MAGIC     Frequency,
# MAGIC     Monetary,
# MAGIC
# MAGIC     RecencyScore,
# MAGIC     FrequencyScore,
# MAGIC     MonetaryScore,
# MAGIC
# MAGIC     RFMScore,
# MAGIC
# MAGIC     CustomerSegment
# MAGIC
# MAGIC
# MAGIC FROM rfm_segments;
# MAGIC
# MAGIC -- ==========================================================
# MAGIC -- Query the View
# MAGIC -- ==========================================================
# MAGIC
# MAGIC SELECT *
# MAGIC
# MAGIC FROM gold.vw_customer_rfm_segmentation
# MAGIC
# MAGIC -- Show highest-value customers first
# MAGIC ORDER BY
# MAGIC
# MAGIC     Monetary DESC,
# MAGIC     Frequency DESC;