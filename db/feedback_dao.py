from db.connection import get_connection

class FeedbackDAO:
    @staticmethod
    def add_feedback(rating: int = None, feedback: str = None):
        conn = get_connection()
        cursor = conn.cursor()
        # Insert the feedback
        cursor.execute(
            "INSERT INTO feedback (rating, feedback) VALUES (?, ?)",
            (rating, feedback)
        )
        conn.commit()
        feedback_id = cursor.lastrowid  # get the inserted ID
        conn.close()
        return feedback_id