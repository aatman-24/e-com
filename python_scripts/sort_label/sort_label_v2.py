import fitz  # PyMuPDF
import pandas as pd
import re

def sort_pdf_by_parent_sku(input_pdf, sku_mapping_csv, output_pdf):
    # Load CSV and normalize column names
    mapping_df = pd.read_csv(sku_mapping_csv)
    mapping_df.columns = [c.strip().lower().replace(" ", "_") for c in mapping_df.columns]

    # Try to locate correct columns
    if not {'parent_sku', 'child_sku'}.issubset(mapping_df.columns):
        raise ValueError(f"CSV columns found: {mapping_df.columns.tolist()} — expected ['parent_sku', 'child_sku']")

    # Create child → parent mapping
    child_to_parent = dict(zip(mapping_df['child_sku'], mapping_df['parent_sku']))

    # Read PDF
    doc = fitz.open(input_pdf)
    sku_pattern = re.compile(r'\b[a-zA-Z0-9_]+_[a-zA-Z0-9_]+_[a-zA-Z0-9_]+\b')
    page_info = []

    # Extract SKUs
    for i, page in enumerate(doc):
        text = page.get_text("text")
        match = sku_pattern.search(text)
        if match:
            sku = match.group(0)
            parent = child_to_parent.get(sku, sku)
            page_info.append((i, parent, sku))
            print(f"Page {i+1}: SKU={sku}, Parent={parent}")
        else:
            page_info.append((i, "zzzzzz", "unknown"))
            print(f"⚠️ No SKU found on page {i+1}, placed last.")

    # Sort
    sorted_pages = sorted(page_info, key=lambda x: (x[1].lower(), x[2].lower()))

    # Write new PDF
    new_doc = fitz.open()
    for page_index, parent, sku in sorted_pages:
        new_doc.insert_pdf(doc, from_page=page_index, to_page=page_index)
        print(f"Added page {page_index+1} (Parent: {parent}, SKU: {sku})")

    new_doc.save(output_pdf)
    print(f"\n✅ Sorted PDF saved as: {output_pdf}")

# Example usage
# Example usage
sort_pdf_by_parent_sku(
    input_pdf="data/2.pdf",
    sku_mapping_csv="data/sku_mapping.csv",
    output_pdf="sorted_by_parent_sku_v2.pdf"
)

