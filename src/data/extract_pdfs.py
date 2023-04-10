import PyPDF2
import os
from PIL import Image, UnidentifiedImageError
import io
import imghdr


def extract_text_and_images(input_pdf_path, output_text_dir, output_img_dir):
    # Create the output directories if they don't exist
    os.makedirs(output_text_dir, exist_ok=True)
    os.makedirs(output_img_dir, exist_ok=True)
    with open(input_pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        for page_number, pdf_page in enumerate(pdf.pages):
            # Extract text from the current page
            page_text = pdf_page.extract_text()
            # Save text to the output text directory
            with open(os.path.join(output_text_dir, f"page_{page_number}.txt"), "w") as text_file:
                text_file.write(page_text)
            img_count = 0
            # Check if the page has XObjects
            if '/XObject' in pdf_page['/Resources']:
                # Extract images using PyPDF2
                x_object = pdf_page['/Resources']['/XObject'].get_object()
                for obj in x_object:
                    if x_object[obj]['/Subtype'] == '/Image':
                        size = (x_object[obj]['/Width'], x_object[obj]['/Height'])
                        data = x_object[obj].get_data()
                        try:
                            img = Image.open(io.BytesIO(data))
                            img.save(os.path.join(output_img_dir, f"page_{page_number}_image_{img_count}.png"))
                            img_count += 1
                        except UnidentifiedImageError:
                            img_format = imghdr.what(None, data)
                            print(f"Unable to process image {img_count} on page {page_number}. Image format: {img_format}")
        # Print the page number, text, and the number of images
            print(f"Page {page_number}:")
            print(f"Number of images: {img_count}")
            print("\n")


# extract_text_and_images("data/raw/The_Strange_Consumer_PDF_Bookmarked_and_Linked_2015-06-23.pdf", "data/interim/text/strange_by_page", "data/interim/images/strange_by_page")
