import unittest
from datetime import datetime
from models.payment import Payment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestPaymentModel(unittest.TestCase):
    def setUp(self):
        # Set up a SQLite in-memory database for testing
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # Create tables in the in-memory database
        Payment.metadata.create_all(bind=engine)

    def test_create_payment(self):
        payment_data = {
            "patient_id": "123",
            "therapist_id": "456",
            "session_id": "789",
            "amount": 100.5,
            "date": datetime(2023, 10, 23, 14, 30, 0),
            "status": True
        }
        payment = Payment(**payment_data)
        self.session.add(payment)
        self.session.commit()

        # Retrieve the payment from the database and assert its attributes
        retrieved_payment = self.session.query(Payment).filter_by(id=payment.id).first()
        self.assertEqual(retrieved_payment.patient_id, payment_data["patient_id"])
        self.assertEqual(retrieved_payment.therapist_id, payment_data["therapist_id"])
        self.assertEqual(retrieved_payment.session_id, payment_data["session_id"])
        self.assertEqual(retrieved_payment.amount, payment_data["amount"])
        self.assertEqual(retrieved_payment.date, payment_data["date"])
        self.assertEqual(retrieved_payment.status, payment_data["status"])

    def test_update_payment(self):
        # Create a payment
        payment_data = {
            "patient_id": "123",
            "therapist_id": "456",
            "session_id": "789",
            "amount": 100.5,
            "date": datetime(2023, 10, 23, 14, 30, 0),
            "status": True
        }
        payment = Payment(**payment_data)
        self.session.add(payment)
        self.session.commit()

        # Update the payment's attributes
        updated_amount = 200.0
        payment.amount = updated_amount
        self.session.commit()

        # Retrieve the payment from the database and assert the updated amount
        retrieved_payment = self.session.query(Payment).filter_by(id=payment.id).first()
        self.assertEqual(retrieved_payment.amount, updated_amount)

    def test_delete_payment(self):
        # Create a payment
        payment_data = {
            "patient_id": "123",
            "therapist_id": "456",
            "session_id": "789",
            "amount": 100.5,
            "date": datetime(2023, 10, 23, 14, 30, 0),
            "status": True
        }
        payment = Payment(**payment_data)
        self.session.add(payment)
        self.session.commit()

        # Delete the payment from the database
        self.session.delete(payment)
        self.session.commit()

        # Attempt to retrieve the payment; it should not exist in the database
        retrieved_payment = self.session.query(Payment).filter_by(id=payment.id).first()
        self.assertIsNone(retrieved_payment)

    def tearDown(self):
        # Clean up resources after each test
        self.session.close()

if __name__ == "__main__":
    unittest.main()
