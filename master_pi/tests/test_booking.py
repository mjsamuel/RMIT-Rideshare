import pytest
from datetime import datetime, timedelta
from app.models.booking import Booking

class TestBooking:
    def test_get_end_date(self):
        """Testing that get_end_time() returns the correct value
        """
        # Creating booking object
        book_time = datetime.utcnow()
        duration = 3
        booking = Booking(1, "dummy", book_time, duration)

        # Checking end time is correct
        end_time = book_time + timedelta(hours=duration)
        assert (end_time == booking.get_end_time())
