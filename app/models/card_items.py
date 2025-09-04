class CardItem:
    def __init__(self, text: str, image_source: str):
        self.text = text
        self.image_source = image_source

    def __repr__(self):
        return f"CardItem(text={self.text}, image_source={self.image_source})"
