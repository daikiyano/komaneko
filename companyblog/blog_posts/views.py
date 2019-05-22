from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import current_user,login_required
from companyblog import db
from companyblog.models import BlogPost,Comment,User,PostLike
from companyblog.blog_posts.forms import BlogPostForm,CommentForm
from companyblog.blog_posts.image_handler import add_image_pic

blog_posts = Blueprint('blog_posts',__name__)

#create
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        # if form.image.data:

            # username = current_user.username
        # pic = add_image_pic(form.image.data)
        # current_user.event_image = pic
        # db.session.commit()

        blog_post = BlogPost(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id,
                            event_image=add_image_pic(form.image.data))

        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)


@blog_posts.route('/like/<int:blog_post_id>/<action>')
@login_required

def like_action(blog_post_id,action):
    blog_post = BlogPost.query.filter_by(id=blog_post_id).first_or_404()
    if action == 'like':
        current_user.like_post(blog_post)
        db.session.commit()

    if action == 'unlike':
        current_user.unlike_post(blog_post)
        db.session.commit()
    return redirect(request.referrer)




#Blog Post (view)
@blog_posts.route('/<int:blog_post_id>',methods=['GET','POST'])
@login_required
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
                                date=blog_post.date,post=blog_post,form=form,comments=comments)






#update
@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        if form.image.data:
            blog_post.event_image = add_image_pic(form.image.data)

        blog_post.title  = form.title.data
        blog_post.text  = form.text.data
        db.session.commit()
        flash("Blog Post Updated")
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        form.image.data = blog_post.event_image

    return render_template('create_post.html',title="Updating",form=form)





#delete

@blog_posts.route('/<int:blog_post_id>/delete',methods=["POST"])
@login_required

def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Post blog delete')
    return redirect(url_for('core.index'))


#comment delete

@blog_posts.route('/comment/<int:blog_comment_id>/delete',methods=["POST"])
@login_required

def delete_comment(blog_comment_id):

    # comment = Comment.query.get_or_404(blog_comment_id)
    comment = Comment.query.get_or_404(blog_comment_id)
    # comment = Comment.query.filter_by(id=blog_comment_id).first_or_404()
    # comment = Comment.query.get(id=blog_comment_id)
    if comment.poster != current_user:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('comment blog delete')
    return redirect(url_for('core.index'))



# comment = Coment.query.filter_by(id=blog_comment_id).first_or_404()
# if action == 'like':
#     current_user.delete_comment(comment)
#     db.session.commit()
#     return redirect(request.referrer)
