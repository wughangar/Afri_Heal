import unittest
from models.base_model import Base  # Import your SQLAlchemy Base object
from models.category import Category
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestCategoryModel(unittest.TestCase):
    def setUp(self):
        # Setup SQLAlchemy engine and session
        self.engine = create_engine('sqlite:///:memory:')  # Use in-memory SQLite database for testing
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create tables in the in-memory database
        Base.metadata.create_all(bind=self.engine)  # Access metadata from the Base object

    # Rest of your test methods go here...

if __name__ == "__main__":
    unittest.main()
