import unittest
import logging
import models
from models.patient import Patient
from models.afri_user import User

logging.basicConfig(level=logging.DEBUG)

class TestPatientModel(unittest.TestCase):
    def setUp(self):
        # Setup SQLAlchemy engine and session
        models.storage.reload
        logging.debug("Establishing db connection ...")

    def tearDown(self):
        # Clean up the session and drop all tables
        models.storage.close()
        logging.debug("Clean up the session and drop all tables ...")


    def test_create_patient(self):
        patient_data = {
            "history": "Medical history of the patient."
        }
        patient = Patient(**patient_data)
        models.storage.new(patient)
        models.storage.save()

        self.assertIsNotNone(patient.id)
        self.assertIsNotNone(patient.created_at)
        self.assertIsNotNone(patient.updated_at)
        self.assertEqual(patient.history, patient_data["history"])

    def test_read_patient(self):
        patient_data = {
            "history": "Medical history of the patient."
        }
        patient = Patient(**patient_data)
        models.storage.new(patient)
        models.storage.save()

        retrieved_patient = models.storage.get(Patient, patient.id)
        self.assertIsNotNone(retrieved_patient)
        self.assertEqual(retrieved_patient.history, patient_data["history"])

    def test_update_patient(self):
        patient_data = {
            "history": "Medical history of the patient."
        }
        patient = Patient(**patient_data)
        models.storage.new(patient)
        models.storage.save()

        new_history = "Updated medical history of the patient."
        patient.history = new_history
        models.storage.save()

        updated_patient = models.storage.get(Patient, patient.id)
        self.assertEqual(updated_patient.history, new_history)

    def test_delete_patient(self):
        patient_data = {
            "history": "Medical history of the patient."
        }
        patient = Patient(**patient_data)
        models.storage.new(patient)
        models.storage.save()

        models.storage.delete(patient)
        models.storage.save()

        deleted_patient = models.storage.get(Patient, patient.id)
        self.assertIsNone(deleted_patient)

    def test_one_to_one_relationship(self):
    # Create a User
        user = User(
            first_name='Peace', 
            last_name='Hunter', 
            phone=1234567897, 
            email='peace@hunter7.com', 
            password='password', 
            role='patient'
        )

        # Create a Patient
        patient = Patient(
            history="I am allergic to therapists"
        )

        # Establish the one-to-one relationship
        user.patient = patient
        patient.user = user

        # Save the User and patient to the database
        models.storage.new(user)
        models.storage.new(patient)
        models.storage.save()

        # Retrieve the user and check if the patients relationship is correctly established
        retrieved_user = models.storage.get(User, user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertIsNotNone(retrieved_user.patient)
        self.assertEqual(retrieved_user.patient.history, 'I am allergic to therapists')  # Correct history value

        logging.debug("adding user and patient together ...")

    def test_add_patient_to_existing_user(self):
        user_id = "fc2f1b5d-092d-48a9-9713-c72b204a92fc"
        user = models.storage.get(User, user_id)

        if user:
            # create a new patient
            patient = Patient(
                history = "theres some kauguruki in me"
            )

            user.patient = patient
            models.storage.save()
        else:
            print("User not found in the database")
        retrieved_user = models.storage.get(User, user_id)
        print("User's patient: {}".format(retrieved_user.patient))

        logging.debug("Adding patient to existing user ...")


if __name__ == "__main__":
    unittest.main()
