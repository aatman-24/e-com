import fitz  # PyMuPDF
import pandas as pd
import re
from datetime import datetime
import os

def sort_pdf_by_parent_sku(input_pdf, sku_mapping_csv, output_pdf):
    # Load mapping and normalize column names
    mapping_df = pd.read_csv(sku_mapping_csv)
    mapping_df.columns = [c.strip().lower().replace(" ", "_") for c in mapping_df.columns]

    if not {'parent_sku', 'child_sku'}.issubset(mapping_df.columns):
        raise ValueError(f"CSV columns found: {mapping_df.columns.tolist()} — expected ['parent_sku', 'child_sku']")

    # Build child → parent map
    child_to_parent = dict(zip(mapping_df['child_sku'], mapping_df['parent_sku']))

    # Open the input PDF
    doc = fitz.open(input_pdf)

    # Patterns
    sku_pattern = re.compile(r'\b[a-zA-Z0-9_]+_[a-zA-Z0-9_]+_[a-zA-Z0-9_]+\b')
    qty_pattern = re.compile(r'\bQty\s*([0-9]+)\b', re.IGNORECASE)

    page_info = []

    for i, page in enumerate(doc):
        text = page.get_text("text")

        # Find SKUs and quantities
        skus = sku_pattern.findall(text)
        qty_match = re.search(r'\bQty\s*([0-9]+)\b', text, re.IGNORECASE)
        qty = int(qty_match.group(1)) if qty_match else 1

        # Determine combo conditions
        is_combo = len(skus) > 1 or qty > 1

        if not skus:
            print(f"⚠️ No SKU found on page {i+1}, placing at end.")
            page_info.append((i, "zzzzzz", "unknown", False))
            continue

        sku = skus[0]
        parent = child_to_parent.get(sku, sku)

        print(f"Page {i+1}: SKUs={skus}, Qty={qty}, Parent={parent}, Combo={is_combo}")
        page_info.append((i, parent, sku, is_combo))

    # Sort: combo first → parent → SKU
    sorted_pages = sorted(
        page_info,
        key=lambda x: (not x[3], x[1].lower(), x[2].lower())
    )

    # Create new PDF
    new_doc = fitz.open()
    combo_count = 0

    for page_index, parent, sku, is_combo in sorted_pages:
        if is_combo:
            combo_count += 1
        new_doc.insert_pdf(doc, from_page=page_index, to_page=page_index)
        print(f"Added page {page_index+1} (Parent: {parent}, SKU: {sku}, Combo={is_combo})")

    new_doc.save(output_pdf)
    print(f"\n✅ Sorted PDF saved as: {output_pdf}")
    print(f"📊 Combo pages: {combo_count} | Total pages: {len(page_info)}")


now = datetime.now()
hour_str = now.strftime("%H")                # first 2-digit hour to differentiate runs in a day
date_str = now.strftime("%d-%b-%Y").lower()  # e.g. 31-oct-2025
os.makedirs("output", exist_ok=True)
output_pdf = f"output/{date_str}_label_{hour_str}.pdf"

# Example usage
# Example usage
sort_pdf_by_parent_sku(
    input_pdf="data/2.pdf",
    sku_mapping_csv="data/sku_mapping.csv",
    output_pdf=output_pdf
)

