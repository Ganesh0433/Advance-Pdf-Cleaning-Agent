import fitz  # PyMuPDF

def extract_text_like_manual_copy(input_pdf):
    """
    Extract text from the PDF using PyMuPDF to mimic manual copying.
    """
    full_text = ""
    try:
        # Open the PDF file
        doc = fitz.open(input_pdf)
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Extract text from the page
            page_text = page.get_text("text")  # "text" mimics manual copying
            if page_text:
                full_text += page_text + "\n\n"  # Separate pages with double newlines
            else:
                print(f"Warning: No text found on page {page_num + 1}")
        doc.close()
    except Exception as e:
        print(f"Error extracting text: {e}")
    return full_text
print(extract_text_like_manual_copy(input_pdf='demo.pdf'))
