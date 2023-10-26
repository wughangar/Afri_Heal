import unittest
import logging
import models
from models.afri_user import User

logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG


class TestAfriUser(unittest.TestCase):

    def setUp(self):
        # Initialize the database connection before each test
        self.db_config = models.storage
        self.db_config.reload()
        logging.debug("testing user set up")

    def tearDown(self):
        # Close the database connection after each test
        self.db_config.close()
        logging.debug("testing user tear down")

    def test_insert_user_as_therapist(self):
        # Create a new User object
        new_user = User(
            first_name="afri",
            last_name="heal",
            phone=123456789,
            email="afri@heal.com",
            password="password123",
            role="therapist"
        )
        
        # Insert the user into the database
        self.db_config.new(new_user)
        self.db_config.save()


        # Retrieve the inserted user from the database
        inserted_user = self.db_config.get(User, new_user.id)

        # Assert that the user was inserted successfully
        self.assertIsNotNone(inserted_user)
        self.assertEqual(inserted_user.first_name, "afri")
        self.assertEqual(inserted_user.last_name, "heal")
        self.assertEqual(inserted_user.phone, 123456789)
        self.assertEqual(inserted_user.email, "afri@heal.com")
        self.assertEqual(inserted_user.role, "therapist")

        logging.info("testing user as therapist")


    def test_insert_user_as_patient(self):
        # Create a new User object
        new_user = User(
            first_name="makit",
            last_name="count",
            phone=1234567891,
            email="makit@count.com",
            password="password123",
            role="patient"
        )
        
        # Insert the user into the database
        self.db_config.new(new_user)
        self.db_config.save()

        # Retrieve the inserted user from the database
        inserted_user = self.db_config.get(User, new_user.id)

        # Assert that the user was inserted successfully
        self.assertIsNotNone(inserted_user)
        self.assertEqual(inserted_user.first_name, "makit")
        self.assertEqual(inserted_user.last_name, "count")
        self.assertEqual(inserted_user.phone, 1234567891)
        self.assertEqual(inserted_user.email, "makit@count.com")
        self.assertEqual(inserted_user.role, "patient")

        logging.debug("testing user as patient")


if __name__ == '__main__':
    unittest.main()
