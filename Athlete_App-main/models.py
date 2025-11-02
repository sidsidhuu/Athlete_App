from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    profile_photo = db.Column(db.String(200))  # Path to profile photo
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True)
    stories = db.relationship('Story', backref='author', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    # Follow relationships
    following = db.relationship('Follow',
                               foreign_keys='Follow.follower_id',
                               backref='follower_user', lazy='dynamic')
    followers = db.relationship('Follow',
                               foreign_keys='Follow.followed_id',
                               backref='followed_user', lazy='dynamic')

    notifications = db.relationship('Notification', foreign_keys='Notification.user_id', backref='user', lazy=True)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id'),)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    video_path = db.Column(db.String(200))  # Path to uploaded video
    activity_type = db.Column(db.String(50))  # e.g., 'running', 'pushups', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    media_path = db.Column(db.String(200))  # Path to photo/video
    media_type = db.Column(db.String(10))  # 'photo' or 'video'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    views = db.relationship('StoryView', backref='story', lazy=True, cascade='all, delete-orphan')

class StoryView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    viewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id'),)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'follow', 'like', 'comment', 'story_view'
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Optional references
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))

    from_user = db.relationship('User', foreign_keys=[from_user_id])
    post = db.relationship('Post', foreign_keys=[post_id])
    story = db.relationship('Story', foreign_keys=[story_id])

def init_db(app):
    db.init_app(app)
    # Don't create tables here - let Flask-Migrate handle it
