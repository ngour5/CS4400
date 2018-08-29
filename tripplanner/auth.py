import util


def is_logged_in(session):
    return 'user_id' in session


def is_admin(session):
    return is_logged_in(session) and session['is_admin'] == 1


def get_user(email, pw):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_email = "SELECT user_id, email, name, suspended, is_admin FROM user WHERE email=%s and password=%s"
            cursor.execute(get_email, (email, pw))
            result = cursor.fetchone()
    finally:
        connection.close()

    return result

