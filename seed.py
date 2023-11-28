from models import User, db
from app import app

#Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

#if table isn't empty, empty it
    User.query.delete()

    #Add users
    JessKelly = User(first_name="Jessica", last_name="Kelly")

    CraigThom = User(first_name="Craig", last_name="Thompson", image_url="https://tinyurl.com/y33ftsdy")

    KylieJackson = User(first_name="Kylie", last_name="Jackson", image_url="https://tinyurl.com/mvem9kp7")

    


    #Add new objects to session
    db.session.add(JessKelly)
    db.session.add(CraigThom)
    db.session.add(KylieJackson)

    #commit to database
    db.session.commit()