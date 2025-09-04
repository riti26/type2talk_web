# app/helpers/phrase_toolbar.py
from flask import session
from utils.tts.gtts_service import TextToSpeech

tts = TextToSpeech()

class PhraseToolbar:
    SESSION_KEY = "toolbar_phrase"

    @classmethod
    def add_word(cls, text, icon=None):
        phrase = session.get(cls.SESSION_KEY, [])
        phrase.append({"text": text, "icon": icon})
        session[cls.SESSION_KEY] = phrase

    @classmethod
    def remove_last(cls):
        phrase = session.get(cls.SESSION_KEY, [])
        if phrase:
            phrase.pop()
            session[cls.SESSION_KEY] = phrase

    @classmethod
    def clear(cls):
        session[cls.SESSION_KEY] = []

    @classmethod
    def speak(cls):
        phrase = session.get(cls.SESSION_KEY, [])
        if phrase:
            text = " ".join([w["text"] for w in phrase])
            tts.play_text(text)

    @classmethod
    def get_phrase(cls):
        return session.get(cls.SESSION_KEY, [])
