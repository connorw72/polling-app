from app import app, db
from models import User, Poll, Option, Vote
from flask import request, jsonify 
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


# registration 
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() # sends user data with request

    # extract user data
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # check if required field is missing 
    if not username or not email or not password:
        return jsonify({"msg":"Missing required fields"}), 400
    
    # checks if there is a user with the email in the dtabase
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Email already in use"}), 400
    
    # hash password
    hashed_password = generate_password_hash(password)

    # passes all checks, create new user object
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

# login 
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # extract data
    email = data.get("email")
    password = data.get("password")
    

    # if missing required data
    if not email or not password:
        return jsonify({"msg":"Missing required fields"}), 400
    
    #checks that email exists and password is valid
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg":"Invalid email"}), 401
    
    #verify password
    if not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid password"}), 401

    # creates Json web token if email and password are valid
    access_token = create_access_token(identity=user.email)
    # success, return JWT
    return jsonify({"msg": "Login successful", "access_token": access_token, "is_admin": user.is_admin}), 200

# create poll 
@app.route('/create-poll', methods=['POST'])
@jwt_required()
def create_poll():
    current_user_email = get_jwt_identity()

    # user from database
    user = User.query.filter_by(email=current_user_email).first()

    # If not admin cannot create
    if not user or not user.is_admin:
        return jsonify({"msg": "You are not authorized to create polls"}), 403
    
    # parse data
    data = request.get_json()
    question = data.get('question')
    options = data.get('options')

    if not question or not options or not isinstance(options, list) or len(options) < 2:
        return jsonify({"msg":"Missing required fields: question and options."}), 400

    # poll object
    new_poll = Poll(
        question=question,
        user_id=user.id
    )

    # save poll to db
    db.session.add(new_poll)
    db.session.commit()

    # add options
    created_options = []
    for option_text in options:
        option = Option(text=option_text, poll_id=new_poll.id)
        db.session.add(option)
        created_options.append({
            "id": option.id,  # Include the option ID in the response
            "text": option.text
        })

    db.session.commit()

    # success response
    return jsonify({
        "msg": "Poll created successfully",
        "poll": {
            "id": new_poll.id,
            "question": new_poll.question,
            "created_at": new_poll.created_at,
            "user_id": new_poll.user_id,
            "options": created_options  # Return both ID and text for each option
        }
    }), 201

# vote
@app.route("/vote/<int:poll_id>", methods=["POST"])
@jwt_required()
def vote(poll_id):
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return {"msg": "User not found"}, 404

    data = request.get_json()
    option_id = data.get("optionId")

    poll = Poll.query.get(poll_id)
    if not poll:
        return {"msg": "Poll not found"}, 404

    option = Option.query.filter_by(id=option_id, poll_id=poll_id).first()
    if not option:
        return {"msg": "Option not found for this poll"}, 404

    # Ensure the user has not already voted on this poll
    existing_vote = Vote.query.filter_by(poll_id=poll_id, user_id=user.id).first()
    if existing_vote:
        return {"msg": "User has already voted on this poll"}, 400

    # Create a new vote
    vote = Vote(poll_id=poll_id, user_id=user.id, option_id=option_id)
    option.votes += 1  # Increment the vote count for the option
    db.session.add(vote)
    db.session.commit()

    return {"msg": "Vote cast successfully"}, 201

@app.route('/polls', methods=["GET"])
@jwt_required()
def get_polls():
    identity = get_jwt_identity()
    current_user = User.query.filter_by(email=identity).first()

    polls = Poll.query.all()
    results = []
    for poll in polls:
        poll_data = {
            "id": poll.id,
            "question": poll.question,
            "options": []
        }
        for option in poll.options:
            poll_data["options"].append({
                "id": option.id,
                "text": option.text,
                "votes": option.votes
            })
        results.append(poll_data)
    return jsonify(results), 200

# edit poll
@app.route('/edit-poll/<int:poll_id>', methods=['PATCH'])
@jwt_required()
def edit_poll(poll_id):
    # admin user
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user or not user.is_admin:
        return jsonify({"msg": "Unauthorized"}), 403
    
    # fetch poll
    poll = Poll.query.get(poll_id)
    if not poll:
        return jsonify({"msg": "Poll not found"}), 404
    
    # check if votes have been cast
    if Vote.query.filter_by(poll_id=poll.id).first():
        return jsonify({"msg": "Cannot edit poll after votes have been cast"}), 400
    
    # update poll
    data = request.json
    question = data.get("question")
    options = data.get("options")
    
    if question:
        poll.question = question
    if options: 
        # clear and add new options
        Option.query.filter_by(poll_id=poll.id).delete()
        for option_text in options:
            new_option = Option(text=option_text, poll_id=poll.id)
            db.session.add(new_option)

    db.session.commit()
    return jsonify({"msg":"Poll updated successfully"}), 200

@app.route('/delete-poll/<int:poll_id>', methods=['DELETE'])
@jwt_required()
@cross_origin(supports_credentials=True)
def delete_poll(poll_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user or not user.is_admin:
        return jsonify({"msg": "unauthorized"}), 403

    poll = Poll.query.get(poll_id)
    if not poll:
        return jsonify({"msg": "Poll not found"}), 404

    db.session.delete(poll)
    db.session.commit()
    return jsonify({"msg": "poll deleted"}), 200


# retrieve poll results
@app.route('/poll-results/<int:poll_id>', methods=['GET'])
@jwt_required()
def get_poll_results(poll_id):
    # admin only
    current_user_email=get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user or not user.is_admin:
        return jsonify({"msg": "Unauthorized"}), 403
    
    # fetch poll
    poll = Poll.query.get(poll_id)
    if not poll:
        return jsonify({"msg":"Poll not found"}), 404
    
    # fetch results
    options = Option.query.filter_by(poll_id=poll.id).all()
    results = [
        {"option": option.text, "votes": option.votes}
        for option in options
    ]
    return jsonify({
        "poll_id":poll.id,
        "question":poll.question,
        "results":results
    }), 200


#view user list
@app.route("/admin/users", methods=["GET", "OPTIONS"])
@cross_origin(supports_credentials=True)
@jwt_required()
def get_users():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user or not user.is_admin:
        return jsonify({"msg": "Unauthorized"}), 403

    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "email": u.email,
        "username": u.username,
        "is_admin": u.is_admin
    } for u in users]), 200
