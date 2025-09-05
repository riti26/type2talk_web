from db.connection import get_connection
from models.language import Language

class LanguageDAO:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, code FROM languages ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [Language(row[0], row[1], row[2]) for row in rows]

    @staticmethod
    def insert_languages(language_list):
        """Insert multiple languages, expects list of (name, code) tuples."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO languages (name, code) VALUES (?, ?)",
            language_list
        )
        conn.commit()
        conn.close()