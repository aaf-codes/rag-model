import fitz
import re


# EXTRACT FULL TEXT FROM PDF
def extract_text_from_pdf(pdf_path):

    text = ""

    # Open PDF
    doc = fitz.open(pdf_path)

    # Read all pages
    for page in doc:

        text += page.get_text()

    # Close PDF
    doc.close()

    return text


# EXTRACT PAPER METADATA
def extract_paper_metadata(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    # Read first 2 pages only
    for page_num in range(min(2, len(doc))):

        text += doc[page_num].get_text()

    # Close PDF
    doc.close()

    lines = text.split("\n")

    # FALLBACK VALUES
    title = "Unknown Title"
    authors = "Unknown Author"
    year = "Unknown Year"

    # TITLE
    if len(lines) > 0:

        title = lines[0].strip()

    # AUTHORS
    if len(lines) > 1:

        authors = lines[1].strip()

    # YEAR
    year_match = re.search(
        r"(19|20)\d{2}",
        text
    )

    if year_match:

        year = year_match.group()

    return {
        "title": title,
        "authors": authors,
        "year": year
    }