"""Tests for activity signup endpoint"""


def test_signup_successfully_adds_student_to_activity(client):
    """Test that a student can successfully sign up for an activity"""
    # Arrange
    email = "new_student@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]

    # Verify the student was actually added
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_with_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity fails"""
    # Arrange
    email = "test@mergington.edu"
    activity_name = "Nonexistent Activity"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_fails_with_400(client):
    """Test that a student cannot sign up twice for the same activity"""
    # Arrange
    email = "duplicate_tester@mergington.edu"
    activity_name = "Programming Class"

    # Act - First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert response1.status_code == 200

    # Act - Attempt duplicate signup
    response2 = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_with_special_characters_in_email(client):
    """Test that emails with special characters are handled correctly"""
    # Arrange
    from urllib.parse import quote
    email = "test+tag@mergington.edu"
    activity_name = "Art Studio"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={quote(email, safe='')}"
    )

    # Assert
    assert response.status_code == 200

    # Verify the student was added with the correct email
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants
