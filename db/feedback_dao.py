import sqlite3
from db.connection import get_connection

class FeedbackDAO:
    @staticmethod
    def add_feedback(rating: int = None, text: str = None):
        conn = get_connection()
        cursor = conn.cursor()
        # Insert the feedback
        cursor.execute(
            "INSERT INTO feedback (rating, text) VALUES (?, ?)",
            (rating, text)
        )
        conn.commit()
        feedback_id = cursor.lastrowid  # get the inserted ID
        conn.close()
        return feedback_id
    
    from db.connection import get_connection

class FeedbackDAO:
    @staticmethod
    def add_feedback(rating: int = None, feedback: str = None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (rating, feedback) VALUES (?, ?)",
            (rating, feedback)
        )
        conn.commit()
        feedback_id = cursor.lastrowid
        conn.close()
        return feedback_id

    @staticmethod
    def get_feedback(rating: int = None, sort_by: str = "created_at", order: str = "desc"):
        """
        Retrieve feedback from the database.

        :param rating: Optional filter by rating (1-5)
        :param sort_by: Column to sort by ("created_at" or "rating")
        :param order: "asc" or "desc"
        :return: List of rows (dict-like)
        """
        if sort_by not in ("created_at", "rating"):
            sort_by = "created_at"
        if order.lower() not in ("asc", "desc"):
            order = "desc"

        query = "SELECT * FROM feedback WHERE 1=1"
        params = []

        if rating:
            query += " AND rating = ?"
            params.append(rating)

        query += f" ORDER BY {sort_by} {order.upper()}"

        conn = get_connection()
        conn.row_factory = sqlite3.Row  # so we can access columns by name
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Convert to list of dicts
        feedback_list = [dict(row) for row in rows]
        return feedback_list