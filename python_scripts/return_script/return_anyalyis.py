import pandas as pd
from datetime import datetime

# === 1️⃣ File Paths ===
returns_file = "data/intransit________next_3_months__2025-10-25_14_0-14_59_3148301__.csv"   # your main Meesho returns file
mapping_file = "data/sku_mapping.csv" # parent-child mapping file

# === 2️⃣ Load Data (skip first 8 rows) ===
df = pd.read_csv(returns_file, skiprows=7)
mapping = pd.read_csv(mapping_file)

# === 3️⃣ Clean Columns ===
df.columns = df.columns.str.strip()
df["SKU"] = df["SKU"].astype(str).str.strip()
df["Variation"] = df["Variation"].astype(str).str.strip()
mapping["Parent_SKU"] = mapping["Parent_SKU"].astype(str).str.strip()
mapping["Child_SKU"] = mapping["Child_SKU"].astype(str).str.strip()

# === 4️⃣ Merge Mapping ===
df = df.merge(mapping, left_on="SKU", right_on="Child_SKU", how="left")
df["Parent_SKU"] = df["Parent_SKU"].fillna(df["SKU"])

# === 5️⃣ Define custom size order ===
size_order = [
    "6-12 Months",
    "0-1 Years",
    "1-2 Years",
    "2-3 Years",
    "3-4 Years",
    "4-5 Years",
    "5-6 Years",
    "6-7 Years",
    "7-8 Years",
    "8-9 Years",
    "9-10 Years",
    "10-11 Years",
    "11-12 Years",
    "12-13 Years",
    "13-14 Years",
    "14-15 Years"
]

# Convert Variation to categorical with fixed order
df["Variation"] = pd.Categorical(df["Variation"], categories=size_order, ordered=True)

# === 6️⃣ Group by Parent SKU + Size (sorted) ===
sku_size_summary = (
    df.groupby(["Parent_SKU", "Variation"], observed=True)["Qty"]
    .sum()
    .reset_index()
    .sort_values(["Parent_SKU", "Variation"])
)

# === 7️⃣ Add blank row after each Parent_SKU ===
grouped_rows = []
for parent, group in sku_size_summary.groupby("Parent_SKU"):
    grouped_rows.append(group)
    grouped_rows.append(pd.DataFrame([["", "", ""]], columns=sku_size_summary.columns))

sku_size_summary_spaced = pd.concat(grouped_rows, ignore_index=True)

# === 8️⃣ Readable grouped summary for console and 2nd sheet ===
grouped = (
    sku_size_summary.groupby("Parent_SKU")
    .apply(lambda x: dict(zip(x["Variation"], x["Qty"])))
    .reset_index()
)
grouped.columns = ["Parent_SKU", "Size_Wise_Returns"]

# === 9️⃣ Save Excel Report ===
date_str = datetime.now().strftime("%d-%m-%Y")
output_file = f"output/{date_str}_meesho_return_analysis_valmo.xlsx"
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    sku_size_summary_spaced.to_excel(writer, sheet_name="Parent+Size Detailed", index=False)
    grouped.to_excel(writer, sheet_name="Grouped Report", index=False)

# === 🔟 Console Output ===
print(f"\n✅ Report saved successfully at: {output_file}")
