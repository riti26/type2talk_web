class CommunicationItem:
    def __init__(self, item_id: int, category_id: int, text: str, user_id: int = None, icon_path: str = None):
        """
        Represents an individual communication item (e.g., 'Yes', 'No', 'Cheese').

        :param item_id: Unique identifier for the item
        :param category_id: ID of the category this item belongs to
        :param text: Text text for the item
        :param icon_path: Optional path to an icon image file
        """
        self.item_id = item_id
        self.category_id = category_id
        self.text = text
        self.user_id = user_id
        self.icon_path = icon_path

    def __repr__(self):
        return f"<CommunicationItem id={self.item_id}, text='{self.text}', category_id={self.category_id}>"

    def to_dict(self):
        """Converts the item object to a dictionary (useful for JSON storage)."""
        return {
            "id": self.item_id,
            "category_id": self.category_id,
            "text": self.text,
            "user_id": self.user_id,
            "icon_path": self.icon_path
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates an item object from a dictionary."""
        return cls(
            item_id=data.get("id"),
            category_id=data.get("category_id"),
            text=data.get("text"),
            user_id=data.get("user_id"),
            icon_path=data.get("icon_path")
        )