from sqlite3 import IntegrityError
from db.connection import get_connection
from db.user_session_dao import UserSessionDAO
from app.models.user import User
from app.utils.add_data_manager import AppDataManager
from app.utils.password.hash import encrypt_password, verify_password

# Custom exceptions for better error handling
class UsernameExistsError(Exception):
    pass

class EmailExistsError(Exception):
    pass


class UserDAO:
    @staticmethod
    def register_user(username: str, email: str, password: str):
        """
        Registers a new user in the database.
        Raises:
            UsernameExistsError: if username is taken
            EmailExistsError: if email is already registered
        """
        username = username.strip().lower()
        email = email.strip().lower()

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, email, password, language)
                    VALUES (?, ?, ?, 'en')
                """, (username, email, encrypt_password(password)))
                conn.commit()

        except IntegrityError as e:
            error_message = str(e).lower()
            if "users.username" in error_message:
                raise UsernameExistsError("Username already exists")
            elif "users.email" in error_message:
                raise EmailExistsError("Email already registered")
            else:
                raise

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()

        users = []
        for row in rows:
            user = User(
                user_id=row[0],
                username=row[1],
                email=row[2],
                password=row[3],
                language=row[4]
            )
            users.append(user)

        return users

    @staticmethod
    def get_by_id(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User(
                user_id=row[0],
                username=row[1],
                email=row[2],
                password=row[3],
                language=row[4]
            )
        return None

    @staticmethod
    def update(user: User):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET username = ?, email = ?, language = ?
            WHERE user_id = ?
        """, (user.username, user.email, user.language, user.user_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_language(user_id, language):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET language = ?
            WHERE user_id = ?
        """, (language, user_id))

        AppDataManager.save_language(code=language)
        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """
        Resets password after verifying old password and meeting requirements.
        Returns (success: bool, message: str)
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "User not found."

        stored_password = row[0]
        if not verify_password(stored_password, old_password):
            conn.close()
            return False, "Old password is incorrect."

        # Password validation
        if len(new_password) < 8:
            conn.close()
            return False, "Password must be at least 8 characters long."
        if not any(c.isupper() for c in new_password):
            conn.close()
            return False, "Password must contain at least one uppercase letter."
        if not any(c.islower() for c in new_password):
            conn.close()
            return False, "Password must contain at least one lowercase letter."
        if not any(c.isdigit() for c in new_password):
            conn.close()
            return False, "Password must contain at least one digit."
        if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for c in new_password):
            conn.close()
            return False, "Password must contain at least one special character."
        
        hashed_password = encrypt_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (hashed_password, user_id))
        conn.commit()
        conn.close()
        return True, "Password updated successfully."

    @staticmethod
    def get_user_by_email(email: str):
        """
        Retrieves a user record by email.
        Returns a User object if found, else None.
        """
        email = email.strip().lower()
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row[0],
                    username=row[1],
                    email=row[2],
                    password=row[3],
                    language=row[4]
                )
            return None

    @staticmethod
    def get_user_by_username(username: str):
        username = username.strip().lower()
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            return cursor.fetchone()
        
    @staticmethod
    def force_reset_password(user_id, new_password):
        """
        Resets password after verifying old password and meeting requirements.
        Returns (success: bool, message: str)
        """
        conn = get_connection()
        cursor = conn.cursor()

        if not new_password or not new_password.strip():
            conn.close()
            return False, "Password shouldn't be empty!"

        hash_password = encrypt_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (hash_password, user_id))
        conn.commit()
        conn.close()
        return True, "Password updated successfully."
    
    @staticmethod
    def login(username: str, password: str):
        """
        Logs in a user by username.
        Returns:
            tuple(User object, session_token) if successful, else (None, None)
        """
        username = username.strip().lower()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()

            if not row:
                return None, "username"   # No user found

            stored_password = row[3]  # Password column

            # Verify password
            if not verify_password(stored_password, password):
                return None, "password"  # Wrong password

            # Create User object
            user = User(
                user_id=row[0],
                username=row[1],
                email=row[2],
                password=row[3],
                language=row[4]
            )

            # Generate session token
            session_token = AppDataManager.generate_session_token()
            UserSessionDAO.create_session(user.user_id, session_token)
            AppDataManager.save_language(user.language)

            return user, session_token
        