import unittest
import logging
import models
import sqlalchemy

logging.basicConfig(level=logging.DEBUG)  

class TestDbConfig(unittest.TestCase):

    def setUp(self):
        logging.debug("testing user set up ...")
        self.db_config = models.storage
        self.db_config.reload()

    def tearDown(self):
        self.db_config.close()
        logging.debug("testing user tear down ...")


    def test_database_connection(self):
        # Test if the database connection is successful
        self.assertIsNotNone(self.db_config._DbConfig__engine)

    def test_table_creation(self):
        # Test if the tables are created properly
        logging.debug("Testing table creation ...")
        insp = sqlalchemy.inspect(self.db_config._DbConfig__engine)
        table_names = insp.get_table_names()
        logging.debug("All Tables in Database: ")
        print(table_names)
        user_table_exists = insp.has_table("users")
        logging.debug("User Table Exists: ")
        print(user_table_exists)

    def test_user(self):
        # Assuming you have a User model mapped to the "users" table
        from models.afri_user import User  # Import your User model
# Create a new user object
        new_user = User(
            first_name="chet",
            last_name="Teg",
            phone=123456788,
            email="makit@count.com",
            password="password123",
            role="therapist"
            )

# Add the user object to the session
        self.db_config._DbConfig__session.add(new_user)

# Commit the transaction to persist the changes to the database
        self.db_config._DbConfig__session.commit()



    # Add more test cases for other methods in DbConfig class if needed

if __name__ == '__main__':
    unittest.main()
