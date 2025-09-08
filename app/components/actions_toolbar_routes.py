import os
from flask import Blueprint, jsonify, redirect, render_template, render_template_string, session, url_for, request, flash
from werkzeug.utils import secure_filename
from app.models.card_items import CardItem
from db.category_dao import CategoryDAO

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
        selected_ids = data.get("selected_items", [])
        for cat_id in selected_ids:
            CategoryDAO.delete(int(cat_id))   # delete from DB
        return jsonify({"success": True, "deleted": selected_ids})  # <<< CHANGED: return JSON instead of redirect
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ---------------- Edit selected ----------------
# ---------------- Edit selected ----------------
@actions_toolbar_bp.route("/edit_selected", methods=["POST"])
def edit_selected():
    # Support both JSON (AJAX) and form-data
    if request.is_json:
        data = request.get_json()
        selected_ids = data.get("selected_items", [])
        name = data.get("name")
        description = data.get("description")
        icon_file = None
    else:
        selected_ids = request.form.getlist("selected_items")
        name = request.form.get("name")
        description = request.form.get("description")
        icon_file = request.files.get("icon")

    if not selected_ids:
        return jsonify({"success": False, "error": "No item selected"})

    category_id = int(selected_ids[0])  # edit only the first one

    # ---------------- Fetch existing category ----------------
    category = CategoryDAO.get_by_id(category_id)
    if not category:
        return jsonify({"success": False, "error": "Category not found"})

    # ---------------- Handle inputs ----------------
    # Keep old values if input not provided
    name = name or category.name
    description = description or category.description

    # Only update is_standalone if explicitly sent in form/JSON
    if request.is_json:
        is_standalone = category.is_standalone  # JSON edit doesn't touch it
    else:
        if "is_standalone" in request.form:
            is_standalone = request.form.get("is_standalone") == "1"
        else:
            is_standalone = category.is_standalone  # keep old value

    # ---------------- Handle file upload ----------------
    icon_path = category.icon_path
    if icon_file and icon_file.filename != "":
        filename = secure_filename(icon_file.filename)
        save_folder = os.path.join("app", "static", "images")
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, filename)
        icon_file.save(save_path)
        icon_path = f"images/{filename}"

    # ---------------- Update category ----------------
    category = CategoryDAO.update(
        category_id=category_id,
        name=name,
        description=description,
        is_standalone=is_standalone,
        icon_path=icon_path,
    )

    if not category:
        return jsonify({"success": False, "error": "Failed to update category"})

    # ---------------- Re-render card ----------------
    cardData: CardItem = CardItem(
        id=category.category_id,
        type="category",
        text=category.name,
        image_source=category.icon_path,
        is_standalone=category.is_standalone,
    )
    macro_template = "{% import 'components/custom_card.html' as custom_card %}{{ custom_card.render_card(item) }}"
    html = render_template_string(macro_template, item=cardData)

    return jsonify({
        "success": True,
        "html": html
    })

# ---------------- Add new category ----------------
@actions_toolbar_bp.route("/add_item", methods=["POST"])
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

    # ---------------- Create category ----------------
    try:
        category = CategoryDAO.add(
            name=name,
            user_id=session.get("user_id"),
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
        text=category.name,
        image_source=category.icon_path,
        is_standalone=category.is_standalone,
    )
    macro_template = "{% import 'components/custom_card.html' as custom_card %}{{ custom_card.render_card(item) }}"
    html = render_template_string(macro_template, item=cardData)

    return jsonify({
        "success": True,
        "html": html
    })
