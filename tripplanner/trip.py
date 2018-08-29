import util


def create_trip(city, start_date, credit_card_id, user_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            save_trip = "INSERT INTO trip (city, start_date, credit_card_id, user_id) values (%s, %s, %s, %s)"
            cursor.execute(save_trip, (city, start_date, credit_card_id, user_id))
            connection.commit()
    finally:
        connection.close()

    return True

def get_user_trips(user_id):
    connection = util.db_connection()
    try:
        with connection.cursor() as cursor:
            get_trips = "select trip_id, city, start_date from trip where user_id = %s order by start_date"
            cursor.execute(get_trips, user_id)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result

def belongs_to(trip_id, user_id):
    connection = util.db_connection()
    try:
        with connection.cursor() as cursor:
            get_trip = "select trip_id from trip where trip_id = %s and user_id = %s"
            cursor.execute(get_trip, (trip_id, user_id))
            result = cursor.fetchone()
    finally:
        connection.close()

    return result is not None

def get_trip(trip_id):
    connection = util.db_connection()
    try:
        with connection.cursor() as cursor:
            get_trip = "select * from trip where trip_id = %s"
            cursor.execute(get_trip, trip_id)
            result = cursor.fetchone()
    finally:
        connection.close()

    return result

def get_city_ids():
    connection = util.db_connection()
    try:
        with connection.cursor() as cursor:
            get_city_ids = "select distinct city from attraction join address using (address_id);"
            cursor.execute(get_city_ids)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result

def get_attraction_id(city_id):
    connection = util.db_connection()
    try:
        with connection.cursor() as cursor:
            get_attraction_id = "select * from attraction join address using (address_id) where city = %s";
            cursor.execute(get_attraction_id, city_id)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result

def get_city(trip_id):
    connection = util.db_connection()
    try:
        with connection.cursor() as cursor:
            get_city = "select city from trip where trip_id = %s";
            cursor.execute(get_city, trip_id)
            result = cursor.fetchone()
    finally:
        connection.close()

    return result

def get_activities(trip_id):
    connection = util.db_connection()
    try:
        with connection.cursor() as cursor:
            get_activities = """
                select start_date_time, end_date_time, a.attraction_id, a.name
                from activity
                  join trip on activity.trip_id = trip.trip_id
                  join attraction a on activity.attraction_id = a.attraction_id
                where trip.trip_id = %s
                order by start_date_time 
            """
            cursor.execute(get_activities, trip_id)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result