# Databricks notebook source
from pyspark.sql.functions import *

# ============================================
# LOAD SILVER TABLES
# ============================================

customer_df = spark.table("silver.customer")
person_df = spark.table("silver.person")
product_df = spark.table("silver.product")
product_subcategory_df = spark.table("silver.product_subcategory")
product_category_df = spark.table("silver.product_category")
sales_person_df = spark.table("silver.sales_person")
sales_territory_df = spark.table("silver.sales_territory")
sales_order_header_df = spark.table("silver.sales_order_header")
sales_order_detail_df = spark.table("silver.sales_order_detail")

# =====================================================
# BUILD STAR SCHEMA DIMENSIONS AND FACT TABLE
# =====================================================

# =====================================================
# CREATE DIM CUSTOMER
# =====================================================

dim_customer = (
    customer_df.alias("c")
    .join(
        person_df.alias("p"),
        col("c.PersonID") == col("p.BusinessEntityID"),
        "left"
    )
    .select(
        col("c.CustomerID").alias("CustomerKey"),
        col("c.AccountNumber"),
        concat_ws(
            " ",
            col("p.FirstName"),
            col("p.MiddleName"),
            col("p.LastName")
        ).alias("CustomerName")
    )
)


# =====================================================
# CREATE DIM PRODUCT
# =====================================================

dim_product = (
    product_df.alias("p")
    .join(
        product_subcategory_df.alias("ps"),
        col("p.ProductSubcategoryID") == col("ps.ProductSubcategoryID"),
        "left"
    )
    .join(
        product_category_df.alias("pc"),
        col("ps.ProductCategoryID") == col("pc.ProductCategoryID"),
        "left"
    )
    .select(
        col("p.ProductID").alias("ProductKey"),
        col("p.Name").alias("ProductName"),
        col("p.ProductNumber"),
        col("p.Color"),
        col("p.Size"),
        col("p.StandardCost"),
        col("p.ListPrice"),
        col("ps.Name").alias("Subcategory"),
        col("pc.Name").alias("Category")
    )
)


# =====================================================
# CREATE DIM TERRITORY
# =====================================================

dim_territory = (
    sales_territory_df
    .select(
        col("TerritoryID").alias("TerritoryKey"),
        col("Name").alias("Territory"),
        col("CountryRegionCode"),
        col("Group")
    )
)


# =====================================================
# CREATE DIM SALESPERSON
# =====================================================

dim_salesperson = (
    sales_person_df.alias("sp")
    .join(
        person_df.alias("p"),
        col("sp.BusinessEntityID") == col("p.BusinessEntityID"),
        "left"
    )
    .select(
    col("sp.BusinessEntityID").alias("SalesPersonKey"),
    trim(
        concat_ws(
            " ",
            col("p.FirstName"),
            col("p.MiddleName"),
            col("p.LastName")
        )
    ).alias("SalesPersonName"),
    col("sp.SalesQuota"),
    col("sp.Bonus"),
    col("sp.CommissionPct"),
    col("sp.SalesYTD")
))

# =====================================================
# CREATE DIM DATE
# =====================================================

dim_date = (
    sales_order_header_df
    .select("OrderDate")
    .distinct()
    .withColumn("DateKey", date_format("OrderDate", "yyyyMMdd").cast("int"))
    .withColumn("Year", year("OrderDate"))
    .withColumn("Quarter", quarter("OrderDate"))
    .withColumn("Month", month("OrderDate"))
    .withColumn("MonthName", date_format("OrderDate", "MMMM"))
    .withColumn("Week", weekofyear("OrderDate"))
    .withColumn("Day", dayofmonth("OrderDate"))
    .withColumn("WeekDay", date_format("OrderDate", "EEEE"))
)

# =====================================================
# CREATE FACT SALES
# =====================================================

fact_sales = (
    sales_order_detail_df.alias("d")
    .join(
        sales_order_header_df.alias("h"),
        "SalesOrderID",
        "inner"
    )
    .select(
        col("SalesOrderID"),
        col("SalesOrderDetailID"),

        date_format(
            col("OrderDate"),
            "yyyyMMdd"
        ).cast("int").alias("DateKey"),

        col("CustomerID").alias("CustomerKey"),
        col("SalesPersonID").alias("SalesPersonKey"),
        col("TerritoryID").alias("TerritoryKey"),
        col("ProductID").alias("ProductKey"),

        col("OrderQty"),
        col("UnitPrice"),
        col("UnitPriceDiscount"),
        col("LineTotal")
    )
)


# =====================================================
# SAVE GOLD TABLES
# =====================================================

# =====================================================
# CREATE GOLD SCHEMA
# =====================================================

spark.sql("""
CREATE SCHEMA IF NOT EXISTS gold
""")

dim_customer.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("gold.dim_customer")


dim_product.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("gold.dim_product")


dim_salesperson.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("gold.dim_salesperson")


dim_territory.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("gold.dim_territory")


dim_date.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("gold.dim_date")


fact_sales.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("gold.fact_sales")



