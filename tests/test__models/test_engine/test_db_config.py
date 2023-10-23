import unittest
from models.engine.db_config import DbConfig

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
        user_table_exists = self.db_config._DbConfig__engine.dialect.has_table(self.db_config._DbConfig__engine, "users")
        self.assertTrue(user_table_exists)

    # Add more test cases for other methods in DbConfig class if needed

if __name__ == '__main__':
    unittest.main()
