from db.menu_dao import MenuDAO


def get_menus():
    db_menus = MenuDAO.get_root_menus()
    return db_menus
