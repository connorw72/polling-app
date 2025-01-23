import pytest
from app import app, db
from models import User, Poll, Option, Vote
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_register(client):
    response = client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "User created successfully"

def test_register_missing_fields(client):
    response = client.post("/register", json={
        "username": "testuser",
        "email": ""
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["msg"] == "Missing required fields"

def test_login_success(client):
    # Register user
    client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })

    # Login
    response = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Login successful"
    assert "access_token" in data

def test_login_invalid_email(client):
    response = client.post("/login", json={
        "email": "nonexistent@example.com",
        "password": "password123"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Invalid email"

def test_login_invalid_password(client):
    # Register user
    client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })

    # Login with wrong password
    response = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Invalid password"

def test_create_poll(client):
    # Register and login admin user
    client.post("/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    user = User.query.filter_by(email="admin@example.com").first()
    user.is_admin = True
    db.session.commit()

    access_token = create_access_token(identity=user.email)

    # Create poll
    response = client.post(
        "/create-poll",
        json={
            "question": "What is your favorite programming language?",
            "options": ["Python", "JavaScript", "C++"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Poll created successfully"
    assert data["poll"]["question"] == "What is your favorite programming language?"
    assert len(data["poll"]["options"]) == 3

def test_create_poll_unauthorized(client):
    # Register non-admin user
    client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    access_token = create_access_token(identity="testuser@example.com")

    # Attempt to create poll
    response = client.post(
        "/create-poll",
        json={
            "question": "What is your favorite programming language?",
            "options": ["Python", "JavaScript"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data["msg"] == "You are not authorized to create polls"

def test_create_poll_missing_fields(client):
    # Register and login admin user
    client.post("/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    user = User.query.filter_by(email="admin@example.com").first()
    user.is_admin = True
    db.session.commit()

    access_token = create_access_token(identity=user.email)

    # Attempt to create poll with missing fields
    response = client.post(
        "/create-poll",
        json={"question": ""},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["msg"] == "Missing required fields: question and options."

def test_vote_single_choice_success(client):
    # Register and login user
    client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    user = User.query.filter_by(email="testuser@example.com").first()
    user.is_admin = True
    db.session.commit()

    access_token_user = create_access_token(identity=user.email)

    # Create a poll
    response = client.post(
        "/create-poll",
        json={
            "question": "What's your favorite programming language?",
            "options": ["Python", "JavaScript", "C++"]
        },
        headers={"Authorization": f"Bearer {access_token_user}"}
    )
    poll = Poll.query.first()  # Fetch the poll
    assert poll is not None

    # Fetch an option
    option = Option.query.filter_by(poll_id=poll.id).first()
    assert option is not None

    # Cast a vote
    vote_response = client.post(
        "/vote",
        json={"poll_id": poll.id, "option_id": option.id},
        headers={"Authorization": f"Bearer {access_token_user}"}
    )
    assert vote_response.status_code == 201
    assert vote_response.get_json()["msg"] == "Vote cast successfully"

def test_vote_single_choice_revote(client):
    # Register and login user
    client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    user = User.query.filter_by(email="testuser@example.com").first()
    user.is_admin = True
    db.session.commit()

    access_token_user = create_access_token(identity=user.email)

    # Create a poll
    response = client.post(
        "/create-poll",
        json={
            "question": "What's your favorite programming language?",
            "options": ["Python", "JavaScript", "C++"]
        },
        headers={"Authorization": f"Bearer {access_token_user}"}
    )
    poll = Poll.query.first()  # Fetch the poll
    assert poll is not None

    # Fetch an option
    option = Option.query.filter_by(poll_id=poll.id).first()
    assert option is not None

    # Cast a vote
    vote_response = client.post(
        "/vote",
        json={"poll_id": poll.id, "option_id": option.id},
        headers={"Authorization": f"Bearer {access_token_user}"}
    )
    assert vote_response.status_code == 201
    assert vote_response.get_json()["msg"] == "Vote cast successfully"

    # Cast a vote
    vote_response = client.post(
        "/vote",
        json={"poll_id": poll.id, "option_id": option.id},
        headers={"Authorization": f"Bearer {access_token_user}"}
    )
    assert vote_response.status_code == 400 # expected
    assert vote_response.get_json()["msg"] == "User has already voted on this poll"

def test_edit_poll_success(client):
    # Register and login admin
    client.post("/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    user = User.query.filter_by(email="admin@example.com").first()
    user.is_admin = True
    db.session.commit()
    access_token = create_access_token(identity=user.email)

    # Create poll
    client.post(
        "/create-poll",
        json={
            "question": "Favorite programming language?",
            "options": ["Python", "JavaScript", "C++"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    poll = Poll.query.first()

    # Edit the poll
    response = client.patch(
        f"/edit-poll/{poll.id}",
        json={
            "question": "Most used programming language?",
            "options": ["Python", "JavaScript"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Poll updated successfully"

def test_edit_poll_not_admin(client):
    # Register and login non-admin user
    client.post("/register", json={
        "username": "user",
        "email": "user@example.com",
        "password": "password123"
    })
    access_token = create_access_token(identity="user@example.com")

    # Attempt to edit poll
    response = client.patch(
        "/edit-poll/1",
        json={
            "question": "Invalid attempt?",
            "options": ["Yes", "No"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data["msg"] == "Unauthorized"

def test_edit_poll_with_votes(client):
    # Register and login admin
    client.post("/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    user = User.query.filter_by(email="admin@example.com").first()
    user.is_admin = True
    db.session.commit()
    access_token = create_access_token(identity=user.email)

    # Create poll and cast a vote
    client.post(
        "/create-poll",
        json={
            "question": "Favorite programming language?",
            "options": ["Python", "JavaScript", "C++"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    poll = Poll.query.first()
    option = Option.query.filter_by(poll_id=poll.id).first()
    client.post(
        "/vote",
        json={"poll_id": poll.id, "option_id": option.id},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Attempt to edit the poll
    response = client.patch(
        f"/edit-poll/{poll.id}",
        json={
            "question": "Updated question?",
            "options": ["Option 1", "Option 2"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["msg"] == "Cannot edit poll after votes have been cast"

def test_get_poll_results_success(client):
    # Register and login admin
    client.post("/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    user = User.query.filter_by(email="admin@example.com").first()
    user.is_admin = True
    db.session.commit()
    access_token = create_access_token(identity=user.email)

    # Create poll and cast votes
    client.post(
        "/create-poll",
        json={
            "question": "Favorite programming language?",
            "options": ["Python", "JavaScript", "C++"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    poll = Poll.query.first()
    option = Option.query.filter_by(poll_id=poll.id).first()
    client.post(
        "/vote",
        json={"poll_id": poll.id, "option_id": option.id},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Fetch results
    response = client.get(
        f"/poll-results/{poll.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["poll_id"] == poll.id
    assert data["question"] == "Favorite programming language?"
    assert len(data["results"]) == 3

def test_get_poll_results_not_admin(client):
    # Register and login non-admin user
    client.post("/register", json={
        "username": "user",
        "email": "user@example.com",
        "password": "password123"
    })
    access_token = create_access_token(identity="user@example.com")

    # Attempt to fetch results
    response = client.get(
        "/poll-results/1",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 403
    data = response.get_json()
    assert data["msg"] == "Unauthorized"

def test_get_poll_results_poll_not_found(client):
    # Register and login admin
    client.post("/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    user = User.query.filter_by(email="admin@example.com").first()
    user.is_admin = True
    db.session.commit()
    access_token = create_access_token(identity=user.email)

    # Attempt to fetch results for non-existent poll
    response = client.get(
        "/poll-results/999",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 404
    data = response.get_json()
    assert data["msg"] == "Poll not found"


