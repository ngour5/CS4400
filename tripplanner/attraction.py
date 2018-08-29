import util

def get_all():
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_attractions = """select *
                                 from attraction
                                   join address on attraction.address_id = address.address_id
                                   order by attraction_id
            """
            cursor.execute(get_attractions)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result


def get_attraction(attraction_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_attractions = """select *
                                 from attraction
                                   join address on attraction.address_id = address.address_id
                                   where attraction_id = %s
                                   order by attraction_id
            """
            cursor.execute(get_attractions, attraction_id)
            result = cursor.fetchone()
    finally:
        connection.close()
    return result


def create_attraction(name, description, price, street_num, street, city, state, zip, country, transit):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            print("clicked!")
            save_address = "INSERT INTO address values (null, %s, %s, %s, %s, %s, %s)"
            cursor.execute(save_address, (street_num, street, city, state, zip, country))
            save_attraction = "INSERT INTO attraction (attraction_id, name, address_id, transit_stop, description, price) values (null, %s, (SELECT address_id FROM address ORDER BY address_id desc limit 1), %s, %s, %s)"
            cursor.execute(save_attraction, (name, transit, description, price))
            connection.commit()
    finally:
        connection.close()

    return True


def edit_attraction(attraction_id, name, description, price, street_num, street, city, state, zip, country, transit):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            address_id = "SELECT attraction.address_id FROM attraction JOIN address using (address_id) WHERE attraction.attraction_id=%s"
            update_address="""
               UPDATE address
               SET street_number=%s, street=%s, city=%s, state=%s, zip=%s, country=%s
               WHERE address_id=%s
            """
            address_data = (street_num, street, city, state, zip, country, address_id)
            cursor.execute(update_address, address_data)

            update_attraction ="""
               UPDATE attraction
               SET name=%s, transit_stop=%s, description=%s, price=%s
               WHERE attraction_id=%s
            """
            attraction_data = (name, transit, description, price, attraction_id)
            cursor.execute(update_attraction, attraction_data)
            connection.commit()
    finally:
        connection.close()

def requires_reservation(attraction_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_time_slots = """select t.attraction_id
                                    from attraction
                                      join time_slot t on attraction.attraction_id = t.attraction_id
                                    where t.attraction_id = %s
                                    group by t.attraction_id"""
            cursor.execute(get_time_slots, attraction_id)
            result = cursor.fetchone()

    finally:
        connection.close()

    return result is not None


def requires_reservation_all():
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_time_slots =     """select attraction.attraction_id, count(t.attraction_id) as 'slots'
                                    from attraction
                                      left join time_slot t on attraction.attraction_id = t.attraction_id
                                    group by attraction.attraction_id"""
            cursor.execute(get_time_slots)
            result = cursor.fetchall()

    finally:
        connection.close()

    # Hands-down best Python feature right here
    return [{ 'attraction_id': r['attraction_id'], 'res_req': r['slots'] > 0 } for r in result]


def get_bookings(attraction_id, date, time_slot_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_attractions = """select attraction.attraction_id, attraction.name, res_num, res_date, t.start_time, t.end_time, u.name
                                 from attraction
                                   join time_slot t on attraction.attraction_id = t.attraction_id
                                   join reservation r on t.time_slot_id = r.time_slot_id
                                   join activity a on r.activity_id = a.activity_id
                                   join trip t2 on a.trip_id = t2.trip_id
                                   join user u on t2.user_id = u.user_id
                                 where res_date = %s and
                                       attraction.attraction_id = %s and
                                       t.time_slot_id = %s
                                 order by start_time
                """
            cursor.execute(get_attractions, (date, attraction_id, time_slot_id))
            result = cursor.fetchall()
    finally:
        connection.close()

    return result

def get_time_slots(attraction_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_attractions = """select time_slot_id, start_time, end_time
                                from attraction
                                  join time_slot t on attraction.attraction_id = t.attraction_id
                                where attraction.attraction_id = %s
                    """
            cursor.execute(get_attractions, attraction_id)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result

def get_time_slot(time_slot_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            get_attractions = """select time_slot_id, start_time, end_time
                                    from time_slot
                                    where time_slot_id = %s
                        """
            cursor.execute(get_attractions, time_slot_id)
            result = cursor.fetchone()
    finally:
        connection.close()

    return result

def delete_attraction(attraction_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            del_attraction = "DELETE FROM attraction WHERE attraction_id = %s"
            cursor.execute(del_attraction, attraction_id)
            connection.commit()
    finally:
        connection.close()

def create_review(title, review, review_created, user_id, attraction_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            add_review = "INSERT INTO review values (%s, %s, %s, %s, %s)"
            cursor.execute(add_review, (title, review, review_created, user_id, attraction_id))
            connection.commit()
    finally:
        connection.close()

    return True

def add_activity(trip_id, attraction_id, start_dt, end_dt):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            create_activity = """insert into activity (start_date_time, end_date_time, attraction_id, trip_id)
                            values (%s, %s, %s, %s)"""
            cursor.execute(create_activity, (start_dt, end_dt, attraction_id, trip_id))
            connection.commit()
    finally:
        connection.close()

    return True

def get_reviews(attr_id):
    connection = util.db_connection()

    try:
        with connection.cursor() as cursor:
            create_activity = "select * from review where attraction_id = %s order by review_created desc"
            cursor.execute(create_activity, attr_id)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result