from models import User, db, Post
from app import app

#Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

#if table isn't empty, empty it
    User.query.delete()
    Post.query.delete()

    #Add users
    JessKelly = User(first_name="Jessica", last_name="Kelly")

    CraigThom = User(first_name="Craig", last_name="Thompson", image_url="https://tinyurl.com/y33ftsdy")

    KylieJackson = User(first_name="Kylie", last_name="Jackson", image_url="https://tinyurl.com/mvem9kp7")

    #Add new objects to session + commit to DB
    db.session.add_all([JessKelly, CraigThom, KylieJackson])
    db.session.commit()

    #Add posts
    JessPost = Post(title="My First Post", content="Wow posting is fun!", user_id=1)

    CraigPost =Post(title="My First Post", content="Wow posting is fun!", user_id=2)

    KyliePost = Post(title="My First Post", content="Wow posting is fun!", user_id=3)

    #Add new objects to session + commit to DB
    db.session.add_all([JessPost, CraigPost, KyliePost])
    db.session.commit()