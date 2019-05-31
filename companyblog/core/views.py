from flask import Flask, render_template,url_for,flash,redirect,request,Blueprint,jsonify
from datetime import datetime
from companyblog.models import BlogPost,PostLike,User
from flask_login import current_user,login_required
from companyblog import db



core = Blueprint('core',__name__)

@core.route('/',methods=['GET','POST'])

def index():

    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        output = firstname + lastname
        if firstname and lastname:
            return jsonify({'output':'名前は:' + output + 'です'})
        return jsonify({'error' : 'Missing data!'})


    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.filter(BlogPost.event_date >= datetime.utcnow()).order_by(BlogPost.event_date.desc()).paginate(page=page,per_page=5)
    return render_template('index.html',blog_posts=blog_posts)

@core.route('/condition',methods=['GET','POST'])
@login_required

def like_action():
    blog_post = BlogPost.query.filter_by(id=request.form['id']).first_or_404()
    if request.method == "POST":
        if current_user.has_liked_post(blog_post):
            current_user.unlike_post(blog_post)
            db.session.commit()
            blog_post = BlogPost.query.filter_by(id=request.form['id']).first_or_404()
            return jsonify({'condition': 'like','count': blog_post.likes.count()})
        else:
            current_user.like_post(blog_post)
            db.session.commit()
            blog_post = BlogPost.query.filter_by(id=request.form['id']).first_or_404()

            return jsonify({'condition': 'unlike','count': blog_post.likes.count()})






# @core.route('/like/<int:blog_post_id>/<action>')
# @login_required
#
# def like_action(blog_post_id,action):
#     blog_post = BlogPost.query.filter_by(id=blog_post_id).first_or_404()
#     if action == 'like':
#         current_user.like_post(blog_post)
#         db.session.commit()
#
#     if action == 'unlike':
#         current_user.unlike_post(blog_post)
#         db.session.commit()
#     return redirect(request.referrer)




@core.route('/info')
def info():
    return render_template('info.html')
