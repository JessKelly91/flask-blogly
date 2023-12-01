"""Test app.py routes"""
from unittest import TestCase
from app import app
from models import User, db


class User_Views(TestCase):

    def setUp(self):
        """Clean up any existing users."""
        with app.app_context():
            #use test database
            app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
            app.config['SQLALCHEMY_ECHO'] = False

            #make flask errors be real errors - rather than HTML pages with error info
            app.config['TESTING'] = True

            #don't use flask DebugToolbar
            app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

            db.drop_all()
            db.create_all()

            User.query.delete()

            user = User(first_name="Jessica", last_name="Kelly", image_url='https://tinyurl.com/mrx6kek8')
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id
    

    # def tearDown(self):
    #     """clean up any fouled transaction"""
    #     db.session.rollback()
    
    def test_list_users(self):
            """Test the homepage"""
            with app.test_client() as client:
                resp = client.get('/users')
                html = resp.get_data(as_text = True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h2>Users:</h2>', html)
                self.assertIn('Jessica', html)


    def test_show_new_user_form(self):
        """Test new user form"""
        with app.test_client() as client:
            resp = client.get('/new')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/new" method="POST">', html)

    
    def test_show_user_details(self):
        """Test user detail page"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="profile-buttons">', html)
            self.assertIn('<h1>Jessica Kelly</h1>', html)

    def test_show_edit_user_form(self):
        """Test edit user pages"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a class="btn btn-info" id="cancel-edit-user" href="/users/1" role="button">Cancel</a>', html)

    def test_delete_user_redirect(self):
        """Test delete route
        Follow redirect and be sure name is not in html response
        """
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text = True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Jessica',html)
