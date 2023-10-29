import unittest
from models.therapist import Therapist
from models.user import User
import models
import logging

logging.basicConfig(level=logging.DEBUG)

class TestTherapistModel(unittest.TestCase):
    def setUp(self):
        # Setup SQLAlchemy engine and session
        models.storage.reload()
        logging.debug("db connection ...")

    def tearDown(self):
        # Clean up the session and drop all tables
        models.storage.close()
        logging.debug("Clean up the session and drop all tables ...")


    def test_create_therapist(self):
        # Create a Therapist
        therapist = Therapist(
            first_name='John', 
            last_name='Doe', 
            phone=123456789, 
            email='john.doe@example.com', 
            password='password', 
            specialization="Psychology",
            experience="5 years",
            availability=True
        )

        # Save the User and Therapist to the database
        models.storage.new(therapist)
        models.storage.save()

        # Retrieve the therpist
        retrieved_therapist = models.storage.get(Therapist, therapist.id)
        self.assertIsNotNone(retrieved_therapist)
        self.assertEqual(retrieved_therapist.first_name, "John")
        self.assertEqual(retrieved_therapist.last_name, "Doe")
        self.assertEqual(retrieved_therapist.phone, 123456789)
        self.assertEqual(retrieved_therapist.email, "john.doe3@example.com")
        self.assertEqual(retrieved_therapist.therapist.specialization, 'Psychology')
        self.assertEqual(retrieved_therapist.therapist.experience, '5 years')

        logging.debug("checking therapist creation ...")


    def test_read_therapist(self):
        therapist_id = ""
        retrieved_therapist = models.storage.get(Therapist, therapist_id)
        self.assertIsNotNone(retrieved_therapist)
        self.assertEqual(retrieved_therapist.first_name, "John")
        self.assertEqual(retrieved_therapist.last_name, "Doe")
        self.assertEqual(retrieved_therapist.phone, 123456789)
        self.assertEqual(retrieved_therapist.email, "john.doe3@example.com")
        self.assertEqual(retrieved_therapist.therapist.specialization, 'Psychology')
        self.assertEqual(retrieved_therapist.therapist.experience, '5 years')

        logging.debug("reading newly created therapist: {}".format(retrieved_therapist))

    def test_update_therapist(self):
        therapist_id = ""
        therapist = models.storage.get(Therapist, therapist_id)
        new_specialization = "Counseling"
        therapist.specialization = new_specialization
        models.storage.save()

        updated_therapist = models.storage.get(Therapist, therapist.id)
        self.assertEqual(updated_therapist.specialization, new_specialization)

    def test_delete_therapist(self):
        therapist_id = ""
        therapist = models.storage.get(Therapist, therapist_id)
        
        models.storage.delete(therapist)
        models.storage.save()

        deleted_therapist = models.storage.get(Therapist, therapist.id)
        self.assertIsNone(deleted_therapist)

if __name__ == "__main__":
    unittest.main()
