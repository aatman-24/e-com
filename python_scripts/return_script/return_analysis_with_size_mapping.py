import pandas as pd
from datetime import datetime
from pathlib import Path

# === CONFIG ===
returns_file = "data/intransit________next_3_months__2025-10-25_14_0-14_59_3148301__.csv"
mapping_file = "data/sku_mapping.csv"
skiprows = 7  # skip first lines from CSV
output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

# === LOAD DATA ===
df = pd.read_csv(returns_file, skiprows=skiprows)
mapping = pd.read_csv(mapping_file)

# === CLEAN COLUMNS ===
df.columns = df.columns.str.strip()
df["SKU"] = df["SKU"].astype(str).str.strip()
df["Variation"] = df["Variation"].astype(str).str.strip()
mapping["Parent_SKU"] = mapping["Parent_SKU"].astype(str).str.strip()
mapping["Child_SKU"] = mapping["Child_SKU"].astype(str).str.strip()

# === MERGE PARENT-CHILD ===
df = df.merge(mapping, left_on="SKU", right_on="Child_SKU", how="left")
df["Parent_SKU"] = df["Parent_SKU"].fillna(df["SKU"])

# === SIZE MAPPING (Customer -> Production) ===
size_mapping = {
    "6-12 Months": "1-2 Years",
    "0-1 Years": "1-2 Years",
    "1-2 Years": "1-2 Years",
    "2-3 Years": "3-4 Years",
    "3-4 Years": "3-4 Years",
    "4-5 Years": "5-6 Years",
    "5-6 Years": "5-6 Years",
    "6-7 Years": "7-8 Years",
    "7-8 Years": "7-8 Years",
    "8-9 Years": "9-10 Years",
    "9-10 Years": "9-10 Years",
    "10-11 Years": "11-12 Years",
    "11-12 Years": "11-12 Years",
    "12-13 Years": "13-14 Years",
    "13-14 Years": "13-14 Years",
    "14-15 Years": "13-14 Years"
}

# Define production size order
production_size_order = [
    "1-2 Years", "3-4 Years", "5-6 Years", "7-8 Years",
    "9-10 Years", "11-12 Years", "13-14 Years"
]
prod_order_index = {s: i for i, s in enumerate(production_size_order)}

# === MAP TO PRODUCTION SIZE ===
df["Production_Size"] = df["Variation"].map(size_mapping).fillna(df["Variation"])
df["Production_Size_sort_idx"] = df["Production_Size"].map(prod_order_index).fillna(len(prod_order_index)).astype(int)

# === GROUP BY Parent_SKU + Production_Size ===
production_summary = (
    df.groupby(["Parent_SKU", "Production_Size", "Production_Size_sort_idx"], observed=True)["Qty"]
    .sum()
    .reset_index()
    .sort_values(["Parent_SKU", "Production_Size_sort_idx"])
    .drop(columns="Production_Size_sort_idx")
)

# === ADD BLANK ROW AFTER EACH Parent_SKU ===
grouped_rows = []
for parent, group in production_summary.groupby("Parent_SKU", sort=False):
    grouped_rows.append(group)
    grouped_rows.append(pd.DataFrame([["", "", ""]], columns=production_summary.columns))

production_summary_spaced = pd.concat(grouped_rows, ignore_index=True)

# === SAVE EXCEL REPORT ===
date_str = datetime.now().strftime("%d-%m-%Y")
output_file = output_dir / f"{date_str}_meesho_production_size_report.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    production_summary_spaced.to_excel(writer, sheet_name="Parent+Production Detailed", index=False)

print(f"\n✅ Report saved successfully at: {output_file}")
