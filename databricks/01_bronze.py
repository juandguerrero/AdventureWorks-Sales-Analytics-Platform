# Databricks notebook source
# =====================================================
# LOAD RAW CSV FILES INTO PYSPARK DATAFRAMES
# =====================================================

# ==========================
# Address
# ==========================

address_columns = [
    "AddressID",
    "AddressLine1",
    "AddressLine2",
    "City",
    "StateProvinceID",
    "PostalCode",
    "SpatialLocation",
    "rowguid",
    "ModifiedDate"
]

address_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/Address.csv")
         .toDF(*address_columns)
)

# ==========================
# Country Region
# ==========================

country_region_columns = [
    "CountryRegionCode",
    "Name",
    "ModifiedDate"
]

country_region_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/CountryRegion.csv")
         .toDF(*country_region_columns)
)

# ==========================
# Customer
# ==========================

customer_columns = [
    "CustomerID",
    "PersonID",
    "StoreID",
    "TerritoryID",
    "AccountNumber",
    "rowguid",
    "ModifiedDate"
]

customer_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/Customer.csv")
         .toDF(*customer_columns)
)

# ==========================
# Employee
# ==========================

employee_columns = [
    "BusinessEntityID",
    "NationalIDNumber",
    "LoginID",
    "OrganizationNode",
    "OrganizationLevel",
    "JobTitle",
    "BirthDate",
    "MaritalStatus",
    "Gender",
    "HireDate",
    "SalariedFlag",
    "VacationHours",
    "SickLeaveHours",
    "CurrentFlag",
    "rowguid",
    "ModifiedDate"
]

employee_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/Employee.csv")
         .toDF(*employee_columns)
)

# ==========================
# Person
# ==========================

person_columns = [
    "BusinessEntityID",
    "PersonType",
    "NameStyle",
    "Title",
    "FirstName",
    "MiddleName",
    "LastName",
    "Suffix",
    "EmailPromotion",
    "AdditionalContactInfo",
    "Demographics",
    "rowguid",
    "ModifiedDate"
]

person_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/Person.csv")
         .toDF(*person_columns)
)

# ==========================
# Product Category
# ==========================

product_category_columns = [
    "ProductCategoryID",
    "Name",
    "rowguid",
    "ModifiedDate"
]

product_category_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/ProductCategory.csv")
         .toDF(*product_category_columns)
)

# ==========================
# Product Subcategory
# ==========================

product_subcategory_columns = [
    "ProductSubcategoryID",
    "ProductCategoryID",
    "Name",
    "rowguid",
    "ModifiedDate"
]

product_subcategory_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/ProductSubcategory.csv")
         .toDF(*product_subcategory_columns)
)

# ==========================
# Product
# ==========================

product_columns = [
    "ProductID",
    "Name",
    "ProductNumber",
    "MakeFlag",
    "FinishedGoodsFlag",
    "Color",
    "SafetyStockLevel",
    "ReorderPoint",
    "StandardCost",
    "ListPrice",
    "Size",
    "SizeUnitMeasureCode",
    "WeightUnitMeasureCode",
    "Weight",
    "DaysToManufacture",
    "ProductLine",
    "Class",
    "Style",
    "ProductSubcategoryID",
    "ProductModelID",
    "SellStartDate",
    "SellEndDate",
    "DiscontinuedDate",
    "rowguid",
    "ModifiedDate"
]

product_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/Product.csv")
         .toDF(*product_columns)
)

# ==========================
# Sales Order Detail
# ==========================

sales_order_detail_columns = [
    "SalesOrderID",
    "SalesOrderDetailID",
    "CarrierTrackingNumber",
    "OrderQty",
    "ProductID",
    "SpecialOfferID",
    "UnitPrice",
    "UnitPriceDiscount",
    "LineTotal",
    "rowguid",
    "ModifiedDate"
]

sales_order_detail_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/SalesOrderDetail.csv")
         .toDF(*sales_order_detail_columns)
)

# ==========================
# Sales Order Header
# ==========================

sales_order_header_columns = [
    "SalesOrderID",
    "RevisionNumber",
    "OrderDate",
    "DueDate",
    "ShipDate",
    "Status",
    "OnlineOrderFlag",
    "SalesOrderNumber",
    "PurchaseOrderNumber",
    "AccountNumber",
    "CustomerID",
    "SalesPersonID",
    "TerritoryID",
    "BillToAddressID",
    "ShipToAddressID",
    "ShipMethodID",
    "CreditCardID",
    "CreditCardApprovalCode",
    "CurrencyRateID",
    "SubTotal",
    "TaxAmt",
    "Freight",
    "TotalDue",
    "Comment",
    "rowguid",
    "ModifiedDate"
]

sales_order_header_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/SalesOrderHeader.csv")
         .toDF(*sales_order_header_columns)
)

# ==========================
# Sales Person
# ==========================

sales_person_columns = [
    "BusinessEntityID",
    "TerritoryID",
    "SalesQuota",
    "Bonus",
    "CommissionPct",
    "SalesYTD",
    "SalesLastYear",
    "rowguid",
    "ModifiedDate"
]

sales_person_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/SalesPerson.csv")
         .toDF(*sales_person_columns)
)

# ==========================
# Sales Territory
# ==========================

sales_territory_columns = [
    "TerritoryID",
    "Name",
    "CountryRegionCode",
    "Group",
    "SalesYTD",
    "SalesLastYear",
    "CostYTD",
    "CostLastYear",
    "rowguid",
    "ModifiedDate"
]

sales_territory_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/SalesTerritory.csv")
         .toDF(*sales_territory_columns)
)

# ==========================
# State Province
# ==========================

state_province_columns = [
    "StateProvinceID",
    "StateProvinceCode",
    "CountryRegionCode",
    "IsOnlyStateProvinceFlag",
    "Name",
    "TerritoryID",
    "rowguid",
    "ModifiedDate"
]

state_province_df = (
    spark.read
         .option("header", False)
         .option("inferSchema", True)
         .csv("/Volumes/workspace/default/adventureworks_raw/StateProvince.csv")
         .toDF(*state_province_columns)
)

# ======================
# CREATE BRONZE SCHEMA
# ======================

spark.sql("""
CREATE SCHEMA IF NOT EXISTS bronze
""")

# =========================
# Save Bronze Delta Tables
# =========================

# 1. Address
address_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.address")


# 2. Country Region
country_region_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.country_region")


# 3. Customer
customer_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.customer")


# 4. Employee
employee_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.employee")


# 5. Person
person_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.person")


# 6. Product
product_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.product")


# 7. Product Category
product_category_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.product_category")


# 8. Product Subcategory
product_subcategory_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.product_subcategory")


# 9. Sales Order Detail
sales_order_detail_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.sales_order_detail")


# 10. Sales Order Header
sales_order_header_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.sales_order_header")


# 11. Sales Person
sales_person_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.sales_person")


# 12. Sales Territory
sales_territory_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.sales_territory")


# 13. State Province
state_province_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze.state_province")