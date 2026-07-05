from pypdf import PdfReader

# Open the PDF file
reader = PdfReader("documents/COMPUTER SCIENCE AND ENGINEERING S7 & S8.pdf")

# Count how many pages it has
print(f"Number of pages: {len(reader.pages)}")

# Extract text from all pages and join it into one big string
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

# Print how many characters of text we got, and a small preview
print(f"Total characters extracted: {len(full_text)}")
print("---- Preview of first 500 characters ----")
print(full_text[:500])