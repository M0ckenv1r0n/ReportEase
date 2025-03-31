from src.agent import create_structured_report
from src.pdf_utils import is_pdf_text_extractable, image_to_pdf_with_ocr, pdf_to_pdf_with_ocr
from src.reporting import generate_report_from_dict
from config import logger
from typing import Optional
import os

def process_input_document(text_input: str, output_pdf_path: str, signature_path: Optional[str],
                           input_filepath: Optional[str] = None) -> bool:
    """Process input text and an optional PDF file to generate a structured report PDF."""
    try:
        if input_filepath:
            if not input_filepath.lower().endswith('.pdf'):
                
                dir_name, base_name = os.path.split(input_filepath)
                file_name, ext = os.path.splitext(base_name)
                new_file_path = os.path.join(dir_name, f"{file_name}_ocr{ext}")

                if image_to_pdf_with_ocr(output_pdf_path = new_file_path, input_filepath = input_filepath):
                    input_filepath = new_file_path
                else:
                    return False
            elif not is_pdf_text_extractable(input_filepath):
                logger.warning("PDF text is not extractable, preparing for OCR: %s", input_filepath)
                dir_name, base_name = os.path.split(input_filepath)
                file_name, ext = os.path.splitext(base_name)
                new_file_path = os.path.join(dir_name, f"{file_name}_ocr{ext}")

                if pdf_to_pdf_with_ocr(output_pdf_path = new_file_path, input_filepath = input_filepath):
                    input_filepath = new_file_path
                else:
                    return False
            # result = edit_pdf_content(text_input, input_filepath, output_pdf_path)
        else:
            content_dict = create_structured_report(text_input)
            title = content_dict.pop("Title", "Generated Report")
            result = generate_report_from_dict(content=content_dict, filename=output_pdf_path, title=title, signature_image=signature_path)
        return result
    except Exception as e:
        logger.exception("Failed to process input document: %s", e)
        return False