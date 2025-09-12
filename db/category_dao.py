from app.models.communication_category import CommunicationCategory
from app.utils.translator.deep_translator_service import translate_to_english_sync
from db.connection import get_connection


class CategoryDAO:
    @staticmethod
    def add(text, user_id=None, icon_path=None, is_standalone=False):
        text = translate_to_english_sync(text)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO communication_category (text, user_id, icon_path, is_standalone)
            VALUES (?, ?, ?, ?)
        """, (text, user_id, icon_path, int(is_standalone)))

        category_id = cursor.lastrowid
        conn.commit()

        cursor.execute("""
            SELECT category_id, text, user_id, icon_path, is_standalone
            FROM communication_category
            WHERE category_id = ?
        """, (category_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return CommunicationCategory(
                category_id=row[0],
                text=row[1],
                user_id=row[2],
                icon_path=row[3],
                is_standalone=bool(row[4])
            )
        return None

    @staticmethod
    def get_all(user_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM communication_category
            WHERE user_id = ?
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()

        categories = []
        for row in rows:
            category = CommunicationCategory(
                category_id=row["category_id"],
                text=row["text"],
                user_id=row["user_id"],
                icon_path=row["icon_path"],
                is_standalone=bool(row["is_standalone"])
            )
            categories.append(category)

        return categories

    @staticmethod
    def get_by_id(category_id: int):
        """Fetch a single category by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category_id, text, user_id, icon_path, is_standalone
            FROM communication_category
            WHERE category_id = ?
        """, (category_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return CommunicationCategory(
                category_id=row[0],
                text=row[1],
                user_id=row[2],
                icon_path=row[3],
                is_standalone=bool(row[4])
            )
        return None

    @staticmethod
    def delete(category_id: int):
        """Delete a single category (items auto-deleted by CASCADE)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM communication_category
            WHERE category_id = ?
        """, (category_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_multiple(category_ids: list[int]):
        """Delete multiple categories (items auto-deleted by CASCADE)."""
        if not category_ids:
            return  # nothing to delete

        conn = get_connection()
        cursor = conn.cursor()
        placeholders = ",".join("?" for _ in category_ids)
        cursor.execute(f"""
            DELETE FROM communication_category
            WHERE category_id IN ({placeholders})
        """, category_ids)
        conn.commit()
        conn.close()

    @staticmethod
    def update(category_id: int, text: str, icon_path: str = None,
               is_standalone: bool = False):
        """
        Update category. If icon_path is None, keep the existing value.
        """
        text = translate_to_english_sync(text)
        conn = get_connection()
        cursor = conn.cursor()

        if icon_path is None:
            cursor.execute("""
                UPDATE communication_category
                SET text = ?, is_standalone = ?
                WHERE category_id = ?
            """, (text, int(is_standalone), category_id))
        else:
            cursor.execute("""
                UPDATE communication_category
                SET text = ?, icon_path = ?, is_standalone = ?
                WHERE category_id = ?
            """, (text, icon_path, int(is_standalone), category_id))

        conn.commit()

        # fetch the updated row
        cursor.execute("""
            SELECT category_id, text, user_id, icon_path, is_standalone
            FROM communication_category
            WHERE category_id = ?
        """, (category_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return CommunicationCategory(
                category_id=row[0],
                text=row[1],
                user_id=row[2],
                icon_path=row[3],
                is_standalone=bool(row[4])
            )
        return None
