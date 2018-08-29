import util
from datetime import datetime


def get_user_cc_ids(user_id):
    connection = util.db_connection()
    try:
        with connection.cursor() as cursor:
            get_cc_ids = "select credit_card_id, cc_number, expiry from user join credit_card on user.user_id = credit_card.user_id where user.user_id = %s"
            cursor.execute(get_cc_ids, user_id)
            result = cursor.fetchall()
    finally:
        connection.close()
    return result


def get_user_by_id(user_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_email = "SELECT user_id, email, name, suspended, is_admin FROM user WHERE user_id=%s"
            cursor.execute(get_email, user_id)
            result = cursor.fetchone()
    finally:
        connection.close()

    return result


def get_all_users():
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_email = "SELECT user_id, email, name, suspended, is_admin FROM user order by user_id"
            cursor.execute(get_email)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result


def create_new_user(email, password, name, snum, street, city, state, zip, country, cc_name, cc_number, cc_cvv, cc_exp_month, cc_exp_year):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            new_user = "INSERT INTO user values (null, %s, %s, %s, %s, %s)"
            new_address = "INSERT INTO address values (null , %s, %s, %s, %s, %s, %s)"
            new_cc = "INSERT INTO credit_card values (null, %s, " \
                     "(SELECT address_id from address order by address_id desc limit 1), %s, %s, " \
                     "(SELECT user_id from user order by user_id desc limit 1))"
            days_31 = [1, 3, 5, 7, 8, 10, 12]
            days_30 = [4, 6, 9, 11]
            days_in_month = ''
            if cc_exp_month in days_31:
                days_in_month = '31'
            elif cc_exp_month in days_30:
                days_in_month = '30'
            else:
                days_in_month = '28'
            exp = '' + days_in_month + cc_exp_month + cc_exp_year
            exp_date = datetime.strptime(exp, "%d%m%Y").date()
            cursor.execute(new_user, (email, password, name, "0", "0"))
            if snum == '':
                snum = None
            if state == '':
                state = None
            cursor.execute(new_address, (snum, street, city, state, zip, country))
            cursor.execute(new_cc, (cc_number, exp_date, cc_cvv))
            connection.commit()
    finally:
        connection.close()

    return True


def edit_user_admin(user_id, email, name, suspended, is_admin):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            update_user = """
            UPDATE user
            SET email=%s, name=%s, suspended=%s, is_admin=%s 
            WHERE user_id=%s
            """
            user_data = (email, name, suspended, is_admin, user_id)
            cursor.execute(update_user, user_data)
            connection.commit()
    finally:
        connection.close()

    # return True


def edit_user(user_id, email, name):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            update_user = """
            UPDATE user
            SET email=%s, name=%s
            WHERE user_id=%s
            """
            user_data = (email, name, user_id)
            cursor.execute(update_user, user_data)
            connection.commit()
    finally:
        connection.close()

    return True

def delete_user(user_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            del_user = "DELETE FROM user WHERE user_id = %s"
            cursor.execute(del_user, user_id)
            connection.commit()
    finally:
        connection.close()
