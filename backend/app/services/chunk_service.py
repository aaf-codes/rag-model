import re

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


# STANDARD PAPER HEADINGS
SECTION_HEADERS = [

    "abstract",

    "introduction",

    "methodology",

    "methods",

    "results",

    "discussion",

    "conclusion",

    "references"

]


# SECTION-AWARE CHUNKING
def split_text_into_chunks(text):

    lines = text.split("\n")

    sections = {}

    current_section = "General"

    sections[current_section] = ""

    # DETECT HEADINGS
    for line in lines:

        clean_line = line.strip().lower()

        if clean_line in SECTION_HEADERS:

            current_section = line.strip()

            sections[current_section] = ""

        else:

            sections[current_section] += (
                line + "\n"
            )

    # FALLBACK
    # If no headings found
    if len(sections) == 1:

        sections = {
            "Full Document": text
        }

    # CHUNK INSIDE EACH SECTION
    splitter = RecursiveCharacterTextSplitter(

        chunk_size=300,

        chunk_overlap=30
    )

    final_chunks = []

    for section_name, section_text in sections.items():

        chunks = splitter.split_text(
            section_text
        )

        for chunk in chunks:

            if len(chunk.strip()) > 80:

                final_chunks.append({

                    "section":
                    section_name,

                    "text":
                    chunk

                })

    return final_chunks