from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import current_user,login_required
from companyblog import db
from companyblog.models import BlogPost,Comment
from companyblog.blog_posts.forms import BlogPostForm,CommentForm

blog_posts = Blueprint('blog_posts',__name__)

#create
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)




#Blog Post (view)
@blog_posts.route('/<int:blog_post_id>',methods=['GET','POST'])
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    comments = Comment.query.filter_by(post_id=blog_post_id)

    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(body=form.body.data,post_id=blog_post.id)

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

        blog_post.title  = form.title.data
        blog_post.text  = form.text.data
        db.session.commit()
        flash("Blog Post Updated")
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

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
