
import os
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

# 📁 Input and Output Paths
input_folder = "/home/heritage-foundation/Office/Extraction/archive1"
output_folder = "/home/heritage-foundation/Office/Extraction/pdfs/text_gen"

# ✅ Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# 🔁 Loop through all PDF files in the input folder 
for file in os.listdir(input_folder):
    if not file.lower().endswith(".pdf"):
        continue 

    pdf_path = os.path.join(input_folder, file)
    print(f"\n📘 Processing: {pdf_path}")

    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
    except Exception as e:
        print(f"❌ Failed to read PDF: {e}")
        continue

    full_text = ""
    for page_num in range(1, num_pages + 1):
        try:
            images = convert_from_path(pdf_path, dpi=300, first_page=page_num, last_page=page_num)
            text = pytesseract.image_to_string(images[0], lang="eng+san+hin+malayalam+telugu+gujarati+punjabi+marathi+bengali+odia+tamil+kannada", config="--psm 6")
            full_text += f"\n\n--- Page {page_num} ---\n{text}"
        except Exception as e:
            print(f"⚠️ Error on page {page_num} of {file}: {e}")

    # 📝 Save the OCR Output
    output_filename = os.path.splitext(file)[0] + ".txt"
    output_path = os.path.join(output_folder, output_filename)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"✅ Saved OCR to: {output_path}")
    except Exception as e:
        print(f"❌ Could not save file {output_path}: {e}")
