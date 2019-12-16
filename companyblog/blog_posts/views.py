from flask import render_template,url_for,flash,redirect,request,Blueprint,jsonify
from flask_login import current_user,login_required
from companyblog import db,app
from companyblog.models import BlogPost,Comment,User,PostLike
from companyblog.blog_posts.forms import BlogPostForm,CommentForm,ImageForm
from companyblog.blog_posts.image_handler import add_image_pic
import boto3

blog_posts = Blueprint('blog_posts',__name__)

s3 = boto3.client(
    's3',
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
    )

#

# @blog_posts.route('/files')
# def files():
#     s3_resource = boto3.resource('s3')
#     my_bucket = s3_resource.Bucket(app.config['AWS_BUCKET'])
#     summaries = my_bucket.objects.all()
#     url = s3.generate_presigned_url('get_object',
#                                 Params={
#                                     'Bucket': app.config['AWS_BUCKET'],
#                                     'Key': '190614_155331.jpg',
#                                 })
#     return render_template('file.html',my_bucket=my_bucket,files=summaries,url=url)

# @blog_posts.route('/upload',methods=["POST"])
# def upload():
#     if request.method == "POST":
#         file = request.files['file']
#         # file = request.files['file']
#         newfile = add_image_pic(file)
#         # s3_resource = boto3.resource('s3')
#         # my_bucket = s3_resource.Bucket(app.config['S3_BUCKET'])
#         # my_bucket.Object(newfile).put(Body=file)
#         return jsonify({'file': newfile})


#create
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        if form.image.data:
            image = add_image_pic(form.image.data)
            s3_resource = boto3.resource('s3')
            my_bucket = s3_resource.Bucket(app.config['AWS_BUCKET'])
            my_bucket.Object(image).put(Body=form.image.data)
            test = 'https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/{}'
            images = test.format(image)
            blog_post = BlogPost(title=form.title.data,
                                event_date=form.event_date.data,
                                event_time=form.event_time.data,
                                text=form.text.data,
                                organizer=form.organizer.data,
                                place=form.place.data,
                                entry=form.entry.data,
                                way=form.way.data,
                                cost=form.cost.data,
                                contact=form.contact.data,
                                user_id=current_user.id,
                                event_image=images)
        else:
            blog_post = BlogPost(title=form.title.data,
                                event_date=form.event_date.data,
                                event_time=form.event_time.data,
                                text=form.text.data,
                                organizer=form.organizer.data,
                                place=form.place.data,
                                entry=form.entry.data,
                                way=form.way.data,
                                cost=form.cost.data,
                                contact=form.contact.data,
                                user_id=current_user.id,
                                event_image='https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/default_profile.png')



        db.session.add(blog_post)
        db.session.commit()
        flash("投稿を作成しました！")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form,api=str(app.config['GOOGLE_MAP_API']))


# @blog_posts.route('/like/<int:blog_post_id>/<action>')
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
#



#Blog Post (view)
@blog_posts.route('/posts/<int:blog_post_id>',methods=['GET','POST'])
# @login_required
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    comments = Comment.query.filter_by(post_id=blog_post_id)
    # comments = Comment.query.get_or_404(comment)


    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(body=form.body.data,post_id=blog_post.id,user_id=current_user.id)

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('blog_posts.blog_post',blog_post_id = blog_post.id))
        # return redirect(url_for('core.index'))


    return render_template('blog_post.html',title=blog_post.title,
                                date=blog_post.date,post=blog_post,form=form,comments=comments,url=request.base_url,api=str(app.config['GOOGLE_MAP_API']))






#update
@blog_posts.route('/posts/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():

       

        if form.image.data:
            image = add_image_pic(form.image.data)
            s3_resource = boto3.resource('s3')
            my_bucket = s3_resource.Bucket(app.config['AWS_BUCKET'])
            my_bucket.Object(image).put(Body=form.image.data)
            test = 'https://{}.s3-ap-northeast-1.amazonaws.com/{}'
            images = test.format(app.config['AWS_BUCKET'],image)
            blog_post.event_image = images

        blog_post.title  = form.title.data
        blog_post.text  = form.text.data
        blog_post.event_date = form.event_date.data
        blog_post.event_time = form.event_time.data
        blog_post.organizer  = form.organizer.data
        blog_post.place  = form.place.data
        blog_post.entry  = form.entry.data
        blog_post.way  = form.way.data
        blog_post.cost  = form.cost.data
        blog_post.contact  = form.contact.data

        


        db.session.commit()
        flash("投稿を更新しました。")
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        form.event_date.data = blog_post.event_date
        form.event_time.data = blog_post.event_time
        form.organizer.data = blog_post.organizer
        form.place.data = blog_post.place
        form.entry.data = blog_post.entry
        form.way.data = blog_post.way
        form.cost.data = blog_post.cost
        form.contact.data = blog_post.contact
       

        post_image = blog_post.event_image


    return render_template('create_post.html',title="Updating",form=form,post_image=post_image)





#delete

@blog_posts.route('/posts/<int:blog_post_id>/delete',methods=["POST"])
@login_required

def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('投稿を削除しました。')
    return redirect(url_for('core.index'))
