import unittest
from models.engine.db_config import DbConfig
from models.afri_user import User

class TestAfriUser(unittest.TestCase):

    def setUp(self):
        # Initialize the database connection before each test
        self.db_config = DbConfig()
        self.db_config.reload()

    def tearDown(self):
        # Close the database connection after each test
        self.db_config.close()

    def test_insert_user(self):
        # Create a new User object
        new_user = User(
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="john.doe@example.com",
            password="password123",
            role="user"
        )
        
        # Insert the user into the database
        self.db_config.new(new_user)
        self.db_config.save()

        # Retrieve the inserted user from the database
        inserted_user = self.db_config.get(User, new_user.id)

        # Assert that the user was inserted successfully
        self.assertIsNotNone(inserted_user)
        self.assertEqual(inserted_user.first_name, "John")
        self.assertEqual(inserted_user.last_name, "Doe")
        self.assertEqual(inserted_user.phone, "1234567890")
        self.assertEqual(inserted_user.email, "john.doe@example.com")
        self.assertEqual(inserted_user.role, "user")

if __name__ == '__main__':
    unittest.main()
