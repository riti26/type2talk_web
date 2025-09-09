from flask import Blueprint, request, jsonify, send_file

from app.utils.tts.gtts_service import play_text

custom_card_bp = Blueprint("custom_card", __name__)

@custom_card_bp.route("/card_click", methods=["POST"])
def card_click():
    data = request.get_json()
    text = data.get("text")

    mp3_fp = play_text(text)

    # Return audio as response
    return send_file(
        mp3_fp,
        mimetype="audio/mpeg",
        as_attachment=False
    )
