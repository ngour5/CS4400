from flask import Flask, render_template, request, session, url_for, redirect, flash, abort
from werkzeug.exceptions import HTTPException
import auth
import trip
import user
import os
import attraction
import datetime as dt


from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


STRINGS = {
    'SIGNED_OUT': 'You must login to access this page',
    'NOT_AUTHORIZED': 'You don\'t have permission to access this page',
    'SIGN_OUT_SUCCESS': 'You are now logged out',
}


def redirect_to_login(msg=None, msg_category=None):
    if msg is not None:
        flash(msg, category=msg_category)  # Flash defines a message that will be displayed in an alert bubble on
        #  the next page the user visits (in this case, the login page).  The display of the message is in
        #  templates/include/page.html but can be overridden on a page by page basis.
    return redirect(url_for('login'))


def redirect_to_home(msg=None, msg_category=None):
    if msg is not None:
        flash(msg, category=msg_category)
    return redirect(url_for('home'))


@app.route('/')
def home():
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    return render_template("home.html", session=session, trips=trip.get_user_trips(session['user_id']))


# Trips
@app.route('/trips/create', methods=["GET", "POST"])
def create_trip():
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])

    # changes to trip page will go here

    city_ids = trip.get_city_ids()

    cc_ids = user.get_user_cc_ids(session['user_id'])

    # This step obfuscates the credit number sent to the UI except for the last 4 digits
    for cc in cc_ids:
        cc['cc_number'] = 'X'*3 + cc['cc_number'][-4:]

    if request.method == "POST":
        city = request.form["city"]
        start_date = request.form["start_date"]
        cc_id = request.form["credit_card"]
        user_id = session['user_id']
        # Things to check:
        # 1. No field is blank
        # 2. The credit card belongs to the user
        # 3. Date is in the future
        trip.create_trip(city, start_date, cc_id, user_id)
        return redirect_to_home("Trip created successfully", "success")

    return render_template("trips/create_trip.html", session=session, cc_ids=cc_ids, city_ids=city_ids)


@app.route('/trips/<trip_id>/edit', methods=['POST', 'GET'])
def edit_trip(trip_id):

    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    if not trip.belongs_to(trip_id, session['user_id']):
        return redirect_to_home(STRINGS['NOT_AUTHORIZED'])

    city_name = trip.get_city(trip_id)['city']
    app.logger.debug("city_name: %s" % city_name)
    attraction_id = trip.get_attraction_id(city_name)
    now = dt.datetime.now().date() # Thanks https://stackoverflow.com/a/3279015/5434744
    trip_ref = trip.get_trip(trip_id)
    trip_start = trip_ref['start_date']
    trip_in_past = now > trip_start


    return render_template("trips/edit_trip.html", session=session, trip=trip_ref,
                           attractions=attraction_id,
                           trip_in_past=trip_in_past,
                           activities=trip.get_activities(trip_id))


@app.route('/attractions/<attraction_id>/report')
def attraction_report(attraction_id):
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    if not auth.is_admin(session):
        return redirect_to_home(STRINGS['NOT_AUTHORIZED'])

    show_date = request.args.get('date', str(dt.datetime.now())[:10])
    try:
        time_slots = attraction.get_time_slots(attraction_id)

        show_time_slot = int(request.args.get('ts', time_slots[0]['time_slot_id']))

        app.logger.debug(time_slots[0]['time_slot_id'])
        return render_template("attractions/attraction_report.html", session=session,
                               attraction=attraction.get_attraction(attraction_id),
                               requires_reservation=attraction.requires_reservation(attraction_id),
                               reservations=attraction.get_bookings(attraction_id, show_date, show_time_slot),
                               date=show_date,
                               time_slots=time_slots,
                               selected_ts=attraction.get_time_slot(show_time_slot))
    except IndexError:
        return render_template("attractions/attraction_report.html", session=session,
                               attraction=attraction.get_attraction(attraction_id),
                               requires_reservation=attraction.requires_reservation(attraction_id))


# Basic user pages (login, logout, profile, admin
@app.route('/admin')
def admin():
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    if not auth.is_admin(session):
        return redirect_to_home(STRINGS['NOT_AUTHORIZED'])
    return render_template("admin.html", session=session, users=user.get_all_users(), attractions=attraction.get_all(),
                           res_info=attraction.requires_reservation_all())
    return render_template("admin.html", session=session, users=user.get_all_users(), attractions=attraction.get_all())

@app.route('/user/<user_id>/delete')
def delete_user(user_id):
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    if not auth.is_admin(session):
        return redirect_to_home(STRINGS['NOT_AUTHORIZED'])
    if int(user_id) == session['user_id']:
        flash("You can't delete your own account")
    else:
        user.delete_user(user_id)
        flash("User deleted successfully", category="success")

    return redirect(url_for('admin'))



@app.route('/attraction/<attraction_id>/delete')
def delete_attraction(attraction_id):
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    if not auth.is_admin(session):
        return redirect_to_home(STRINGS['NOT_AUTHORIZED'])

    attraction.delete_attraction(attraction_id)
    flash("Attraction deleted successfully", category='success')
    return redirect(url_for('admin'))




@app.route('/users/<user_id>', methods=['POST', 'GET'])
def profile(user_id):
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    if int(user_id) == session['user_id'] or auth.is_admin(session):
        if request.method == 'POST':
            if auth.is_admin(session):
                email = request.form['email']
                name = request.form['user-name']
                suspended = request.form.get('suspended')
                is_admin = request.form.get('role')
                if suspended is None:
                    suspended = 0
                if is_admin == 'admin':
                    is_admin = 1
                else:
                    is_admin = 0
                user.edit_user_admin(user_id, email, name, suspended, is_admin)
            else:
                email = request.form['email']
                name = request.form['user-name']
                app.logger.debug(user_id, email, name)
                user.edit_user(user_id, email, name)

            flash("Changes saved successfully", category="success")
            return redirect(url_for('profile', user_id=user_id))
        else:
            return render_template("profile.html", session=session, user=user.get_user_by_id(user_id))
    else:
        return redirect_to_home(STRINGS['NOT_AUTHORIZED'])


@app.route('/login', methods=['POST', 'GET'])
def login():
    if auth.is_logged_in(session):
        return redirect_to_home()

    if request.method == 'POST':
        user = auth.get_user(request.form['username'], request.form['password'])
        app.logger.debug(user)
        if user is not None:
            if user['suspended'] == 1:
                flash("Your account is suspended")
            else:
                session['user_id'] = user['user_id']
                # Technically we shouldn't store this information in session variables because changes made in the DB
                # won't reflect on the frontend until they sign out and sign back in (that clears the session variables)
                session['email'] = user['email']
                session['is_admin'] = user['is_admin']
                session['name'] = user['name']
                flash("Successfully logged in", category="success")
                return redirect_to_home()
        else:
            flash("Invalid email or password")

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if auth.is_logged_in(session):
        session.clear()
        return redirect(url_for('register'))
    if request.method == 'POST':
        # Access request fields using request.form['name attribute from HTML input element']
        # Check to make sure each field contains valid info
        # If one or more fields are not valid, call flash("message about invalid field")
        #    and don't save the data
        # If you're feeling nice, return to the page with the data still filled in
        email = request.form['email']
        email_confirm = request.form['email_confirm']
        if email != email_confirm:
            flash("Entered emails do not match")
            return render_template('auth/register.html', session=session)
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            flash("Entered passwords do not match")
            return render_template('auth/register.html', session=session)
        name = request.form['full_name']
        snum = request.form['address_snum']
        street = request.form['address_street']
        city = request.form['address_city']
        state = request.form['address_state']
        zip = request.form['address_zip']
        country = request.form['address_country']
        cc_number = request.form['cc_number']
        cc_cvv = request.form['cc_cvv']
        cc_exp_month = request.form['cc_expiry_month']
        cc_exp_year = request.form['cc_expiry_year']
        user.create_new_user(email, password, name, snum, street, city, state, zip, country, cc_number, cc_number, cc_cvv, cc_exp_month, cc_exp_year)
        return redirect_to_login("Welcome to the Matrix", "success")

    return render_template('auth/register.html', session=session)


@app.route('/logout')
def logout():
    session.clear()
    return redirect_to_login(STRINGS['SIGN_OUT_SUCCESS'], 'success')


# attractions
@app.route('/attractions/create', methods=['GET', 'POST'])
def create_attraction():
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    if not auth.is_admin(session):
        return redirect_to_home(STRINGS['NOT_AUTHORIZED'])

    if request.method == 'POST':
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        if request.form["street_num"] == "":
            street_num = None
        else:
            street_num = request.form["street_num"]
        street = request.form["street"]
        city = request.form["city"]
        if request.form["state"] == "":
            state = None
        else:
            state = request.form["state"]
        zip = request.form["zip"]
        country = request.form["country"]
        if request.form["transit"] == "":
            transit = None
        else:
            transit = request.form["transit"]

        attraction.create_attraction(name, description, price, street_num, street, city, state, zip, country, transit)

        flash("Attraction created successfully", category="success")
        return redirect(url_for('admin'))

    return render_template("attractions/attraction.html", session=session)


@app.route('/attractions/<attraction_id>/edit', methods=['POST', 'GET'])
def edit_attraction(attraction_id):
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    if not auth.is_admin(session):
        return redirect_to_home(STRINGS['NOT_AUTHORIZED'])

    if request.method == 'POST':
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        if request.form["street_num"] == "":
            street_num = None
        else:
            street_num = request.form["street_num"]
        street = request.form["street"]
        city = request.form["city"]
        if request.form["state"] == "":
            state = None
        else:
            state = request.form["state"]
        zip = request.form["zip"]
        country = request.form["country"]

        if request.form["transit"] == "":
            transit = None
        else:
            transit = request.form["transit"]

        attraction.edit_attraction(attraction_id, name, description, price, street_num, street, city, state, zip,
                                   country, transit)

        flash("Attraction edited successfully", category="success")
        return redirect(url_for('admin'))

    return render_template("attractions/attraction.html", session=session,
                           attraction=attraction.get_attraction(attraction_id))

#review attraction
@app.route('/attractions/<attraction_id>/review', methods=['GET','POST'])
def review_attraction(attraction_id):
    if not auth.is_logged_in(session):
        return redirect_to_login(STRINGS['SIGNED_OUT'])
    if request.method == 'POST':
        review = request.form['review']
        title = request.form['title']
        review_created = dt.datetime.now()
        user_id = session['user_id']
        attraction_id = attraction_id

        attraction.create_review(title, review, review_created, user_id, attraction_id)

        flash("Review created successfully", category="success")
        return redirect(url_for('home'))
    return render_template("attractions/review.html", session=session,
                           attr=attraction.get_attraction(attraction_id))

@app.route('/activity/<trip_id>/<attraction_id>', methods=['POST'])
def create_activity(trip_id, attraction_id):
    start_dt = request.form['start_dt']
    end_dt = request.form['end_dt']
    attraction.add_activity(trip_id, attraction_id, start_dt, end_dt)
    return redirect(url_for('edit_trip', trip_id=trip_id))


@app.route('/attractions/<attr_id>/all_reviews')
def attraction_reviews(attr_id):
    return render_template("attractions/attr_reviews.html", attr=attraction.get_attraction(attr_id),
                           reviews=attraction.get_reviews(attr_id))

# Most of this function is from https://stackoverflow.com/a/29332131/5434744
@app.errorhandler(Exception)
def error_handler(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code

    if ":" in str(e):
        return render_template("errors/generic_error.html", error=str(e)[:str(e).index(":")],
                           desc=str(e)[str(e).index(":") + 2:], code=code)
    else:
        return render_template("errors/generic_error.html", error="500 Internal Server Error",
                               desc="We can't process your request right now.", code=500)
