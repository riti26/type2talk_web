from gtts import gTTS
from flask import send_file
import io

from utils.add_data_manager import AppDataManager

class TextToSpeech:
    """
    Generates speech audio from text and returns it as an in-memory file for Flask.
    """

    @staticmethod
    def generate_audio(text):
        """
        Returns a BytesIO object containing MP3 audio.
        """
        tts = gTTS(text=text, lang=AppDataManager.get_language())
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp