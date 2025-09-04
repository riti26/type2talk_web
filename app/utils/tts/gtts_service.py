from gtts import gTTS
from kivy.core.audio import SoundLoader
import tempfile
import os

from db.language_dao import LanguageDAO
from utils.add_data_manager import AppDataManager

class TextToSpeech:
    def __init__(self):
        self.sound = None

    def play_text(self, text):
        # Stop and unload existing sound if any
        if self.sound:
            self.sound.stop()
            self.sound.unload()
            self.sound = None

        # Create temp file (will be deleted on playback end)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tmp_file.close()

        # Generate speech and save to temp file
        tts = gTTS(text=text, lang=AppDataManager.get_language())
        tts.save(tmp_file.name)

        # Load sound from temp file
        self.sound = SoundLoader.load(tmp_file.name)
        if self.sound:
            # Bind deletion of temp file when playback stops
            self.sound.bind(on_stop=lambda *args: os.unlink(tmp_file.name))
            self.sound.play()
        else:
            print("Failed to load sound")
            os.unlink(tmp_file.name)
