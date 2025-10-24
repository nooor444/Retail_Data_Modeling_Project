# 🏬 Retail Data Modeling (ETL + Star Schema)

This project simulates a **mini data warehouse pipeline** for a retail business.  
It demonstrates a complete **ETL process** — from raw data ingestion to a clean **Star Schema** model — built entirely in Python using **Pandas**.

---

## 🚀 Project Overview

The goal of this project is to showcase:
- End-to-end **data transformation (Bronze → Silver → Gold)**  
- **Data cleaning, standardization, and modeling**
- Construction of a **Star Schema** for analytics  
- Simple analytical queries on the modeled data (e.g., revenue by region, top products)

---

## 🧱 Architecture

            ┌────────────────────────┐
            │     Bronze Layer       │
            │ (Raw CSV files /data)  │
            └──────────┬─────────────┘
                       │
                       ▼
            ┌────────────────────────┐
            │     Silver Layer       │
            │ (Cleaned CSVs /silver) │
            └──────────┬─────────────┘
                       │
                       ▼
            ┌────────────────────────┐
            │      Gold Layer        │
            │ (Star Schema /gold)    │
            └────────────────────────┘

---

## 📂 Project Structure

Retail_Data_Modeling_Project/
│
├── data/ # Bronze: Raw data (input CSVs)
├── silver/ # Silver: Cleaned & standardized data
├── gold/ # Gold: Fact & Dimension tables
│ ├── SalesFact.csv
│ ├── ProductDim.csv
│ ├── CustomerDim.csv
│ ├── StoreDim.csv
│ └── DateDim.csv
├── venv/ # Python virtual environment
└── main.py # ETL + Data Modeling + Query script


---

## 🧰 Technologies Used

| Tool | Purpose |
|------|----------|
| **Python (Pandas)** | Data cleaning and transformations |
| **Matplotlib (optional)** | Data visualization (can be skipped) |
| **CSV Storage** | Simulated data lake / warehouse layers |

---

## ⚙️ How to Run the Project

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/Retail_Data_Modeling_Project.git
   cd Retail_Data_Modeling_Project
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
Run the ETL pipeline
python main.py

---
## Outputs
Cleaned data → /silver
Star Schema tables → /gold
Query results printed in terminal
