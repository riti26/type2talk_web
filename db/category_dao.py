from app.models.communication_category import CommunicationCategory
from app.utils.translator.deep_translator_service import translate_to_english_sync
from db.connection import get_connection

class CategoryDAO:
    @staticmethod
    def add(name, user_id=None, icon_path=None, description=None, is_standalone=False):
        name = translate_to_english_sync(name)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO communication_category (name, user_id, icon_path, description, is_standalone)
            VALUES (?, ?, ?, ?, ?)
        """, (name, user_id, icon_path, description, int(is_standalone)))

        category_id = cursor.lastrowid
        conn.commit()

        cursor.execute("""
            SELECT category_id, name, user_id, icon_path, description, is_standalone
            FROM communication_category
            WHERE category_id = ?
        """, (category_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return CommunicationCategory(
                category_id=row[0],
                name=row[1],
                user_id=row[2],
                icon_path=row[3],
                description=row[4],
                is_standalone=bool(row[5])
            )
        return None

    @staticmethod
    def get_all(user_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM communication_category
            WHERE user_id = ? OR user_id IS NULL
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()

        categories = []
        for row in rows:
            category = CommunicationCategory(
                category_id=row["category_id"],
                name=row["name"],
                user_id=row["user_id"],
                icon_path=row["icon_path"],
                description=row["description"],
                is_standalone=bool(row["is_standalone"])
            )
            categories.append(category)

        return categories

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
    def update(category_id: int, name: str, icon_path: str = None, 
                   description: str = None, is_standalone: bool = False):
        """
        Update all data of a category except category_id and user_id.
        """
        name = translate_to_english_sync(name)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE communication_category
            SET name = ?, icon_path = ?, description = ?, is_standalone = ?
            WHERE category_id = ?
        """, (name, icon_path, description, int(is_standalone), category_id))
        conn.commit()
        conn.close()