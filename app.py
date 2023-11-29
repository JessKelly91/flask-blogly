"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.debug = True
app.config ['SECRET_KEY'] = 'bloglyappsecretkey'
app.config ['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def redirect_to_user_list():
    """redirect to user lists"""

    return redirect('/users')

@app.route('/users')
def list_all_users():
    """List all current users in the database"""
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', users=users)

@app.route('/new')
def show_add_user_form():
    """Show the add new user form"""

    return render_template('new.html')

@app.route('/new', methods = ['POST'])
def add_new_user():
    """Handle submission of new user form"""
    
    #get info from form
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form.get("image-url", None)

    #create new instance of User based on form info
    new_user = User(first_name = first_name, last_name = last_name, image_url=image_url)

    #update in session and commit to db
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show user details for single user"""
    user = User.query.get_or_404(user_id)
    
    image_url = user.image_url

    return render_template('user_detail.html', user=user, image_url=image_url)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show the edit user form"""
    
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_user_form(user_id):
    """Handle submission of edit user form and display update user detail page"""
    user = User.query.get_or_404(user_id)

    #get info from the form
    #if blank, default to previous info in database
    user.first_name = request.form.get("first-name")if request.form.get("first-name") else user.first_name
    user.last_name = request.form.get("last-name") if request.form.get("last-name") else user.last_name
    user.image_url = request.form.get("image-url") if request.form.get("image-url") else user.image_url

    #update in session and db
    db.session.commit()

    return redirect (f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete the show user from the page"""
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')