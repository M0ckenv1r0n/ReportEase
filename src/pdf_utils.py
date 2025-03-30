import fitz
import PyPDF2
from typing import Any
from config import logger


def replace_text_in_pdf(pdf_path: str, output_path: str, old_text: str, new_text: str) -> None:
    """Replace occurrences of specific text in a PDF file with new text."""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text_instances = page.search_for(old_text)
            # Redact found text with a white box
            for inst in text_instances:
                page.add_redact_annot(inst, fill=(1, 1, 1))
            page.apply_redactions()
            for inst in text_instances:
                page.insert_text((inst.x0, inst.y1 - 1), new_text, fontsize=inst.y1 - inst.y0)
        doc.save(output_path)
        logger.info("Replaced text in PDF and saved to '%s'", output_path)
    except fitz.FitzError as e:
        logger.exception("Error replacing text in PDF: %s", e)
    except Exception as e:
        logger.exception("Unexpected error: %s", e)


def is_pdf_text_extractable(file_path: str, min_chars: int = 10) -> bool:
    """Check if text can be extracted from the PDF."""
    try:
        with open(file_path, 'rb') as f:
            reader: Any = PyPDF2.PdfReader(f)
            extracted_text: str = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text
            is_extractable = len(extracted_text.strip()) >= min_chars
            logger.info("Text extractable from '%s': %s", file_path, is_extractable)
            return is_extractable
    except PyPDF2.PdfReaderError as e:
        logger.exception("Error processing PDF for text extraction: %s", e)
        return False
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        return False

    
def image_to_pdf_with_ocr(output_pdf_path:str, input_filepath:str) -> bool:
    pass

def pdf_to_pdf_with_ocr(output_pdf_path:str, input_filepath:str) -> bool:
    pass