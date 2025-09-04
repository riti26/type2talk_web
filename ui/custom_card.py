# custom_card.py
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable


@dataclass
class CustomCard:
    """
    A reusable server-side card object with actions.

    Attributes:
    - id: Unique identifier
    - text: Card text
    - image_source: Card image URL
    - is_standalone: Boolean for card type
    - selected: Boolean if currently selected
    - bg_color: Background color
    - origin_screen: Optional origin reference
    - toolbar: Optional dict acting as toolbar selection state
    - on_card_pressed: Optional callback function when card is pressed
    """
    id: str
    text: str
    image_source: str
    is_standalone: bool = True
    selected: bool = False
    bg_color: str = "#fff8c6"
    origin_screen: Optional[str] = None

    toolbar: Optional[Dict[str, dict]] = field(default_factory=dict)
    on_card_pressed: Optional[Callable[['CustomCard'], None]] = None

    def press(self):
        """
        Handle a card press:
        - If toolbar is expanded, toggle selection
        - Otherwise, call the on_card_pressed callback
        """
        if self.toolbar.get("expanded", False):
            self.toggle_selection()
        else:
            if self.on_card_pressed:
                self.on_card_pressed(self)

    def toggle_selection(self):
        """Toggle the selection state and update toolbar's selected_cards."""
        self.selected = not self.selected

        if self.toolbar is None:
            return

        if "selected_cards" not in self.toolbar:
            self.toolbar["selected_cards"] = {}

        if self.selected:
            self.toolbar["selected_cards"][self.id] = self.to_dict()
        else:
            self.toolbar["selected_cards"].pop(self.id, None)

    def set_toolbar(self, toolbar: Dict):
        """Assign a toolbar dict to the card and initialize state."""
        self.toolbar = toolbar
        if "selected_cards" not in self.toolbar:
            self.toolbar["selected_cards"] = {}
        self._update_selection_icon()

    def _update_selection_icon(self):
        """Placeholder for updating the icon (can be used in templates)."""
        self.toolbar["icon_visible"] = self.toolbar.get("expanded", False)

    def to_dict(self):
        """Return a dictionary representation for Jinja templates."""
        return {
            "id": self.id,
            "text": self.text,
            "image_source": self.image_source,
            "is_standalone": self.is_standalone,
            "selected": self.selected,
            "bg_color": self.bg_color,
            "origin_screen": self.origin_screen,
        }

    def select(self):
        """Explicitly select the card."""
        if not self.selected:
            self.toggle_selection()

    def deselect(self):
        """Explicitly deselect the card."""
        if self.selected:
            self.toggle_selection()
