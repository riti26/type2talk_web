class CommunicationCategory:
    def __init__(self, category_id: int, name: str, user_id: int = None, icon_path: str = None, description: str = None, is_standalone: bool = True):
        """
        Represents a communication category (e.g., Food, Drinks, People).

        :param category_id: Unique identifier for the category
        :param name: Name of the category
        :param icon_path: Optional path to an icon image file
        :param description: Optional description of the category
        """
        self.category_id = category_id
        self.name = name
        self.user_id = user_id
        self.icon_path = icon_path
        self.description = description
        self.is_standalone = is_standalone

    def __repr__(self):
        return f"<CommunicationCategory id={self.category_id}, name='{self.name}'>"

    def to_dict(self):
        """Converts the category object to a dictionary (useful for JSON storage)."""
        return {
            "id": self.category_id,
            "name": self.name,
            "user_id": self.user_id,
            "icon_path": self.icon_path,
            "description": self.description,
            "is_standalone": self.is_standalone
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a category object from a dictionary."""
        return cls(
            category_id=data.get("id"),
            name=data.get("name"),
            user_id=data.get("user_id"),
            icon_path=data.get("icon_path"),
            description=data.get("description"),
            is_standalone=data.get("is_standalone")
        )