"""Tests for activities endpoint"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    # Arrange
    # (no setup needed - activities already exist in app state)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_get_activities_have_required_fields(client):
    """Test that each activity has all required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, details in activities.items():
        assert isinstance(details, dict)
        assert required_fields.issubset(details.keys())
        assert isinstance(details["participants"], list)
        assert isinstance(details["max_participants"], int)


def test_root_redirects_to_index_html(client):
    """Test that GET / redirects to the static index page"""
    # Arrange
    # (no setup needed)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
