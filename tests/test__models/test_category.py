import unittest
import models
import logging
from models.base_model import Base  # Import your SQLAlchemy Base object
from models.category import Category

logging.basicConfig(level=logging.DEBUG)

class TestCategoryModel(unittest.TestCase):
    def setUp(self):
        # Setup SQLAlchemy engine and session
        models.storage.reload()
        logging.debug("Establishing db connection ...")

    def tearDown(self):
        models.storage.close()
        logging.debug("Clean up the session and drop all table ...")

    def test_create_category(self):
        category_data = {
            "category_name" : "wierd"
        }
        category = Category(**category_data)
        models.storage.new(category)
        models.storage.save()

        self.assertIsNotNone(category.id)
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)
        self.assertEqual(category.category_name, category_data["category_name"])
        logging.debug("Testing create category ...")

    def test_read_category(self):
        category_data = {
            "category_name" : "wierd"
        }
        category = Category(**category_data)
        models.storage.new(category)
        models.storage.save()

        retrieved_category = models.storage.get(Category, category.id)
        self.assertIsNotNone(retrieved_category)
        self.assertEqual(retrieved_category.category_name, "wierd")


    def test_update_category(self):
        category_data = {
            "category_name": "wierd."
        }
        category = Category(**category_data)
        models.storage.new(category)
        models.storage.save()

        new_name = "Interesting."
        category.category_name = new_name
        models.storage.save()

        updated_category = models.storage.get(Category, category.id)
        self.assertEqual(updated_category.category_name, new_name)

    def test_delete_category(self):
        category_data = {
            "category_name": "Weird."
        }
        category = Category(**category_data)
        models.storage.new(category)
        models.storage.save()

        models.storage.delete(category)
        models.storage.save()

        deleted_category = models.storage.get(Category, category.id)
        self.assertIsNone(deleted_category)

if __name__ == "__main__":
    unittest.main()
