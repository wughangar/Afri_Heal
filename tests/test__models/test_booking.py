#!/usr/bin/python3

import unittest
import models
import logging
from models.booking import Booking
from models.session import Session
from models.patient import Patient
from models.therapist import Therapist
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)


class TestBookingModel(unittest.TestCase):
    def setUp(self):
        models.storage.reload()
        logging.debug("testing db set up ...")

    def tearDown(self):
        # Clean up the session and drop all tables
        models.storage.close()
        logging.debug("testing ear down ...")


    def test_create_booking(self):
        booking_data = {
            "date": datetime.now(),
            "status": True
        }
        booking = Booking(**booking_data)
        models.storage.new(booking)
        models.storage.save()
        logging.debug("creating new booking without any relationship...")

        self.assertIsNotNone(booking.id)
        self.assertIsNotNone(booking.created_at)
        self.assertIsNotNone(booking.updated_at)
        self.assertEqual(booking.date, booking_data["date"])
        self.assertEqual(booking.status, booking_data["status"])

    def test_read_booking(self):
        booking_data = {
            # "patient_id": "patient123",
            # "therapist_id": "therapist123",
            # "session_id": "session123",
            "date": datetime.now(),
            "status": True
        }
        booking = Booking(**booking_data)
        models.storage.new(booking)
        models.storage.save()

        retrieved_booking = models.storage.get(Booking, booking.id)
        self.assertIsNotNone(retrieved_booking)
        # self.assertEqual(retrieved_booking.patient_id, booking_data["patient_id"])
        # self.assertEqual(retrieved_booking.therapist_id, booking_data["therapist_id"])
        # self.assertEqual(retrieved_booking.session_id, booking_data["session_id"])
        self.assertEqual(retrieved_booking.date, booking_data["date"])
        self.assertEqual(retrieved_booking.status, booking_data["status"])
        logging.info("testing booking retrieval ...")

    def test_update_booking(self):
        booking_data = {
            "date": datetime.now(),
            "status": True
        }
        booking = Booking(**booking_data)
        models.storage.new(booking)
        models.storage.save()

        new_status = False
        booking.status = new_status
        models.storage.save()

        models.storage.get(Booking, booking.id)
        self.assertEqual(booking.status, new_status)
        # self.assertEqual(updated_booking.status, new_status)
        logging.info("testing updating a booking status to false ...")

    def test_delete_booking(self):
        booking_data = {
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
        logging.info("Testing deleting a booking ...")

    """
        testing relationships
    """ 
    def test_add_booking_to_patient(self):
        # Retrieve a patient
        patient_id = "8b943f2a-438a-45cd-b3c6-cd46d4b7fd60"
        patient = models.storage.get(Patient, patient_id)
        if patient:
            
            # Retrieve a booking
            booking_id = "02bb5212-2426-4db7-82f1-cccd8f690784"
            booking = models.storage.get(Booking, booking_id)
            logging.info("booking found {}".format(booking) )
            if booking:
                patient.bookings = [booking]
                models.storage.save()
            else:
                logging.error("Booking not found")

        # Query the patient and check if the booking is associated
        retrieved_patient = models.storage.get(Patient, patient_id)
        self.assertEqual(len(retrieved_patient.bookings), 1)
        self.assertEqual(retrieved_patient.bookings[0].id, booking.id)

        logging.info("Adding bookings to a patient ...")

    def test_add_booking_to_session(self):
        # Retrieve a patient
        session_id = "10499188-6ce5-4dce-bb1d-11e2838fa817"
        session = models.storage.get(Session, session_id)
        if session:
            
            # Retrieve a booking
            booking_id = "02bb5212-2426-4db7-82f1-cccd8f690784"
            booking = models.storage.get(Booking, booking_id)
            logging.info("booking found {}".format(booking) )
            if booking:
                session.bookings = [booking]
                models.storage.save()
            else:
                logging.error("Booking not found")
        else:
            logging.error("Session not found")

        # Query the patient and check if the booking is associated
        retrieved_session = models.storage.get(Session, session_id)
        self.assertEqual(len(retrieved_session.bookings), 1)
        self.assertEqual(retrieved_session.bookings[0].id, booking.id)

        logging.info("Adding bookings to a session ...")

    def test_add_booking_to_therapist(self):
        # Retrieve a patient
        therapist_id = "135c7796-e968-4302-84da-27afeb4c6fa4"
        therapist = models.storage.get(Therapist, therapist_id)
        if therapist:
            
            # Retrieve a booking
            booking_id = "02bb5212-2426-4db7-82f1-cccd8f690784"
            booking = models.storage.get(Booking, booking_id)
            logging.info("booking found {}".format(booking) )
            if booking:
                therapist.bookings = [booking]
                models.storage.save()
            else:
                logging.error("Booking not found")
        else:
            logging.error("Session not found")

        # Query the patient and check if the booking is associated
        retrieved_therapist = models.storage.get(Therapist, therapist_id)
        self.assertEqual(len(retrieved_therapist.bookings), 1)
        self.assertEqual(retrieved_therapist.bookings[0].id, booking.id)

        logging.info("Adding bookings to a therapist ...")


    # def test_add_booking_to_therapist(self):
    #     # Create a therapist
    #     therapist = Therapist(therapist_name='Test Therapist')
    #     self.session.add(therapist)
    #     self.session.commit()

    #     # Create a booking and associate it with the therapist
    #     booking = Booking(therapist_id=therapist.id, date='2023-10-25', status=True)
    #     self.session.add(booking)
    #     self.session.commit()

    #     # Query the therapist and check if the booking is associated
    #     retrieved_therapist = self.session.query(Therapist).filter_by(id=therapist.id).first()
    #     self.assertEqual(len(retrieved_therapist.bookings), 1)
    #     self.assertEqual(retrieved_therapist.bookings[0].id, booking.id)

    # def test_add_booking_to_session(self):
    #     # Create a session
    #     session = Session(date='2023-10-25', status=True)
    #     self.session.add(session)
    #     self.session.commit()

    #     # Create a booking and associate it with the session
    #     booking = Booking(session_id=session.id, date='2023-10-25', status=True)
    #     self.session.add(booking)
    #     self.session.commit()

    #     # Query the session and check if the booking is associated
    #     retrieved_session = self.session.query(Session).filter_by(id=session.id).first()
    #     self.assertEqual(len(retrieved_session.bookings), 1)
    #     self.assertEqual(retrieved_session.bookings[0].id, booking.id)


if __name__ == "__main__":
    unittest.main()
