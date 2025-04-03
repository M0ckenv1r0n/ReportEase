import os
import logging
# LLM Model
LLM_MODEL = "llama3.2:3b-instruct-q5_K_M"

# Base directory for the project
BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))

# Folder where uploaded files will be stored
UPLOAD_FOLDER: str = os.path.join(BASE_DIR, 'uploads')

# Define allowed file extensions for audio uploads
ALLOWED_EXTENSIONS: set = {'wav', 'mp3', 'ogg'}

# Folder for storing transcripts
TRANSCRIPT_FOLDER: str = os.path.join(BASE_DIR, 'transcripts')

LOW_MODEL: str = "base"
HIGH_MODEL: str = "large-v3-turbo"

DEFAULT_FONT_FAMILY: str = 'Arial'
DEFAULT_HEADER_STYLE: str = 'B'
DEFAULT_HEADER_SIZE: int = 16
DEFAULT_SUBHEADER_STYLE: str = 'B'
DEFAULT_SUBHEADER_SIZE: int = 14
DEFAULT_BODY_STYLE: str = ''
DEFAULT_BODY_SIZE: int = 12
DEFAULT_FOOTER_STYLE: str = 'I'
DEFAULT_FOOTER_SIZE: int = 8

import logging

logger = logging.getLogger('PROJECT_IU')
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
