from flask import Blueprint, redirect, url_for
from ui.phrase_toolbar import PhraseToolbar

toolbar_bp = Blueprint("toolbar", __name__)

@toolbar_bp.route("/toolbar/remove_last", methods=["POST"])
def toolbar_remove_last():
    PhraseToolbar.remove_last()
    return redirect(url_for("home"))

@toolbar_bp.route("/toolbar/clear", methods=["POST"])
def toolbar_clear():
    PhraseToolbar.clear()
    return redirect(url_for("home"))

@toolbar_bp.route("/toolbar/speak", methods=["POST"])
def toolbar_speak():
    PhraseToolbar.speak()
    return redirect(url_for("home"))
