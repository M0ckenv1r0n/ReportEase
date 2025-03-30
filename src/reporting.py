from config import DEFAULT_FONT_FAMILY, DEFAULT_HEADER_STYLE, DEFAULT_HEADER_SIZE, DEFAULT_SUBHEADER_STYLE, DEFAULT_SUBHEADER_SIZE, DEFAULT_BODY_STYLE, DEFAULT_BODY_SIZE, DEFAULT_FOOTER_STYLE, DEFAULT_FOOTER_SIZE, logger
from datetime import datetime
from tzlocal import get_localzone
from fpdf import FPDF
from typing import Dict

class ReportConfig:
    def __init__(self,
                 font_family: str = DEFAULT_FONT_FAMILY,
                 header_style: str = DEFAULT_HEADER_STYLE, header_size: int = DEFAULT_HEADER_SIZE,
                 subheader_style: str = DEFAULT_SUBHEADER_STYLE, subheader_size: int = DEFAULT_SUBHEADER_SIZE,
                 body_style: str = DEFAULT_BODY_STYLE, body_size: int = DEFAULT_BODY_SIZE,
                 footer_style: str = DEFAULT_FOOTER_STYLE, footer_size: int = DEFAULT_FOOTER_SIZE):
        self.font_family = font_family
        self.header_style = header_style
        self.header_size = header_size
        self.subheader_style = subheader_style
        self.subheader_size = subheader_size
        self.body_style = body_style
        self.body_size = body_size
        self.footer_style = footer_style
        self.footer_size = footer_size


class ScientificPDF(FPDF):
    def __init__(self, config: ReportConfig, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.title_text = title

    def header(self) -> None:
        self.set_font(self.config.font_family, self.config.header_style, self.config.header_size)
        self.cell(0, 10, self.title_text, ln=True, align='C')
        self.set_line_width(0.5)
        self.line(10, 25, self.w - 10, 25)
        self.ln(5)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font(self.config.font_family, self.config.footer_style, self.config.footer_size)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def add_signature_block(pdf: ScientificPDF, config: ReportConfig, date_str: str, signature_image: str = None,
                        signature_block_height: float = 30) -> None:
    target_y = pdf.h - pdf.b_margin - signature_block_height
    if pdf.get_y() > target_y:
        pdf.add_page()
        target_y = pdf.h - pdf.b_margin - signature_block_height
    pdf.set_y(target_y)
    pdf.set_font(config.font_family, config.body_style, config.body_size)
    pdf.cell(60, 10, 'Authorized Signature:', ln=0)
    current_x = pdf.get_x() - 20
    current_y = pdf.get_y()
    if signature_image:
        pdf.image(signature_image, x=current_x, y=current_y, w=40)
    pdf.ln(15)
    pdf.cell(0, 10, f'Creation date: {date_str}', ln=True)


def create_scientific_report(filename: str,
                             config: ReportConfig,
                             content: Dict[str, str],
                             title: str = "Scientific Report",
                             date_str: str = None,
                             signature_image: str = None) -> None:
    pdf = ScientificPDF(config, title)
    pdf.add_page()

    def add_section(header: str, text: str) -> None:
        pdf.set_font(config.font_family, config.subheader_style, config.subheader_size)
        pdf.cell(0, 10, header, ln=True)
        pdf.set_font(config.font_family, config.body_style, config.body_size)
        pdf.multi_cell(0, 8, text)
        pdf.ln(5)

    for section, section_text in content.items():
        add_section(section, section_text)

    if date_str is None:
        local_tz = get_localzone()
        current_time = datetime.now(local_tz)
        date_str = current_time.strftime('%Y-%m-%d %H:%M:%S %Z')


    add_signature_block(pdf, config, date_str, signature_image)
    pdf.output(filename)
    logger.info("Scientific report generated and saved as '%s'", filename)


def generate_report_from_dict(content: Dict[str, str], filename: str, title: str, signature_image: str) -> bool:
    """Generate a PDF report from a dictionary of content."""
    try:
        config = ReportConfig()
        create_scientific_report(
            filename=filename,
            config=config,
            content=content,
            title=title,
            signature_image=signature_image
        )
        return True
    except Exception as e:
        logger.exception("Error generating report from dictionary: %s", e)
        return False