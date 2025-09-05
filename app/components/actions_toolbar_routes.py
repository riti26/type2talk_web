from flask import Blueprint, jsonify, redirect, render_template, session, url_for, request, flash

actions_toolbar_bp = Blueprint("actions_toolbar", __name__, url_prefix="/actions_toolbar")

@actions_toolbar_bp.route("/toggle_toolbar", methods=["POST"])
def toggle_toolbar():
    session["toolbar_expanded"] = not session.get("toolbar_expanded", False)
    return jsonify({"expanded": session["toolbar_expanded"]})

def render_actions_toolbar():
    # Access Flask session
    expanded = session.get("toolbar_expanded", False)
    return render_template("components/actions_toolbar.html", expanded=expanded)


@actions_toolbar_bp.route("/select_all", methods=["POST"])
def select_all():
    # handle selection logic
    flash("All items selected")
    return redirect(request.referrer)

@actions_toolbar_bp.route("/delete_selected", methods=["POST"])
def delete_selected():
    selected_ids = request.form.getlist("selected_items")
    # call your DAO to delete
    flash(f"Deleted items: {selected_ids}")
    return redirect(request.referrer)

@actions_toolbar_bp.route("/edit_selected", methods=["POST"])
def edit_selected():
    selected_ids = request.form.getlist("selected_items")
    # redirect to edit page or show a form
    return redirect(url_for("main.edit_item", item_id=selected_ids[0]))

@actions_toolbar_bp.route("/add_item", methods=["POST"])
def add_item():
    # redirect to add item page or show modal
    return redirect(url_for("main.add_item"))
