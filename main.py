import pdfplumber
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configure Gemini AI
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

# Extract Text from PDF (Preserve Structure)
def extract_text_from_pdf(pdf_path):
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

    return "\n\n".join(extracted_text)

# Clean Text Using Gemini AI
def clean_text_with_gemini(text, removal_prompt):
    prompt = f"""
    Here is a formatted document extracted from a PDF:

    {text}

    Instructions: {removal_prompt}

    Return only the cleaned text, keeping the structure like headings, paragraphs, bullet points, and tables.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Save Cleaned Text Back to PDF
def save_cleaned_text_to_pdf(cleaned_text, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    margin = 50
    line_height = 14
    current_y = height - margin

    c.setFont("Helvetica", 12)

    for para in cleaned_text.split("\n"):
        if current_y < margin:
            c.showPage()
            c.setFont("Helvetica", 12)
            current_y = height - margin
        
        c.drawString(margin, current_y, para)
        current_y -= line_height

    c.save()
    print(f"Cleaned PDF saved as: {output_pdf}")

# Main Function
def process_pdf(input_pdf, output_pdf, removal_prompt):
    print("Extracting text while keeping structure...")
    extracted_text = extract_text_from_pdf(input_pdf)

    print("Cleaning content with Gemini AI...")
    cleaned_text = clean_text_with_gemini(extracted_text, removal_prompt)

    print("Saving cleaned text back to PDF...")
    save_cleaned_text_to_pdf(cleaned_text, output_pdf)

# Example Usage
if __name__ == "__main__":
    input_pdf = "input.pdf"  # Replace with your file
    output_pdf = "cleaned_output.pdf"
    removal_prompt = "Remove any personal information, redundant text, and example phrases while keeping the original structure."

    process_pdf(input_pdf, output_pdf, removal_prompt)
