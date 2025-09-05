class CardItem:
    def __init__(self, id:int, type: str, text: str, image_source: str, is_standalone: bool):
        self.id = id
        self.type = type
        self.text = text
        self.image_source = image_source
        self.is_standalone = is_standalone

    def __repr__(self):
        return f"CardItem(id={self.id}, type={self.type}, text={self.text}, image_source={self.image_source}, is_standalone={self.is_standalone})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "text": self.text,
            "image_source": self.image_source,
            "is_standalone": self.is_standalone
        }
