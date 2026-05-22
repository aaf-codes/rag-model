import fitz#opens pdf


def extract_text_from_pdf(pdf_path):

    text = ""

    # Open PDF
    doc = fitz.open(pdf_path)

    # Read every page
    for page in doc:#loops
        text += page.get_text()#extracts text from current project and text+= joins all pages togther

    # Close document
    doc.close()

    return text