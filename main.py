import pandas as pd
import os


# STEP 1: DEFINE PATHS

RAW_PATH = "data/"
SILVER_PATH = "silver/"
GOLD_PATH = "gold/"

os.makedirs(SILVER_PATH, exist_ok=True)
os.makedirs(GOLD_PATH, exist_ok=True)


# STEP 2: LOAD RAW DATA (BRONZE LAYER)

print("🔹 Loading Bronze Layer (raw CSVs)...")

sales = pd.read_csv(RAW_PATH + "sales.csv")
customers = pd.read_csv(RAW_PATH + "customers.csv")
products = pd.read_csv(RAW_PATH + "products.csv")
stores = pd.read_csv(RAW_PATH + "stores.csv")
dates = pd.read_csv(RAW_PATH + "dates.csv")

print(
    f" Raw data loaded successfully! Sales rows: {len(sales)}, Customers: {len(customers)}, Products: {len(products)}")

# STEP 3: CLEAN DATA (SILVER LAYER)

print("🔹 Cleaning data for Silver Layer...")

# Drop duplicates
for df in [sales, customers, products, stores, dates]:
    df.drop_duplicates(inplace=True)

# Handle missing values
sales.fillna({'revenue': 0, 'quantity': 0}, inplace=True)

# Standardize column names
for df in [sales, customers, products, stores, dates]:
    df.columns = df.columns.str.replace(
        "ï»¿", "", regex=False)  # remove BOM if present
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Save cleaned data
sales.to_csv(SILVER_PATH + "sales_clean.csv", index=False)
customers.to_csv(SILVER_PATH + "customers_clean.csv", index=False)
products.to_csv(SILVER_PATH + "products_clean.csv", index=False)
stores.to_csv(SILVER_PATH + "stores_clean.csv", index=False)
dates.to_csv(SILVER_PATH + "dates_clean.csv", index=False)

print(" Cleaned data saved to the Silver Layer.")

# STEP 4: LOAD CLEANED DATA (SILVER → MEMORY)

print("🔹 Loading Silver Layer for Gold transformation...")

sales = pd.read_csv(SILVER_PATH + "sales_clean.csv", encoding="utf-8-sig")
customers = pd.read_csv(
    SILVER_PATH + "customers_clean.csv", encoding="utf-8-sig")
products = pd.read_csv(
    SILVER_PATH + "products_clean.csv", encoding="utf-8-sig")
stores = pd.read_csv(SILVER_PATH + "stores_clean.csv", encoding="utf-8-sig")
dates = pd.read_csv(SILVER_PATH + "dates_clean.csv", encoding="utf-8-sig")

# Clean column names again for safety
for df in [sales, customers, products, stores, dates]:
    df.columns = df.columns.str.replace("ï»¿", "", regex=False)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print(" Silver Layer loaded and standardized.")


# STEP 5: BUILD GOLD LAYER (STAR SCHEMA)

print("🔹 Building Gold Layer (Star Schema)...")

# ----- Dimension Tables -----
ProductDim = products.copy()
ProductDim["product_key"] = ProductDim["product_id"]
ProductDim = ProductDim[["product_key", "product_name", "category", "brand"]]
ProductDim.to_csv(GOLD_PATH + "ProductDim.csv", index=False)

CustomerDim = customers.copy()
CustomerDim["customer_key"] = CustomerDim["customer_id"]
CustomerDim = CustomerDim[["customer_key",
                           "name", "gender", "city", "join_date"]]
CustomerDim.to_csv(GOLD_PATH + "CustomerDim.csv", index=False)

StoreDim = stores.copy()
StoreDim["store_key"] = StoreDim["store_id"]
StoreDim = StoreDim[["store_key", "store_name", "region"]]
StoreDim.to_csv(GOLD_PATH + "StoreDim.csv", index=False)

DateDim = dates.copy()
DateDim["date_key"] = DateDim["date_id"]
DateDim = DateDim[["date_key", "date", "month", "year"]]
DateDim.to_csv(GOLD_PATH + "DateDim.csv", index=False)

# ----- Fact Table -----
SalesFact = sales.copy()
SalesFact.rename(columns={
    "product_id": "product_key",
    "customer_id": "customer_key",
    "store_id": "store_key",
    "date_id": "date_key"
}, inplace=True)

SalesFact = SalesFact[["sale_id", "date_key", "product_key",
                       "customer_key", "store_key", "quantity", "revenue"]]
SalesFact.to_csv(GOLD_PATH + "SalesFact.csv", index=False)

print(" Gold Layer created successfully! Star Schema ready.")
print("✨ Pipeline completed successfully (Bronze → Silver → Gold).")

# STEP 6: ANALYSIS & VISUALIZATION (Querying the Gold Layer)
print("Running analytical queries on the Gold Layer...")

# --- Load the Gold Layer tables ---
SalesFact = pd.read_csv(GOLD_PATH + "SalesFact.csv")
ProductDim = pd.read_csv(GOLD_PATH + "ProductDim.csv")
CustomerDim = pd.read_csv(GOLD_PATH + "CustomerDim.csv")
StoreDim = pd.read_csv(GOLD_PATH + "StoreDim.csv")
DateDim = pd.read_csv(GOLD_PATH + "DateDim.csv")

# ---  Total Revenue by Region ---
revenue_region = (
    SalesFact.merge(StoreDim, on="store_key")
    .groupby("region")["revenue"]
    .sum()
    .reset_index()
    .sort_values("revenue", ascending=False)
)
print("\n💰 Total Revenue by Region:")
print(revenue_region)

# ---  Top-Selling Product ---
revenue_product = (
    SalesFact.merge(ProductDim, on="product_key")
    .groupby("product_name")["revenue"]
    .sum()
    .reset_index()
    .sort_values("revenue", ascending=False)
)
print("\n🏆 Top-Selling Product:")
print(revenue_product.head(3))

# ---  Revenue by Month ---
revenue_month = (
    SalesFact.merge(DateDim, on="date_key")
    .groupby("month")["revenue"]
    .sum()
    .reset_index()
)
print("\n Revenue by Month:")
print(revenue_month)