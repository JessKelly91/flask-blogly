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
    JessOne = Post(title="Jess's First Post", content="Wow posting is fun!", user_id=1)

    CraigOne =Post(title="Craig's First Post", content="Wow posting is fun!", user_id=2)

    KylieOne = Post(title="Kylie's First Post", content="Wow posting is fun!", user_id=3)

    JessTwo = Post(title="Jess's Second Post", content="What a wonder!", user_id=1)

    CraigTwo = Post(title="Craig's Second Post", content="What a wonder!", user_id=2)

    KylieTwo = Post(title="Kylie's Second Post", content="What a wonder!", user_id=3)

    JessThree = Post(title="Jess's Third Post", content="Another one!", user_id=1)

    CraigThree = Post(title="Craig's Third Post", content="Another one!", user_id=2)

    KylieThree = Post(title="Kylie's Third Post", content="Another one!", user_id=3)


    #Add new objects to session + commit to DB
    db.session.add_all([JessOne, CraigOne, KylieOne, JessTwo, CraigTwo, KylieTwo, JessThree, CraigThree, KylieThree])
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
