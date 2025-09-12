import os
from flask import Blueprint, jsonify, redirect, render_template, render_template_string, session, url_for, request, flash
from werkzeug.utils import secure_filename
from app.models.card_items import CardItem
from db.category_dao import CategoryDAO
from db.item_dao import ItemDAO
from app.decorators import login_required
from app.main.services import get_user_id

actions_toolbar_bp = Blueprint("actions_toolbar", __name__, url_prefix="/actions_toolbar")

@actions_toolbar_bp.route("/toggle_toolbar", methods=["POST"])
def toggle_toolbar():
    session["toolbar_expanded"] = not session.get("toolbar_expanded", False)
    return jsonify({"expanded": session["toolbar_expanded"]})

# ---------------- Render toolbar ----------------
def render_actions_toolbar():
    expanded = session.get("toolbar_expanded", False)
    return render_template("components/actions_toolbar.html", expanded=expanded)

# ---------------- Reset toolbar ----------------
@actions_toolbar_bp.route("/reset_toolbar", methods=["POST"])
def reset_toolbar():
    # Read state from POST form
    state = request.form.get("state", "false").lower() == "true"
    session["toolbar_expanded"] = state
    return jsonify(success=True, toolbar_expanded=state)

# ---------------- Select all ----------------
@actions_toolbar_bp.route("/select_all", methods=["POST"])
def select_all():
    flash("All items selected")
    return redirect(request.referrer)

# ---------------- Delete selected ----------------
@actions_toolbar_bp.route("/delete_selected", methods=["POST"])
def delete_selected():
    """AJAX deletion of selected categories"""
    try:
        data = request.get_json()   # <<< CHANGED: accept JSON body
        selected_ids = data.get("selected_items", None)
        cardType = data.get("cardType", None)
        if selected_ids:
            if cardType == "category":
                CategoryDAO.delete_multiple(selected_ids)
            elif cardType == "communication_items":
                ItemDAO.delete_multiple(selected_ids)
        return jsonify({"success": True, "deleted": selected_ids})  # <<< CHANGED: return JSON instead of redirect
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ---------------- Edit selected ----------------
@actions_toolbar_bp.route("/edit_selected", methods=["POST"])
def edit_selected():
    cardData: CardItem = None
    item_id = request.form.get("selected_item")
    name = request.form.get("name")
    item_type = request.form.get("type", None)  
    description = request.form.get("description")
    icon_file = request.files.get("icon")

    if not item_id:
        return jsonify({"success": False, "error": "No item selected"})
    
    if not item_type:
        return jsonify({"success": False, "error": "Item type not specified"})
    
    icon_path = None  # initialize

    if item_type == "category":
        category = CategoryDAO.get_by_id(item_id)
        if not category:
            return jsonify({"success": False, "error": "Category not found"})
        icon_path = category.icon_path  # default to existing icon path

        # ---------------- Handle file upload ----------------
        if icon_file and icon_file.filename != "":
            filename = secure_filename(icon_file.filename)
            save_folder = os.path.join("app", "static", "images")
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, filename)
            icon_file.save(save_path)
            icon_path = f"images/{filename}"

        updatedCategory = CategoryDAO.update(
            category_id=category.category_id,
            name=name or category.name,
            description=description or category.description,
            is_standalone=category.is_standalone,
            icon_path=icon_path,
        )
        if not updatedCategory:
            return jsonify({"success": False, "error": "Failed to update category"})
        else:
            cardData = CardItem(
                id=category.category_id,
                type="category",
                text=name,
                image_source=updatedCategory.icon_path,
                is_standalone=updatedCategory.is_standalone,
            )

    elif item_type == "communication_items":
        item = ItemDAO.get_by_id(item_id)
        if not item:
            return jsonify({"success": False, "error": "Item not found"})
        icon_path = item.icon_path  # default to existing icon path

        # ---------------- Handle file upload ----------------
        if icon_file and icon_file.filename != "":
            filename = secure_filename(icon_file.filename)
            save_folder = os.path.join("app", "static", "images")
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, filename)
            icon_file.save(save_path)
            icon_path = f"images/{filename}"

        updatedCommunicationItem = ItemDAO.update(
            item_id=item.item_id,
            text=name or item.text,
            icon_path=icon_path,
            audio_path=description or item.audio_path
        )
        if not updatedCommunicationItem:
            return jsonify({"success": False, "error": "Failed to update item"})
        else:
            cardData = CardItem(
                id=updatedCommunicationItem.item_id,
                type="communication_items",
                text=name,
                image_source=updatedCommunicationItem.icon_path,
                is_standalone=True,
            )

    macro_template = "{% import 'components/custom_card.html' as custom_card %}{{ custom_card.render_card(item) }}"
    html = render_template_string(macro_template, item=cardData)

    return jsonify({
        "success": True,
        "html": html
    })

# ---------------- Add new category ----------------
@actions_toolbar_bp.route("/add_item", methods=["POST"])
@login_required
def add_item():
    name = request.form.get("name")
    description = request.form.get("description")
    is_standalone = request.form.get("is_standalone") == "1"

    # ---------------- Handle file upload ----------------
    icon_file = request.files.get("icon")
    icon_path = None
    if icon_file and icon_file.filename != "":
        filename = secure_filename(icon_file.filename)
        save_folder = os.path.join("app", "static", "images")
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, filename)
        icon_file.save(save_path)
        icon_path = f"images/{filename}"

    if not name:
        return jsonify({"success": False, "error": "Category name required"})

    try:
        # ---------------- Create category ----------------
        category = CategoryDAO.add(
            name=name,
            user_id=get_user_id(),
            icon_path=icon_path,
            description=description,
            is_standalone=is_standalone
        )
        if not category:
            raise Exception("Failed to save category")
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

    # Import the macro from custom_card.html
    cardData: CardItem = CardItem(
        id=category.category_id,
        type="category",
        text=name,
        image_source=category.icon_path,
        is_standalone=category.is_standalone,
    )
    macro_template = "{% import 'components/custom_card.html' as custom_card %}{{ custom_card.render_card(item) }}"
    html = render_template_string(macro_template, item=cardData)

    return jsonify({
        "success": True,
        "html": html
    })

@actions_toolbar_bp.route("/add_communication_item", methods=["POST"])
def add_communication_item():
    category_id = request.form.get("category_id")
    if not category_id:
        return jsonify({"success": False, "error": "Missing category ID"})

    name = request.form.get("name")
    icon_file = request.files.get("icon")

    # Save icon file
    icon_path = None
    if icon_file and icon_file.filename != "":
        filename = secure_filename(icon_file.filename)
        save_folder = os.path.join("app", "static", "images")
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, filename)
        icon_file.save(save_path)
        icon_path = f"images/{filename}"

    # Add item to DB
    item = ItemDAO.add(
        category_id=int(category_id),
        text=name,
        icon_path=icon_path
    )

    # Render HTML card
    cardData = CardItem(
        id=item.item_id,
        type="item",
        text=name,
        image_source=item.icon_path,
        is_standalone=True
    )
    macro_template = "{% import 'components/custom_card.html' as custom_card %}{{ custom_card.render_card(item) }}"
    html = render_template_string(macro_template, item=cardData)

    return jsonify({"success": True, "html": html})


