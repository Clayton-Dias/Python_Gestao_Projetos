from functions.db_usuario import get_load_user


def mod_load_user(mysql, user_id):
    return get_load_user(mysql, user_id)