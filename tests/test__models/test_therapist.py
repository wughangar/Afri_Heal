import unittest
from models.therapist import Therapist
from models.afri_user import User
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


    def test_one_to_one_relationship(self):
    # Create a User
        user = User(
            first_name='John', 
            last_name='Doe', 
            phone=1234567893, 
            email='john.doe3@example.com', 
            password='password', 
            role='therapist'
        )

        # Create a Therapist
        therapist = Therapist(
            specialization="Psychology",
            experience="5 years",
            availability=True
        )

        # Establish the one-to-one relationship
        user.therapist = therapist
        therapist.user = user

        # Save the User and Therapist to the database
        models.storage.new(user)
        models.storage.new(therapist)
        models.storage.save()

        # Retrieve the user and check if the therapists relationship is correctly established
        retrieved_user = models.storage.get(User, user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertIsNotNone(retrieved_user.therapist)
        self.assertEqual(retrieved_user.therapist.specialization, 'Psychology')  # Correct specialization value
        self.assertEqual(retrieved_user.therapist.experience, '5 years')

        logging.debug("checking relationship ...")


    def test_add_therapist_to_existing_user(self):
    # Load the existing user from the database
        user_id = "b8242c01-aa94-4c1f-bf38-050a1f6097c5"
        user = models.storage.get(User, user_id)

        # Check if the user exists
        if user:

        # Create a new therapist instance
            therapist = Therapist(
                specialization="Psychliastrist",
                experience="7 years",
                availability=True
            )

            # Establish the one-to-one relationship
            user.therapist = therapist

            # Save the User and Therapist to the database
            models.storage.save()
        else:
            print("User not found in the database.")


        # Optionally, you can verify the relationship
        retrieved_user = models.storage.get(User, user_id)
        print("User's therapist: {}".format(retrieved_user.therapist))



    def test_read_therapist(self):
        therapist_data = {
            "specialization": "Psychology",
            "experience": "5 years",
            "availability": True
        }
        therapist = Therapist(**therapist_data)
        models.storage.new(therapist)
        models.storage.save()

        retrieved_therapist = models.storage.get(Therapist, therapist.id)
        self.assertIsNotNone(retrieved_therapist)
        # self.assertEqual(retrieved_therapist.user_id, therapist_data["user_id"])
        self.assertEqual(retrieved_therapist.specialization, therapist_data["specialization"])
        self.assertEqual(retrieved_therapist.experience, therapist_data["experience"])
        self.assertEqual(retrieved_therapist.availability, therapist_data["availability"])

        logging.debug("reading newly created therapist: {}".format(retrieved_therapist))

    def test_update_therapist(self):
        therapist_data = {
            "specialization": "Psychology",
            "experience": "5 years",
            "availability": True
        }
        therapist = Therapist(**therapist_data)
        models.storage.new(therapist)
        models.storage.save()

        new_specialization = "Counseling"
        therapist.specialization = new_specialization
        models.storage.save()

        updated_therapist = models.storage.get(Therapist, therapist.id)
        self.assertEqual(updated_therapist.specialization, new_specialization)

    def test_delete_therapist(self):
        therapist_data = {
            "specialization": "Psychology",
            "experience": "5 years",
            "availability": True
        }
        therapist = Therapist(**therapist_data)
        models.storage.new(therapist)
        models.storage.save()

        models.storage.delete(therapist)
        models.storage.save()

        deleted_therapist = models.storage.get(Therapist, therapist.id)
        self.assertIsNone(deleted_therapist)

if __name__ == "__main__":
    unittest.main()
