class Menu:
    def __init__(self, id, name, text, icon, parent_id=None):
        self.id = id
        self.name = name          # internal identifier (e.g., "settings")
        self.text = text          # display text (e.g., "Settings")
        self.icon = icon          # icon name (e.g., "cog")
        self.parent_id = parent_id

    def to_dict(self):
        """Convert menu item into dictionary for KivyMD UI usage."""
        return {
            "id": self.id,
            "name": self.name,
            "text": self.text,
            "icon": self.icon,
            "parent_id": self.parent_id
        }
