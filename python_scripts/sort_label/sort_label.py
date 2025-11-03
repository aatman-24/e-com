import fitz  # PyMuPDF
import re

def sort_pdf_by_sku(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    page_skus = []

    # Pattern to find SKU (e.g. boy_run_yellow_c1)
    sku_pattern = re.compile(r'\b[a-zA-Z0-9_]+_[a-zA-Z0-9_]+_[a-zA-Z0-9_]+\b')

    # Extract SKU from each page
    for i, page in enumerate(doc):
        text = page.get_text("text")
        # Find line starting with SKU
        match = sku_pattern.search(text)
        if match:
            sku = match.group(0)
            page_skus.append((i, sku))
            print(f"Page {i+1}: Found SKU {sku}")
        else:
            print(f"⚠️ No SKU found on page {i+1}, keeping it at the end.")
            page_skus.append((i, "zzzzzzzz"))  # ensures missing SKU goes last

    # Sort by SKU
    sorted_pages = sorted(page_skus, key=lambda x: x[1].lower())

    # Create new PDF in sorted order
    new_doc = fitz.open()
    for page_index, sku in sorted_pages:
        new_doc.insert_pdf(doc, from_page=page_index, to_page=page_index)
        print(f"Added page {page_index+1} (SKU: {sku})")

    new_doc.save(output_pdf)
    print(f"\n✅ New sorted PDF saved as: {output_pdf}")

# Example usage
sort_pdf_by_sku("data/1.pdf", "sorted_by_sku.pdf")
