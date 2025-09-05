from flask import Blueprint, render_template, session

from app.decorators import login_required
from app.main.services import get_communication_item, get_category_data
from app.models.card_items import CardItem

main_bp = Blueprint("main", __name__, url_prefix="/main")

@main_bp.route("/home")
@login_required
def home():# Reset toolbar on entering Home
    session["toolbar_expanded"] = False
    categories = get_category_data()
    cardData: CardItem = [CardItem(id=item.category_id, type="category", text=item.name, image_source=item.icon_path, is_standalone=item.is_standalone) for item in categories]
    return render_template("main/home.html",
                           cardData=cardData,
                           toolbar_expanded=session["toolbar_expanded"])

@main_bp.route("/communication-items/<int:category_id>")
@login_required
def communication_items(category_id):# Reset toolbar on entering Home
    session["toolbar_expanded"] = False
    items = get_communication_item(category_id)
    cardData: CardItem = [CardItem(id=item.item_id, type="communication_item", text=item.text, image_source=item.icon_path, is_standalone=True) for item in items]

    return render_template("main/communication_items.html",
                           cardData=cardData,
                           toolbar_expanded=session["toolbar_expanded"])
