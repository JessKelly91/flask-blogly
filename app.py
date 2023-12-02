"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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

#USER ROUTES
@app.route('/')
def show_homepage():
    """redirect to user lists"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('homepage.html', posts=posts)

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

    posts = Post.query.filter_by(user_id=user.id).all()

    return render_template('user_detail.html', user=user, image_url=image_url, posts=posts)

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

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """handle the deletion of a user"""
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

#POST ROUTES
@app.route('/users/<user_id>/posts/new')
def show_add_new_post_form(user_id):
    """Show new post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('new_post.html', user=user, tags=tags)


@app.route('/users/<user_id>/posts/new', methods=["POST"])
def handle_add_new_post(user_id):
    """handle submission of new post form"""
    user = User.query.get_or_404(user_id)

    #get info from form
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user.id)

    #add info to posts table
    db.session.add(new_post)
    db.session.commit()

    #get selected tags + commit to post_tag table
    selected_tags = request.form.getlist('tags')
    for tag in selected_tags:
        tag = Tag.query.filter_by(name=tag).one()
        if tag:
            new_post_tag = PostTag(post_id=new_post.id, tag_id=tag.id)
            db.session.add(new_post_tag)

    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/posts/<post_id>')
def show_post(post_id):
    """Show post details"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.user_id)

    tags = post.tags

    return render_template('show_post.html', post=post, user=user, tags=tags)

@app.route('/posts/<post_id>/edit')
def show_edit_post_form(post_id):
    """Show edit post form"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.user_id)

    return render_template('edit_post.html', post=post, user=user)

@app.route('/posts/<post_id>/edit', methods=["POST"])
def handle_edit_post_form(post_id):
    """Show edit post form"""
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)
    
    #get info from form
    #if blank, default to previous info in database
    post.title = request.form.get("title") if request.form.get("title") else post.title
    post.content = request.form.get("content") if request.form.get("content") else post.content
    post.user_id = user.id

    #update in session and db
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<post_id>/delete')
def handle_delete_post(post_id):
    """Handle deleting a post"""
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)

    db.session.delete(post)
    db.session.commit()

    return redirect (f'/users/{user.id}')

#TAG ROUTES
@app.route('/tags')
def show_all_tags():
    """Show all tags"""

    tags = Tag.query.order_by(Tag.name).all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<tag_id>')
def show_tag_details(tag_id):
    """Show individual tag details"""
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_detail.html', tag=tag)

@app.route('/tags/new')
def show_new_tag_form():
    """Show a form to create a new tag"""
    posts = Post.query.order_by(Post.title).all()

    return render_template('new_tag.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def handle_new_tag_form():
    """Handle the submission of new tag form"""

    name = request.form['name']
    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect(f'/tags/{new_tag.id}')

@app.route('/tags/<tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show a form to edit a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.order_by(Post.title).all()

    return render_template('edit_tag.html', tag=tag, posts=posts)

@app.route('/tags/<tag_id>/edit', methods=["POST"])
def handle_edit_tag_form(tag_id):
    """Handle the submission of edit tag form"""
    tag = Tag.query.get(tag_id)

    tag.name = request.form.get('name') if request.form.get('name') else tag.name

    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<tag_id>/delete')
def handle_delete_tag(tag_id):
    """Handle deleting a tag"""
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
