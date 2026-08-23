import os
import sys
from pypdf import PdfReader


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = "\n".join(p.extract_text() for p in reader.pages)
    return text


path = "C:/Users/larst/Downloads/Flug Lux - Bud Rechnung.pdf"

print(f"Reading PDF from: {path}")
text = read_pdf(path)
# print(text)

text = text.lower()  # Convert text to lowercase for case-insensitive search

if "lars" in text:
    print("The document is related to Lars.")
    if "rechnung" in text:
        print("The document is a Rechnung.")
elif "maria" in text:
    print("The document is related to Maria.")
    if "rechnung" in text:
        print("The document is a Rechnung.")
else:
    print("The document is not related to Lars or Maria.")
