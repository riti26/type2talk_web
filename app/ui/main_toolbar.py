from flask import render_template, request
from app.ui.common_service import get_menus
from app.main.services import get_selected_category

class MainToolbar:
    def __init__(self):
        self.root_menus = get_menus()
        # Convert every Menu object to a dict immediately
        self.menu_structure = [m.to_dict() for m in self.root_menus]
        if request and request.endpoint == 'main.communication_items':
            self.selected_category = get_selected_category()
        else:
            self.selected_category = "Type2Talk"

    def render(self):
        return render_template(
            "components/main_toolbar.html",
            menu_structure=self.menu_structure,
            selected_category=self.selected_category
        )
