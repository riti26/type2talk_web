class Language:
    def __init__(self, language_id: int, name: str, code: str):
        self.language_id = language_id
        self.name = name
        self.code = code

    def __repr__(self):
        return f"Language(id={self.language_id}, name='{self.name}', code='{self.code}')"
