import ffmpeg
from config import logger, LOW_MODEL, HIGH_MODEL
from pywhispercpp.model import Model

def convert_audio(audio_filepath:str, converted_audio_filepath:str) -> bool:
    try:
        (
            ffmpeg
            .input(audio_filepath)
            .output(converted_audio_filepath, ar=16000, ac=1, c='pcm_s16le')
            .run(overwrite_output=True)
        )
        return True
    except Exception as e:
        logger.error(f"Error during conversion: {e}")
        return False
    

def transcribe_audio_with_whisper(audio_path: str, model: str) -> str:
    """Transcribe audio using Whisper and return the transcript."""
    model_instance = Model(LOW_MODEL if model == 1 else HIGH_MODEL)
    try:
        segments = model_instance.transcribe(audio_path)
        transcript = " ".join(segment.text for segment in segments)
        return transcript
    except Exception as e:
        logger.exception("Error during transcription: %s", e)
        return "Error: " + str(e)
    