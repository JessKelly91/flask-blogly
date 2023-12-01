from models import db, User, Post, Tag, PostTag
from app import app

#Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

#if table isn't empty, empty it
    User.query.delete()
    Post.query.delete()
    Tag.query.delete()
    PostTag.query.delete()

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

    #Add tags
    cringe = Tag(name="cringe")
    yolo = Tag(name="yolo")
    truth = Tag(name="truth")

    #Add new objects to session + commit to DB
    db.session.add_all([cringe, yolo, truth])
    db.session.commit()

    #Add post_tags
    post_tag = PostTag(post_id=1, tag_id=1)
    post_tag2 = PostTag(post_id=2, tag_id=2)
    post_tag3 = PostTag(post_id=3, tag_id=3)


    #Add new objects to session + commit to DB
    db.session.add_all([post_tag, post_tag2, post_tag3])
    db.session.commit()
