import unittest
from api.app import app, db
from forms.login_form import LoginForm

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        response = self.app.post('/register', data=dict(
            first_name='Jon',
            last_name='Do',
            email='johne@gmail.com',
            password='testpassword'
        ), follow_redirects=True)
        self.assertIn(b'Your account has been created!', response.data)

    def test_user_login(self):
        # Assuming you have a test user created in the database
        response = self.app.post('/login', data=dict(
            email='johne@gmail.com',
            password='testpassword'
        ), follow_redirects=True)
        self.assertIn(b'You have been logged in!', response.data)

    #def test_get_users_api(self):
        #response = self.app.get('/api/users')
        #self.assertEqual(response.status_code, 200)

    #def test_get_user_by_id_api(self):
        #response = self.app.get('/api/users/1')
        #self.assertEqual(response.status_code, 200)

    def test_create_review_api(self):
        response = self.app.post('/api/reviews', json={
            "patient_id": "1",
            "therapist_id": "1",
            "rating": 5,
            "comments": "Great therapist!"
            })
        self.assertEqual(response.status_code, 201)

    def test_get_reviews_api(self):
        response = self.app.get('/api/reviews')
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_id_api(self):
        response = self.app.get('/api/reviews/1')
        self.assertEqual(response.status_code, 200)

    def test_update_review_api(self):
        response = self.app.put('/api/reviews/1', json={
            "rating": 4,
            "comments": "Good therapist."
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_review_api(self):
        response = self.app.delete('/api/reviews/1')
        self.assertEqual(response.status_code, 200)

    def test_create_therapist_api(self):
        response = self.app.post('/api/therapists', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "1234567890",
            "email": "jane@example.com",
            "password": "testpassword",
            "specialization": "Psychologist",
            "experience": "5 years",
            "availability": "Monday, Wednesday"
        })
        self.assertEqual(response.status_code, 201)

    def test_get_therapists_api(self):
        response = self.app.get('/api/therapists')
        self.assertEqual(response.status_code, 200)

    def test_get_therapist_by_id_api(self):
        response = self.app.get('/api/therapists/eec54e2d-cb14-4f63-a224-1c439f970cc6')
        self.assertEqual(response.status_code, 200)

    def test_update_therapist_api(self):
        therapist_id = 'eec54e2d-cb14-4f63-a224-1c439f970cc6'
        response = self.app.put(f'/api/therapists/{therapist_id}', json={
            "availability": "Monday, Tuesday, Wednesday"
            })
        self.assertEqual(response.status_code, 200)

    def test_delete_therapist_api(self):
        therapist_id = 'eec54e2d-cb14-4f63-a224-1c439f970cc6'
        response = self.app.delete(f'/api/therapists/{therapist_id}')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
