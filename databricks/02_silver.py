# Databricks notebook source
# =====================================================
# IMPORT FUNCTIONS
# =====================================================

from pyspark.sql.functions import (
    col,
    when,
    trim,
    concat_ws,
    year,
    quarter,
    month,
    date_format,
    weekofyear,
    dayofmonth
)


# =====================================================
# STEP 1 — LOAD BRONZE TABLES
# =====================================================

address_df = spark.table("bronze.address")
country_region_df = spark.table("bronze.country_region")
customer_df = spark.table("bronze.customer")
employee_df = spark.table("bronze.employee")
person_df = spark.table("bronze.person")
product_df = spark.table("bronze.product")
product_category_df = spark.table("bronze.product_category")
product_subcategory_df = spark.table("bronze.product_subcategory")
sales_order_detail_df = spark.table("bronze.sales_order_detail")
sales_order_header_df = spark.table("bronze.sales_order_header")
sales_person_df = spark.table("bronze.sales_person")
sales_territory_df = spark.table("bronze.sales_territory")
state_province_df = spark.table("bronze.state_province")

# =====================================================
# STEP 2 — DATA CLEANING
# =====================================================

from pyspark.sql.functions import (
    col,
    when,
    trim,
    upper,
    initcap
)

# -----------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------

def clean_int(column_name):
    return (
        when(
            trim(col(column_name)).isin("", "NULL"),
            None
        )
        .otherwise(trim(col(column_name)))
        .cast("int")
    )


def clean_double(column_name):
    return (
        when(
            trim(col(column_name)).isin("", "NULL"),
            None
        )
        .otherwise(trim(col(column_name)))
        .cast("double")
    )


def clean_string(column_name):
    return trim(col(column_name))


# -----------------------------------------------------
# CUSTOMER
# -----------------------------------------------------

customer_df = (
    customer_df
    .dropDuplicates(["CustomerID"])
    .withColumn("PersonID", clean_int("PersonID"))
    .withColumn("StoreID", clean_int("StoreID"))
    .withColumn("AccountNumber", clean_string("AccountNumber"))
)


# -----------------------------------------------------
# PERSON
# -----------------------------------------------------

person_df = (
    person_df
    .dropDuplicates(["BusinessEntityID"])
    .withColumn("FirstName", initcap(clean_string("FirstName")))
    .withColumn("MiddleName", initcap(clean_string("MiddleName")))
    .withColumn("LastName", initcap(clean_string("LastName")))
)


# -----------------------------------------------------
# PRODUCT
# -----------------------------------------------------

product_df = (
    product_df
    .dropDuplicates(["ProductID"])
    .withColumn("ProductSubcategoryID", clean_int("ProductSubcategoryID"))
    .withColumn("ProductModelID", clean_int("ProductModelID"))
    .withColumn("StandardCost", clean_double("StandardCost"))
    .withColumn("ListPrice", clean_double("ListPrice"))
    .withColumn("Name", clean_string("Name"))
    .withColumn("Color", initcap(clean_string("Color")))
    .withColumn("Size", clean_string("Size"))
)


# -----------------------------------------------------
# PRODUCT SUBCATEGORY
# -----------------------------------------------------

product_subcategory_df = (
    product_subcategory_df
    .dropDuplicates(["ProductSubcategoryID"])
    .withColumn("ProductCategoryID", clean_int("ProductCategoryID"))
    .withColumn("Name", clean_string("Name"))
)


# -----------------------------------------------------
# PRODUCT CATEGORY
# -----------------------------------------------------

product_category_df = (
    product_category_df
    .dropDuplicates(["ProductCategoryID"])
    .withColumn("Name", clean_string("Name"))
)


# -----------------------------------------------------
# SALES ORDER HEADER
# -----------------------------------------------------

sales_order_header_df = (
    sales_order_header_df
    .dropDuplicates(["SalesOrderID"])
    .withColumn("SalesPersonID", clean_int("SalesPersonID"))
    .withColumn("CustomerID", clean_int("CustomerID"))
    .withColumn("TerritoryID", clean_int("TerritoryID"))
)


# -----------------------------------------------------
# SALES ORDER DETAIL
# -----------------------------------------------------

sales_order_detail_df = (
    sales_order_detail_df
    .dropDuplicates(["SalesOrderID", "SalesOrderDetailID"])
    .withColumn("OrderQty", clean_int("OrderQty"))
    .withColumn("UnitPrice", clean_double("UnitPrice"))
    .withColumn("UnitPriceDiscount", clean_double("UnitPriceDiscount"))
    .withColumn("LineTotal", clean_double("LineTotal"))
)


# -----------------------------------------------------
# SALES PERSON
# -----------------------------------------------------

sales_person_df = (
    sales_person_df
    .dropDuplicates(["BusinessEntityID"])
    .withColumn("TerritoryID", clean_int("TerritoryID"))
    .withColumn("SalesQuota", clean_double("SalesQuota"))
    .withColumn("Bonus", clean_double("Bonus"))
    .withColumn("CommissionPct", clean_double("CommissionPct"))
    .withColumn("SalesYTD", clean_double("SalesYTD"))
)


# -----------------------------------------------------
# SALES TERRITORY
# -----------------------------------------------------

sales_territory_df = (
    sales_territory_df
    .dropDuplicates(["TerritoryID"])
    .withColumn("Name", clean_string("Name"))
    .withColumn("CountryRegionCode", upper(clean_string("CountryRegionCode")))
)


# -----------------------------------------------------
# ADDRESS
# -----------------------------------------------------

address_df = (
    address_df
    .dropDuplicates(["AddressID"])
    .withColumn("City", initcap(clean_string("City")))
    .withColumn("PostalCode", clean_string("PostalCode"))
)


# -----------------------------------------------------
# STATE PROVINCE
# -----------------------------------------------------

state_province_df = (
    state_province_df
    .dropDuplicates(["StateProvinceID"])
    .withColumn("Name", clean_string("Name"))
)


# -----------------------------------------------------
# COUNTRY REGION
# -----------------------------------------------------

country_region_df = (
    country_region_df
    .dropDuplicates(["CountryRegionCode"])
    .withColumn("Name", clean_string("Name"))
)

# =====================================================
# STEP 3 — DATA QUALITY VALIDATION
# =====================================================

# -----------------------------
# Primary Keys should never be NULL
# -----------------------------

print("Null CustomerID:",
      customer_df.filter(col("CustomerID").isNull()).count())

print("Null ProductID:",
      product_df.filter(col("ProductID").isNull()).count())

print("Null SalesOrderID:",
      sales_order_header_df.filter(col("SalesOrderID").isNull()).count())

# -----------------------------
# Invalid numeric values
# -----------------------------

print("Negative Quantity:",
      sales_order_detail_df.filter(col("OrderQty") <= 0).count())

print("Negative Price:",
      sales_order_detail_df.filter(col("UnitPrice") < 0).count())

print("Negative Revenue:",
      sales_order_detail_df.filter(col("LineTotal") < 0).count())

# -----------------------------
# Invalid Dates
# -----------------------------

print("ShipDate before OrderDate:",
      sales_order_header_df.filter(
          col("ShipDate") < col("OrderDate")
      ).count())

print("DueDate before OrderDate:",
      sales_order_header_df.filter(
          col("DueDate") < col("OrderDate")
      ).count())


# =====================================================
# STEP 4 — REFERENTIAL INTEGRITY
# =====================================================

# Products in Sales not found in Product

invalid_products = ( 
    sales_order_detail_df
    .join(
        product_df,
        "ProductID",
        "left_anti"
    )
)

print("Invalid Products:",
      invalid_products.count())

# Customers in Sales not found in Customer

invalid_customers = (
    sales_order_header_df
    .join(
        customer_df,
        "CustomerID",
        "left_anti"
    )
)

print("Invalid Customers:",
      invalid_customers.count())

# Territories in Sales not found in Territory

invalid_territories = (
    sales_order_header_df
    .join(
        sales_territory_df,
        "TerritoryID",
        "left_anti"
    )
)

print("Invalid Territories:",
      invalid_territories.count())

# =====================================================
# STEP 5 — CREATE SILVER SCHEMA
# =====================================================

spark.sql("""
CREATE SCHEMA IF NOT EXISTS silver
""")

# =====================================================
# STEP 6 — SAVE SILVER DELTA TABLES
# =====================================================

# Address
address_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.address")


# Country Region
country_region_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.country_region")


# Customer
customer_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.customer")


# Employee
employee_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.employee")


# Person
person_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.person")


# Product
product_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.product")


# Product Category
product_category_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.product_category")


# Product Subcategory
product_subcategory_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.product_subcategory")


# Sales Order Header
sales_order_header_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.sales_order_header")


# Sales Order Detail
sales_order_detail_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.sales_order_detail")


# Sales Person
sales_person_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.sales_person")


# Sales Territory
sales_territory_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.sales_territory")


# State Province
state_province_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("silver.state_province")

