"""Test app.py routes"""
from unittest import TestCase
from app import app
from models import User, db, Post


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

            post = Post(title="My first post", content="SQL-Alchemy is great!", user_id=1)
            db.session.add(post)
            db.session.commit()

            self.user_id = user.id
            self.post_id = post.id
            self.post_title = post.title
    

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
            self.assertIn('<h1>Jessica Kelly</h1>', html)
            self.assertIn(f'<a href="/posts/{self.post_id}">{self.post_title}</a>', html)

    def test_show_edit_user_form(self):
        """Test edit user pages"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a class="btn btn-info" id="cancel-edit-user" href="/users/{self.user_id}" role="button">Cancel</a>', html)

    def test_delete_user_redirect(self):
        """Test delete route
        Follow redirect and be sure name is not in html response
        """
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text = True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Jessica',html)

    def test_show_new_post_page(self):
        """Test showing new post form"""
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label for="title" class="form-label">Title:</label>', html)
    
    def test_show_post(self):
        """Test showing individual post"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('SQL-Alchemy is great!', html)
    
    def test_show_edit_post_form(self):
        """Test showing edit post form"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My first post', html)

    def test_delete_post_redirect(self):
        """Test delete route
        Follow redirect and be sure name is not in html response
        """
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text = True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('My first post',html)