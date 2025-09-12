from datetime import datetime, timedelta
from typing import Optional

from app.models.user_session import UserSession
from app.utils.add_data_manager import AppDataManager
from db.connection import get_connection

class UserSessionDAO:
    @staticmethod
    def create_session(user_id, token, days_valid=30, device_id=None):
        expires_at = datetime.utcnow() + timedelta(days=days_valid)
        
        # 1. Save session in the database
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_sessions (user_id, session_token, expires_at, device_id)
                VALUES (?, ?, ?, ?)
            """, (user_id, token, expires_at, device_id))
            conn.commit()

        # 2. Save session locally so app remembers user
        AppDataManager.save_session(token)

    @staticmethod
    def get_session(token: str) -> Optional[UserSession]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_sessions WHERE session_token = ?", (token,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return UserSession(
                session_id=row[0],
                user_id=row[1],
                session_token=row[2],
                created_at=row[3],
                expires_at=row[4]
            )
        return None
    
    
    @staticmethod
    def get_user_id(token: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_sessions WHERE session_token = ?", (token,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[1]
        return None
    
    @staticmethod
    def get_user_info(token: str):
        with get_connection() as conn:
         cursor = conn.cursor()
         cursor.execute("""
            SELECT u.user_id, u.username, u.email
            FROM users u
            JOIN user_sessions s ON u.user_id = s.user_id
            WHERE s.session_token = ?
        """, (token,))
        row = cursor.fetchone()
        if row:
            return {"user_id": row[0], "username": row[1], "email": row[2]}
        return None

    @staticmethod
    def validate_session(token):
        now = datetime.utcnow()
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.* FROM users u
                JOIN user_sessions s ON u.user_id = s.user_id
                WHERE s.session_token = ? AND s.expires_at > ?
            """, (token, now))
            return cursor.fetchone()
        
    @staticmethod
    def logout(token: str) -> bool:
        """
        Logs the user out by deleting their session from DB and clearing local storage.
        Returns True if a session was deleted, False otherwise.
        """
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM user_sessions WHERE session_token = ?",
                    (token,)
                )
                deleted = True
                conn.commit()

            # Clear locally stored session (if any)
            if deleted:
                AppDataManager.clear_session()
                AppDataManager.save_language('en')

            return deleted
        except Exception as e:
            print(f"[Logout Error] {e}")
            return False