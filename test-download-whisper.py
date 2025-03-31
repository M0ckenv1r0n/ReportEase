import asyncio
import concurrent.futures
import sys
from pywhispercpp.model import Model
from config import LOW_MODEL, HIGH_MODEL, logger

def transcribe_sync(model_name: str, model_label: str) -> str:
    logger.info(f"Testing and/or downloading {model_name} ({model_label} model)")
    model_instance = Model(model_name)
    segments = model_instance.transcribe("test-cvtd.wav")
    transcript = " ".join(segment.text for segment in segments)
    return transcript

async def transcribe_async(model_name: str, model_label: str, timeout: float = 30.0) -> str:
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            transcript = await asyncio.wait_for(
                loop.run_in_executor(executor, transcribe_sync, model_name, model_label),
                timeout=timeout
            )
            # logger.info(f"Transcribing using {model_name} ({model_label} model) completed within {timeout} seconds")
            return transcript
        except asyncio.TimeoutError:
            raise

async def main():
    logger.info("Testing and/or downloading whisper models...")
    try:
        transcript_low = await transcribe_async(LOW_MODEL, "low")
    except asyncio.TimeoutError:
        logger.error("Low model transcription exceeded 30 seconds. "
                     "Please ensure that pywhispercpp is installed correctly.")
        sys.exit(1)
    try:
        transcript_high = await transcribe_async(HIGH_MODEL, "high")
    except asyncio.TimeoutError:
        logger.error("High model transcription exceeded 30 seconds. It is recommended to use the low model instead.")
        sys.exit(1)


    logger.info("Both models transcribed successfully within the time limit. You can use any model.\n")

if __name__ == "__main__":
    asyncio.run(main())