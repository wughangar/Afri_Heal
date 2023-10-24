import unittest
from models.booking import Booking
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import models
import logging

logging.basicConfig(level=logging.DEBUG)


class TestBookingModel(unittest.TestCase):
    def setUp(self):
        models.storage.reload()
        logging.debug("testing db set up ...")

    def tearDown(self):
        # Clean up the session and drop all tables
        models.storage.close()
        logging.debug("testingt ear down ...")


    def test_create_booking(self):
        booking_data = {
            "patient_id": "patient123",
            "therapist_id": "therapist123",
            "session_id": "session123",
            "date": datetime.now(),
            "status": True
        }
        booking = Booking(**booking_data)
        models.storage.new(booking)
        models.storage.save()
        logging.debug("creating new booking ...")

        self.assertIsNotNone(booking.id)
        self.assertIsNotNone(booking.created_at)
        self.assertIsNotNone(booking.updated_at)
        self.assertEqual(booking.patient_id, booking_data["patient_id"])
        self.assertEqual(booking.therapist_id, booking_data["therapist_id"])
        self.assertEqual(booking.session_id, booking_data["session_id"])
        self.assertEqual(booking.date, booking_data["date"])
        self.assertEqual(booking.status, booking_data["status"])

    def test_read_booking(self):
        booking_data = {
            "patient_id": "patient123",
            "therapist_id": "therapist123",
            "session_id": "session123",
            "date": datetime.now(),
            "status": True
        }
        booking = Booking(**booking_data)
        models.storage.new(booking)
        models.storage.save()

        retrieved_booking = models.storage.get(Booking, booking.id)
        logging.debug(f"retrieved booking: {retrieved_booking}")
        self.assertIsNotNone(retrieved_booking)
        self.assertEqual(retrieved_booking.patient_id, booking_data["patient_id"])
        self.assertEqual(retrieved_booking.therapist_id, booking_data["therapist_id"])
        self.assertEqual(retrieved_booking.session_id, booking_data["session_id"])
        self.assertEqual(retrieved_booking.date, booking_data["date"])
        self.assertEqual(retrieved_booking.status, booking_data["status"])
        logging.debug("testing booking retrieval ...")

    def test_update_booking(self):
        booking_data = {
            "patient_id": "patient123",
            "therapist_id": "therapist123",
            "session_id": "session123",
            "date": datetime.now(),
            "status": True
        }
        booking = Booking(**booking_data)
        models.storage.new(booking)
        models.storage.save()

        new_status = False
        booking.status = new_status
        models.storage.save()

        updated_booking = models.storage.get(Booking, booking.id)
        print(updated_booking)
        # self.assertEqual(updated_booking.status, new_status)
        logging.debug("testing updating a booking status to false ...")

    def test_delete_booking(self):
        booking_data = {
            "patient_id": "patient123456",
            "therapist_id": "therapist123456",
            "session_id": "session123456",
            "date": datetime.now(),
            "status": True
        }
        booking = Booking(**booking_data)
        models.storage.new(booking)
        models.storage.save()

        models.storage.delete(booking)
        models.storage.save()

        deleted_booking = models.storage.get(Booking, booking.id)
        self.assertIsNone(deleted_booking)

if __name__ == "__main__":
    unittest.main()
