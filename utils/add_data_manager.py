from flask import session

class AppDataManager:
    # ------------------- Session -------------------
    @staticmethod
    def save_session(token):
        session['session_token'] = token

    @staticmethod
    def load_session():
        return session.get('session_token')

    @staticmethod
    def clear_session():
        session.pop('session_token', None)

    # ------------------- Language -------------------
    @staticmethod
    def save_language(code):
        session['language'] = code

    @staticmethod
    def get_language():
        return session.get('language', 'en')  # default to 'en'

    @staticmethod
    def clear_language():
        session.pop('language', None)
