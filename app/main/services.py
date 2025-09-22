from flask import session
from app.utils.add_data_manager import AppDataManager
from db.category_dao import CategoryDAO
from db.item_dao import ItemDAO
from db.user_session_dao import UserSessionDAO
from app.utils.translator.deep_translator_service import _translate_sync


def get_category_data():
    categories = CategoryDAO.get_all(get_user_id())
    return categories

def get_communication_items(category_id):
    items = ItemDAO.get_by_category(category_id)
    return items

def get_user_id():
    token = AppDataManager.load_session()
    user_info = UserSessionDAO.get_user_info(token)
    return user_info.user_id if user_info else None

def set_selected_category(id):
    category = CategoryDAO.get_by_id(id)
    if category:
        session['selected_category'] = category.text

def get_selected_category():
    translated_text = session.get('selected_category') or None
    if translated_text:
        translated_text = _translate_sync(  # <-- use sync translation
                session.get('selected_category'),
                AppDataManager.get_language()
            )
    return translated_text or "Type2Talk"

def translate_all_data(language):
    categories = CategoryDAO.get_all(get_user_id())
    for category in categories:
        translated_text = _translate_sync(  # <-- use sync translation
            category.text,
            language
        )
        items = get_communication_items(category.category_id)
        for item in items:
            translated_item_text = _translate_sync(  # <-- use sync translation
                item.text,
                language
            )
    return True