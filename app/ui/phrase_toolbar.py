from flask import render_template
from app.utils.add_data_manager import AppDataManager
from db.user_session_dao import UserSessionDAO

class PhraseToolbar:    
    def render(self):
        return render_template("components/phrase_toolbar.html", phrase_toolbar=self)
