# models.py
from datetime import datetime, timezone
from app import db
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique user ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # unique, required username
    email = db.Column(db.String(120), unique=True, nullable=False)  # unique, required email
    password = db.Column(db.String(200), nullable=False)  # required password
    is_admin = db.Column(db.Boolean, default=False) # true or false admin
    polls = db.relationship('Poll', backref='creator', lazy=True) # relationship to polls

    def __repr__(self):
        return f'<User {self.email}>'

# Poll model
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique poll ID
    question = db.Column(db.String(200), nullable=False)  # required poll question
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  # date/time question is created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # foreign key to user
    is_multiple_choice = db.Column(db.Boolean, default=False) # flag if multiple choice

    def __repr__(self):
        return f'<Poll {self.question}>'

    # option relationship
    options = db.relationship("Option", backref="poll", lazy=True, cascade="all, delete")
    # votes relationship
    votes = db.relationship('Vote', backref='poll', lazy=True, cascade= "all, delete") 

# Options model
class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique option ID
    text = db.Column(db.String(200), nullable=False)  # text for the option
    votes = db.Column(db.Integer, default=0)  # Vote count
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)  # Key for poll

# Vote model
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True) # unique vote ID
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False) # poll key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # user key
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False) # option key
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc)) # when the vote was cast 

    __table_args__ = (
        db.UniqueConstraint('poll_id', 'user_id', name='unique_user_vote_per_poll'), # user can only vote once per poll
    )
