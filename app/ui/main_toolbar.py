from flask import render_template
from app.ui.common_service import get_menus

class MainToolbar:
    def __init__(self):
        self.root_menus = get_menus()
        self.menu_structure = []
        for root in self.root_menus:
            # Assuming get_menus returns root with .text and .children
            self.menu_structure.append({"root": root, "children": getattr(root, "children", [])})

    def render(self):
        # **Pass the correct name to template**
        return render_template(
            "components/main_toolbar.html",
            menu_structure=self.menu_structure
        )
