import fitz  # PyMuPDF
import pandas as pd
import re

def sort_pdf_by_parent_sku(input_pdf, sku_mapping_csv, output_pdf):
    # Load mapping file
    mapping_df = pd.read_csv(sku_mapping_csv)
    mapping_df.columns = [c.strip().lower().replace(" ", "_") for c in mapping_df.columns]

    if not {'parent_sku', 'child_sku'}.issubset(mapping_df.columns):
        raise ValueError(f"CSV columns found: {mapping_df.columns.tolist()} — expected ['parent_sku', 'child_sku']")

    # Map child → parent
    child_to_parent = dict(zip(mapping_df['child_sku'], mapping_df['parent_sku']))

    # Open PDF
    doc = fitz.open(input_pdf)
    sku_pattern = re.compile(r'\b[a-zA-Z0-9_]+_[a-zA-Z0-9_]+_[a-zA-Z0-9_]+\b')
    page_info = []

    for i, page in enumerate(doc):
        text = page.get_text("text")
        skus = sku_pattern.findall(text)

        if not skus:
            print(f"⚠️ No SKU found on page {i+1}, will be placed last.")
            page_info.append((i, "zzzzzz", "unknown", False))
            continue

        # Determine parent for each SKU
        parents = [child_to_parent.get(s, s) for s in skus]
        is_combo = len(skus) > 1  # True if multiple SKUs
        parent = parents[0] if parents else "unknown"

        print(f"Page {i+1}: SKUs={skus}, Parent={parent}, Combo={is_combo}")
        page_info.append((i, parent, skus[0], is_combo))

    # Sort order:
    # 1️⃣ Combo pages first
    # 2️⃣ Then by parent SKU
    # 3️⃣ Then by SKU
    sorted_pages = sorted(
        page_info,
        key=lambda x: (not x[3], x[1].lower(), x[2].lower())
    )

    # Create sorted PDF
    new_doc = fitz.open()
    for page_index, parent, sku, is_combo in sorted_pages:
        new_doc.insert_pdf(doc, from_page=page_index, to_page=page_index)
        print(f"Added page {page_index+1} (Parent: {parent}, SKU: {sku}, Combo={is_combo})")

    new_doc.save(output_pdf)
    print(f"\n✅ Sorted PDF saved as: {output_pdf}")

# Example usage
# Example usage
sort_pdf_by_parent_sku(
    input_pdf="data/2.pdf",
    sku_mapping_csv="data/sku_mapping.csv",
    output_pdf="sorted_by_parent_sku_v3.pdf"
)

