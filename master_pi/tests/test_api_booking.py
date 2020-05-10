import pytest

class TestApiBookingEndpoints:
    def test_get(self, client):
        """Testing get returns the right bookings for the right user
        """

        response = client.get('/api/booking?username=dummy')
        expected_data = b'{"bookings":[{"book_time":"2020-05-09T10:22:51","car":{"body_type":"SUV","colour":"Black","cost_per_hour":15,"id":1,"location":null,"make":"Toyota","no_seats":5},"car_id":1,"duration":3,"gcal_id":null,"id":2,"username":"dummy"},{"book_time":"2020-05-09T02:22:51","car":{"body_type":"Pickup","colour":"Silver","cost_per_hour":25,"id":2,"location":null,"make":"Tesla","no_seats":6},"car_id":2,"duration":1,"gcal_id":null,"id":1,"username":"dummy"}]}\n'
        print(response.data)
        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_make_booking_success(self, client):
        """Testing that making a booking works when booking criteria is met
        """

        response = client.post(
            '/api/booking',
            json={
                "car_id": 1,
                "username": "john",
                "duration": 2
            }
        )
        expected_data = b'{"message":"Success"}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_make_booking_fail_missing_duration(self, client):
        """Testing that making a booking fails when missing duration
        """

        response = client.post(
            '/api/booking',
            json={
                "car_id": 1,
                "username": "john"
            }
        )
        expected_data = b'{"message":"Missing duration"}\n'

        assert (response.status == '400 BAD REQUEST')
        assert (response.data == expected_data)

    def test_make_booking_fail_already_booked(self, client):
        """Testing that making a booking fails when the car is already booked
        """
        # User books car for 2 hours
        client.post(
            '/api/booking',
            json={
                "car_id": 1,
                "username": "dummy",
                "duration": 2
            }
        )

        # Seperate user tries to book the same car in the window it is booked for
        response = client.post(
            '/api/booking',
            json={
                "car_id": 1,
                "username": "john",
                "duration": 1
            }
        )
        expected_data = b'{"message":"Car is currently booked"}\n'

        print(response.data)
        print(response.status)

        assert (response.status == '401 UNAUTHORIZED')
        assert (response.data == expected_data)

    def test_delete_booking(self, client):
        """Testing that deleting a booking succeeds
        """
        # User books car for 2 hours
        response = client.delete('/api/booking?id=1')

        assert (response.status == '200 OK')
