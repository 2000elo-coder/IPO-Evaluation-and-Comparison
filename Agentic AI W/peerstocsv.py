import pdfplumber
import pandas as pd
import re

RHP_PATH = "agentic rhp.pdf"

def extract_peer_comparison_tables(pdf_path, heading_pattern="Comparison with listed peers"):
    tables_found = []
    heading_page_idx = None

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if re.search(heading_pattern, text, re.IGNORECASE):
                print(f"✅ Found heading on page {i+1}")
                heading_page_idx = i
                break

        if heading_page_idx is None:
            print("❌ Heading not found in the document.")
            return []

        total_pages = len(pdf.pages)   # ✅ FIXED: use pdf.pages, not pdf

        # Extract tables from that page and the next few pages
        for j in range(heading_page_idx, min(heading_page_idx + 3, total_pages)):
            page = pdf.pages[j]
            tables = page.extract_tables()
            for t in tables:
                if t and len(t) > 1:  # ensure it's a real table
                    df = pd.DataFrame(t[1:], columns=t[0])
                    tables_found.append(df)
                    print(f"📄 Extracted table from page {j+1} with {len(df)} rows")

    return tables_found

# === Run the extraction ===
peer_tables = extract_peer_comparison_tables(RHP_PATH)

import pandas as pd

# === Clean and combine all extracted tables safely ===
cleaned_tables = []

for i, df in enumerate(peer_tables, 1):
    # Make column names strings and strip whitespace/newlines
    df.columns = [str(c).strip().replace('\n', ' ') for c in df.columns]

    # Ensure all column names are unique
    seen = {}
    new_cols = []
    for col in df.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 1
            new_cols.append(col)
    df.columns = new_cols

    # Drop completely empty rows
    df = df.dropna(how="all")

    cleaned_tables.append(df)

# Safely combine all tables
combined = pd.concat(cleaned_tables, ignore_index=True)

# Save combined DataFrame as CSV
combined.to_csv("peer_comparison.csv", index=False, encoding="utf-8-sig")

print("✅ All peer comparison tables cleaned and saved as 'peer_comparison.csv'")

