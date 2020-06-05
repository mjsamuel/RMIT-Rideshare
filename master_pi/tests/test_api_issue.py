import pytest, json

class TestApiIssueEndpoints:
    def test_new_issue_success(self, client):
        """Testing that reporting an issue succeeds when called with the correct
        information
        """
        response = client.post(
            '/api/issue',
            json={
                "car_id": 1,
                "username": "admin",
                "details": "Broken tail light",
            }
        )
        expected_data = b'{"message":"Success"}\n'

        assert (response.status == '200 OK')
        assert (response.data == expected_data)

    def test_new_issue_fail_invalid_role(self, client):
        """Testing that updating a car fails when not the user requesting then
        update is not an admin
        """
        response = client.post(
            '/api/issue',
            json={
                "car_id": 1,
                "username": "dummy",
                "details": "Broken tail light",
            }
        )
        expected_data = b'{"message":{"user":["User is not an admin."]}}\n'

        assert (response.status == '401 UNAUTHORIZED')
        assert (response.data == expected_data)
