import io
import uuid

from loader import client_openai


def _get_valid_format_voice(voice: io.BytesIO) -> tuple[str, bytes]:
    result = (f'{uuid.uuid4()}-voice.oga', voice.getvalue())
    return result


async def get_transcription(voice: io.BytesIO) -> str:
    """Accepts voice and generates text from it"""
    formatted_voice = _get_valid_format_voice(voice)
    transcription = await (client_openai.audio.transcriptions.
                           create(file=formatted_voice, model="whisper-1", response_format="text"))
    return transcription


async def get_voice_from_text(text: str) -> bytes:
    """Accepts text and generates speech from it"""
    if text:
        voice = await (client_openai.audio.speech.
                       create(model="tts-1", voice="nova", input=text, response_format='mp3'))
        voice_gpt_b = await voice.aread()

        return voice_gpt_b
