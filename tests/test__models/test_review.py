import unittest
from datetime import datetime
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestReviewModel(unittest.TestCase):
    def setUp(self):
        # Set up a SQLite in-memory database for testing
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # Create tables in the in-memory database
        Review.metadata.create_all(bind=engine)

    def test_create_review(self):
        review_data = {
            "patient_id": "123",
            "therapist_id": "456",
            "rating": 5,
            "date": datetime(2023, 10, 23, 14, 30, 0),
            "comments": "Great therapist!"
        }
        review = Review(**review_data)
        self.session.add(review)
        self.session.commit()

        # Retrieve the review from the database and assert its attributes
        retrieved_review = self.session.query(Review).filter_by(id=review.id).first()
        self.assertEqual(retrieved_review.patient_id, review_data["patient_id"])
        self.assertEqual(retrieved_review.therapist_id, review_data["therapist_id"])
        self.assertEqual(retrieved_review.rating, review_data["rating"])
        self.assertEqual(retrieved_review.date, review_data["date"])
        self.assertEqual(retrieved_review.comments, review_data["comments"])

    def test_update_review(self):
        # Create a review
        review_data = {
            "patient_id": "123",
            "therapist_id": "456",
            "rating": 5,
            "date": datetime(2023, 10, 23, 14, 30, 0),
            "comments": "Great therapist!"
        }
        review = Review(**review_data)
        self.session.add(review)
        self.session.commit()

        # Update the review's attributes
        updated_comments = "Excellent therapist!"
        review.comments = updated_comments
        self.session.commit()

        # Retrieve the review from the database and assert the updated comments
        retrieved_review = self.session.query(Review).filter_by(id=review.id).first()
        self.assertEqual(retrieved_review.comments, updated_comments)

    def test_delete_review(self):
        # Create a review
        review_data = {
            "patient_id": "123",
            "therapist_id": "456",
            "rating": 5,
            "date": datetime(2023, 10, 23, 14, 30, 0),
            "comments": "Great therapist!"
        }
        review = Review(**review_data)
        self.session.add(review)
        self.session.commit()

        # Delete the review from the database
        self.session.delete(review)
        self.session.commit()

        # Attempt to retrieve the review; it should not exist in the database
        retrieved_review = self.session.query(Review).filter_by(id=review.id).first()
        self.assertIsNone(retrieved_review)

    def tearDown(self):
        # Clean up resources after each test
        self.session.close()

if __name__ == "__main__":
    unittest.main()
