import unittest
import logging
import models
from datetime import datetime
from models.session import Session
from models.category import Category

logging.basicConfig(level=logging.DEBUG)

class TestSessionModel(unittest.TestCase):
    def setUp(self):
        # Setup SQLAlchemy engine and session
        models.storage.reload
        logging.debug("Establishing db connection ...")

    def tearDown(self):
        # Clean up the session and drop all tables
        models.storage.close()
        logging.debug("Clean up the session and drop all tables ...")


    def test_create_session(self):
        session_data = {
            "date": datetime.now(),
            "duration": 120,
            }
        session = Session(**session_data)
        models.storage.new(session)
        models.storage.save()

        self.assertIsNotNone(session.id)
        self.assertIsNotNone(session.created_at)
        self.assertIsNotNone(session.updated_at)
        self.assertEqual(session.duration, 120)
        logging.info("Testing session creation ...")


    def test_read_session(self):
        session_data = {
            "date": datetime.now(),
            "duration": 120,
            }
        session = Session(**session_data)
        models.storage.new(session)
        models.storage.save()

        retrieved_session = models.storage.get(Session, session.id)
        self.assertIsNotNone(retrieved_session)
        logging.info("Retrieving a session ...")

    def test_update_session(self):
        session_data = {
            "date": datetime.now(),
            "duration": 120,
            }
        session = Session(**session_data)
        models.storage.new(session)
        models.storage.save()

        new_duration = 60
        session.duration = new_duration
        models.storage.save()

        updated_session = models.storage.get(Session, session.id)
        self.assertEqual(updated_session.duration, new_duration)
        logging.info("Updating a session ...")


    def test_delete_session(self):
        session_data = {
            "date": datetime.now(),
            "duration": 120,
            }
        session = Session(**session_data)

        models.storage.new(session)
        models.storage.save()

        models.storage.delete(session)
        models.storage.save()

        deleted_session = models.storage.get(Session, session.id)
        self.assertIsNone(deleted_session)
        logging.info("Deleting a session ...")


    def test_add_session_to_category(self):
        # Create a category
        category = Category(category_name='Test Category')
        models.storage.new(category)
        models.storage.save()

        # Create a session and associate it with the category
        session = Session(
            category_id=category.id, 
            date='2023-10-25', 
            duration=60, 
            )
        models.storage.new(session)
        models.storage.save()

        # Query the category and check if the session is associated
        retrieved_category = models.storage.get(Category, category.id)
        self.assertEqual(len(retrieved_category.sessions), 1)
        self.assertEqual(retrieved_category.sessions[0].id, session.id)
        logging.info("Testing relationship ...")


    def test_add_session_to_existing_category(self):
        category_id = "d767a76f-28ee-4262-b9ef-cafa36223aeb"
        category = models.storage.get(Category, category_id)

        if category:
            # create a new patient
            session = Session(
                date='2023-10-25', 
                duration=60, 
            )

            category.session = session
            models.storage.save()
            logging.info("Adding session to existing category ...")
        else:
            logging.warning("Category not found in the database")
        # retrieved_category = models.storage.get(Category, category_id)
        # print("Category's session: {}".format(retrieved_category.sessions))

if __name__ == "__main__":
    unittest.main()
