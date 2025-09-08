from flask import render_template
from app.utils.add_data_manager import AppDataManager
from db.user_session_dao import UserSessionDAO

class PhraseToolbar:
    def __init__(self, user):
        self.user = user
        self.unread_count = 0
        if user.session_token:
            self.load_state()

    def load_state(self):
        user = UserSessionDAO.get_user_info(AppDataManager.load_session())
    
    def render(self):
        return render_template("components/phrase_toolbar.html", phrase_toolbar=self)
