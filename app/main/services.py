from flask import session
from app.utils.add_data_manager import AppDataManager
from db.category_dao import CategoryDAO
from db.item_dao import ItemDAO
from db.user_session_dao import UserSessionDAO


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
    return session.get('selected_category') or "Type2Talk"