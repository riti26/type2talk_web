class User:
    def __init__(self, user_id=None, username=None, email=None, password=None, language=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.language = language

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}, language='{self.language}')"
