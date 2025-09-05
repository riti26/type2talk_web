from flask import Blueprint, render_template, request

from app.decorators import login_required
from app.main.services import get_communication_item, get_category_data

main_bp = Blueprint("main", __name__, url_prefix="/main")

@main_bp.route("/home")
@login_required
def home():
    data = get_category_data()
    return render_template("main/home.html", data=data)

@main_bp.route("/communication-items/<int:category_id>")
@login_required
def communication_items(category_id):
    data = get_communication_item(category_id)
    if not data:
            return "Category not found", 404
    return render_template("main/communication_items.html", data=data)
