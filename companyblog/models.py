from companyblog import db,login_manager,app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user,LoginManager
from flask_admin import Admin
from flask import session, redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
import time
from flask_admin import Admin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# login = LoginManager(app)
#
#


#
# @login.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)





followers = db.Table(
    'followers',
    db.Column('follower_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('followed_id',db.Integer,db.ForeignKey('users.id'))
    )



class User(db.Model,UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.Text,nullable=False,default='https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/default_profile.png')
    email = db.Column(db.String(140),unique=True,index=True)
    username = db.Column(db.String(140),unique=True,index=True)
    name = db.Column(db.String(140),nullable=True)
    club_name = db.Column(db.String(140),nullable=True)
    event = db.Column(db.Text,nullable=True)
    facebook = db.Column(db.String(140), nullable=True)
    twitter = db.Column(db.String(140), nullable=True)
    instagram = db.Column(db.String(140),nullable=True)
    info = db.Column(db.Text,nullable=True)
    url = db.Column(db.String(140),nullable=True)
    university = db.Column(db.Integer,nullable=False)
    type = db.Column(db.Integer,nullable=False)
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    posts = db.relationship('BlogPost',backref='author',lazy=True)
    comments = db.relationship('Comment',backref='poster',lazy=True)
    followed = db.relationship(
    'User',secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers',lazy='dynamic'),lazy='dynamic')

    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user',lazy='dynamic')


    def __init__(self,email,username,name,club_name,type,university,password,email_confirmation_sent_on=None):
        self.email = email
        self.username = username
        self.name = name
        self.club_name = club_name
        self.type = type
        self.university = university
        self.password_hash = generate_password_hash(password)
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.authenticated = False

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def is_authenticated(self):
        return self.authenticated

    def __repr__(self):
        return f"Username {self.username}"

    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = BlogPost.query.join(
            followers,(followers.c.followed_id == BlogPost.user_id)).filter(
                followers.c.follower_id == self.id)
        return followed.union(self.posts).order_by(BlogPost.date.desc())

    def like_post(self,blog_post):
        if not self.has_liked_post(blog_post):
            like = PostLike(user_id=self.id,post_id=blog_post.id)
            db.session.add(like)

    def unlike_post(self,blog_post):
        if self.has_liked_post(blog_post):
            PostLike.query.filter_by(
            user_id=self.id,
            post_id=blog_post.id).delete()

    def has_liked_post(self,blog_post):
        return PostLike.query.filter(
        PostLike.user_id == self.id,
        PostLike.post_id == blog_post.id).count() > 0



class BlogPost(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    event_image = db.Column(db.Text,nullable=False,default='https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/default_profile.png')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    event_date = db.Column(db.DateTime,default=datetime.utcnow)
    event_time = db.Column(db.Time,default=datetime.utcnow)
    organizer = db.Column(db.String(140),nullable=False)
    place = db.Column(db.String(140),nullable=False)
    entry = db.Column(db.Text,nullable=False)
    way = db.Column(db.Text,nullable=False)
    cost = db.Column(db.String(140),nullable=False)
    contact = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)

    comments = db.relationship('Comment',backref='title',lazy=True)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')


    def __init__(self,organizer,place,title,event_date,event_time,entry,text,way,user_id,cost,event_image,contact):
        self.title = title
        self.text = text
        self.event_date = event_date
        self.event_time = event_time
        self.user_id = user_id
        self.event_image = event_image
        self.organizer = organizer
        self.place = place
        self.entry = entry
        self.way = way
        self.cost = cost
        self.contact = contact

        def __repr__(self):
            return f"Post ID: {self.id} --Date:{self.date} --- {self.title}"

class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))


class Comment(db.Model):
    blog_post = db.relationship(BlogPost)
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140),nullable=False)
    timestamp = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    post_id = db.Column(db.Integer,db.ForeignKey('blog_post.id'),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __init__(self,body,post_id,user_id):
        self.body = body
        self.post_id = post_id
        self.user_id = user_id




        def __repr__(self):
            return f"Post ID: {self.id}---userid:{self.user_id} --Date:{self.timestamp}---{self.body}"

def init():
    db.create_all()

from companyblog.models import User,BlogPost

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == app.config['ADMIN_NAME']:
            return True
        return False


admin = Admin(app)
admin.add_view(MyModelView(User,db.session))
admin.add_view(MyModelView(BlogPost,db.session))
