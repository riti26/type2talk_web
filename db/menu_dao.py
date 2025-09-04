from db.connection import get_connection
from models.menu import Menu

class MenuDAO:
    @staticmethod
    def get_all():
        """Fetch all menus (flat list)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, text, icon, viewclass, parent_id FROM menu ORDER BY id"
        )
        rows = cursor.fetchall()
        conn.close()
        return [Menu(*row) for row in rows]
    
    @staticmethod
    def get_root_menus():
        """Return all menus that do not have a parent (top-level)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, text, icon, viewclass, parent_id
            FROM menu
            WHERE parent_id IS NULL
            ORDER BY id
        """)
        rows = cursor.fetchall()
        conn.close()
        return [Menu(*row) for row in rows]

    @staticmethod
    def get_children(parent_id):
        """Fetch all submenus under a parent menu."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, text, icon, viewclass, parent_id FROM menu WHERE parent_id = ? ORDER BY id",
            (parent_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [Menu(*row) for row in rows]