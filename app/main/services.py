from app.utils.add_data_manager import AppDataManager
from db.category_dao import CategoryDAO
from db.item_dao import ItemDAO
from db.user_session_dao import UserSessionDAO


def get_category_data():
    token = AppDataManager.load_session()
    user_info = UserSessionDAO.get_user_info(token)
    user_id = user_info["user_id"] if user_info else None

    categories = CategoryDAO.get_all(user_id=user_id)

    return {"categories": categories}

def get_communication_item(category_id):
    items = ItemDAO.get_by_category(category_id)
    return items
