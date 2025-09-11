from flask import render_template
from app.ui.common_service import get_menus

class MainToolbar:
    def __init__(self):
        self.root_menus = get_menus()
        # Convert every Menu object to a dict immediately
        self.menu_structure = [m.to_dict() for m in self.root_menus]

    def render(self):
        return render_template(
            "components/main_toolbar.html",
            menu_structure=self.menu_structure
        )
