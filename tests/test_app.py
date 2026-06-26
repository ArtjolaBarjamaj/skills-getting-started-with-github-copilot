import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_success(self):
        """Test successfully retrieving all activities"""
        # Arrange
        # No setup needed - activities already populated
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        # Verify each activity has required fields
        for activity_name, details in data.items():
            assert "description" in details
            assert "schedule" in details
            assert "max_participants" in details
            assert "participants" in details
            assert isinstance(details["participants"], list)


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self):
        """Test successfully signing up for an activity"""
        # Arrange
        email = "newstudent@example.com"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_nonexistent_activity(self):
        """Test signup for activity that doesn't exist"""
        # Arrange
        email = "student@example.com"
        activity = "Nonexistent Activity"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate(self):
        """Test signing up twice for the same activity"""
        # Arrange
        email = "duplicate@example.com"
        activity = "Programming Class"
        
        # Act - First signup
        response1 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert first signup succeeds
        assert response1.status_code == 200
        
        # Act - Second signup with same email
        response2 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert second signup fails
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"].lower()


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self):
        """Test successfully unregistering from an activity"""
        # Arrange
        email = "unregister@example.com"
        activity = "Soccer Team"
        
        # Sign up first
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        assert email in data["message"]

    def test_unregister_nonexistent_activity(self):
        """Test unregistering from activity that doesn't exist"""
        # Arrange
        email = "student@example.com"
        activity = "Nonexistent Activity"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered(self):
        """Test unregistering when not signed up"""
        # Arrange
        email = "notregistered@example.com"
        activity = "Drama Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"].lower()
