"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import Login, Signup, Profiles
from app.models import Profile, Users, Favourite
from flask_wtf.csrf import generate_csrf

###
# Routing for your application.
###

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/api/register', methods=['POST'])
def register():
    form = Signup()

    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        name = form.name.data
        email = form.email.data
        photo = form.photo.data.filename
        
        new_user = Users(username, password, name, email, photo)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'errors': form.errors}), 400


@app.route('/api/auth/login', methods=['POST'])
def login():
    form = Login()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return jsonify({'message': 'Logged in successfully'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    return jsonify({'errors': form.errors}), 400

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    profiles = Profile.query.all()
    return jsonify([p.serialize() for p in profiles])  # Define serialize method

@app.route('/api/profiles', methods=['POST'])
@login_required
def create_profile():
    form = Profiles()

    if form.validate_on_submit():
        profile = Profile(
            description=form.description.data,
            parish=form.parish.data,
            biography=form.biography.data,
            sex=form.sex.data,
            race=form.race.data,
            birth_year=form.birth_year.data,
            height=form.height.data,
            fav_cuisine=form.fav_cuisine.data,
            fav_color=form.fav_color.data,
            fav_school_subject=form.fav_school_subject.data,
            political=form.political.data,
            religious=form.religious.data,
            family_oriented=form.family_oriented.data,
            user_id_fk=current_user.id
        )
        db.session.add(profile)
        db.session.commit()

        return jsonify({'message': 'Profile created'}), 201
    return jsonify({'errors': form.errors}), 400

@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    return jsonify(profile.serialize())

@app.route('/api/profiles/<int:user_id>/favourite', methods=['POST'])
@login_required
def add_favourite(user_id):
    fav = Favourite(user_id_fk=current_user.id, fav_user_id_fk=user_id)
    db.session.add(fav)
    db.session.commit()
    return jsonify({'message': 'Added to favourites'}), 201

@app.route('/api/profiles/matches/<int:profile_id>', methods=['GET'])
def get_matches(profile_id):
    base_profile = Profile.query.get_or_404(profile_id)
    matches = Profile.query.filter(
        Profile.sex == base_profile.sex,
        Profile.race == base_profile.race,
        Profile.parish == base_profile.parish
    ).all()

    return jsonify([p.serialize() for p in matches])

@app.route('/api/search', methods=['GET'])
def search_profiles():
    name = request.args.get('name')
    birth_year = request.args.get('birth_year')
    sex = request.args.get('sex')
    race = request.args.get('race')

    query = Profile.query

    if name:
        query = query.join(Users).filter(Users.name.ilike(f'%{name}%'))
    if birth_year:
        query = query.filter(Profile.birth_year == birth_year)
    if sex:
        query = query.filter(Profile.sex.ilike(f'%{sex}%'))
    if race:
        query = query.filter(Profile.race.ilike(f'%{race}%'))

    results = query.all()
    return jsonify([p.serialize() for p in results])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@app.route('/api/users/<int:user_id>/favourites', methods=['GET'])
def get_user_favourites(user_id):
    favs = Favourite.query.filter_by(user_id_fk=user_id).all()
    return jsonify([fav.fav_user_id_fk for fav in favs])

@app.route('/api/users/favourites/<int:N>', methods=['GET'])
def top_favourites(N):
    from sqlalchemy import func

    fav_counts = db.session.query(
        Favourite.fav_user_id_fk,
        func.count(Favourite.fav_user_id_fk).label('count')
    ).group_by(Favourite.fav_user_id_fk).order_by(func.count(Favourite.fav_user_id_fk).desc()).limit(N).all()

    return jsonify([{'user_id': row[0], 'count': row[1]} for row in fav_counts])

@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(Users).filter_by(id=id)).scalar()

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404