"""Tests for participant deletion endpoint"""


def test_delete_removes_participant_from_activity(client):
    """Test that a participant can be successfully removed from an activity"""
    # Arrange
    email = "remove_test@mergington.edu"
    activity_name = "Gym Class"

    # First, add the participant
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    assert email in response.json()["message"]

    # Verify the student was actually removed
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_delete_nonexistent_participant_returns_404(client):
    """Test that deleting a non-registered participant fails"""
    # Arrange
    email = "never_signed_up@mergington.edu"
    activity_name = "Tennis Club"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]


def test_delete_from_nonexistent_activity_returns_404(client):
    """Test that deleting from a non-existent activity fails"""
    # Arrange
    email = "test@mergington.edu"
    activity_name = "Nonexistent Activity"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_delete_and_resigned_for_activity(client):
    """Test that a deleted participant can sign up again"""
    # Arrange
    email = "resigner@mergington.edu"
    activity_name = "Music Band"

    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Delete
    delete_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    assert delete_response.status_code == 200

    # Act - Re-signup
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert signup_response.status_code == 200

    # Verify they're registered again
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants
