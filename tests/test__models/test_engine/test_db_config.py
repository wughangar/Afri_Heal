import unittest
from models.engine.db_config import DbConfig
import sqlalchemy

class TestDbConfig(unittest.TestCase):

    def setUp(self):
        self.db_config = DbConfig()
        self.db_config.reload()

    def tearDown(self):
        self.db_config.close()

    def test_database_connection(self):
        # Test if the database connection is successful
        self.assertIsNotNone(self.db_config._DbConfig__engine)

def test_table_creation(self):
    # Test if the tables are created properly
    print("Testing table creation ...")
    insp = sqlalchemy.inspect(self.db_config._DbConfig__engine)
    table_names = insp.get_table_names()
    print("All Tables in Database:", table_names)  # Add this line for debugging
    user_table_exists = insp.has_table("users")
    print("User Table Exists:", user_table_exists)  # Add this line for debugging
    self.assertTrue(user_table_exists)


    # Add more test cases for other methods in DbConfig class if needed

if __name__ == '__main__':
    unittest.main()
