

from companyblog import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


followers = db.Table(
    'followers',
    db.Column('follower_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('followed_id',db.Integer,db.ForeignKey('users.id'))
    )



class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    info = db.Column(db.String(250))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
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


    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

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
    event_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    organizer = db.Column(db.String(140),nullable=False)
    place = db.Column(db.String(140),nullable=False)
    entry = db.Column(db.String(140),nullable=False)
    way = db.Column(db.String(140),nullable=False)
    cost = db.Column(db.String(140),nullable=False)
    contact = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)

    comments = db.relationship('Comment',backref='title',lazy=True)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')


    def __init__(self,organizer,place,title,entry,text,way,user_id,cost,event_image,contact):
        self.title = title
        self.text = text
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
