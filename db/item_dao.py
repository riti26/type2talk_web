from app.models.communication_item import CommunicationItem
from app.utils.translator.deep_translator_service import translate_to_english_sync
from db.connection import get_connection

class ItemDAO:

    @staticmethod
    def add(category_id, text, icon_path=None):
        text = translate_to_english_sync(text)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO communication_item (category_id, text, icon_path)
            VALUES (?, ?, ?)
        """, (category_id, text, icon_path))

        item_id = cursor.lastrowid
        conn.commit()

        cursor.execute("""
            SELECT item_id, category_id, text, icon_path
            FROM communication_item
            WHERE item_id = ?
        """, (item_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return CommunicationItem(
                item_id=row[0],
                category_id=row[1],
                text=row[2],
                icon_path=row[3]
            )
        return None

    @staticmethod
    def get_by_category(category_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM communication_item WHERE category_id = ?", (category_id,))
        rows = cursor.fetchall()
        conn.close()

        items = []
        for row in rows:
            item = CommunicationItem(
                item_id=row[0],
                category_id=row[1],
                text=row[2],
                icon_path=row[3]
            )
            items.append(item)

        return items

    @staticmethod
    def delete_multiple(item_ids):
        if not item_ids:
            return  # nothing to delete

        conn = get_connection()
        cursor = conn.cursor()
        placeholders = ",".join("?" for _ in item_ids)
        cursor.execute(f"""
            DELETE FROM communication_item
            WHERE item_id IN ({placeholders})
        """, item_ids)
        conn.commit()
        conn.close()

    @staticmethod
    def update(item_id: int, text: str, icon_path: str = None) -> CommunicationItem | None:
        """
        Update communication item. If icon_path is None, keep the existing value.
        """
        text = translate_to_english_sync(text)
        conn = get_connection()
        cursor = conn.cursor()

        if icon_path is None:
            cursor.execute("""
                UPDATE communication_item
                SET text = ?
                WHERE item_id = ?
            """, (
                text,
                item_id
            ))
        else:
            cursor.execute("""
                UPDATE communication_item
                SET text = ?, icon_path = ?
                WHERE item_id = ?
            """, (
                text,
                icon_path,
                item_id
            ))

        conn.commit()

        # fetch the updated row
        cursor.execute("""
            SELECT * FROM communication_item
            WHERE item_id = ?
        """, (item_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return CommunicationItem(
                item_id=row[0],
                category_id=row[1],
                text=row[2],
                icon_path=row[3]
            )
        return None

    @staticmethod
    def get_by_id(item_id: int) -> CommunicationItem | None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT item_id, category_id, text, icon_path
            FROM communication_item
            WHERE item_id = ?
        """, (item_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return CommunicationItem(
                item_id=row[0],
                category_id=row[1],
                text=row[2],
                icon_path=row[3]
            )
        return None
