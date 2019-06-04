

from datetime import datetime
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from companyblog import db,app
from companyblog.models import User,BlogPost
from companyblog.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from companyblog.users.picture_handler import add_profile_pic
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from companyblog import mail


users = Blueprint('users',__name__)

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    # msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_url = url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url)

    send_email('KomaNeco確認メール', [user_email], html)

@users.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


#register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data,
                    university=form.university.data,
                    type=form.type.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        login_user(user)
        send_confirmation_email(user.email)
        flash('この度はご登録ありがとうございます。{}宛に確認メールをお送りいたしましたので、本登録の完了を宜しくお願いいたします'.format(user.email), 'success')
        # send_email('Registration',
        #                    ['1mg5326d@komazawa-u.ac.jp'],
        #                    'Thanks for registering with Kennedy Family Recipes!',
        #                    '<h3>Thanks for registering with Kennedy Family Recipes!</h3>')
        # flash('Thanks for registering!  Please check your email to confirm your email address.', 'success')
        # msg = Message(subject='テスト',
        #                       body='ご登録ありがとうございます。',
        #                       recipients=['1mg5326d@komazawa-u.ac.jp'])
        # mail.send(msg)
        # flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)

#login_view

@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.email_confirmed == True:
            if user.check_password(form.password.data) and user is not None:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('{}さん　KomaNecoへようこそ！'.format(user.username))

                next = request.args.get('next')

                if next == None or not next[0]=='/':
                    next = url_for('core.index')

                    return redirect(next)
        else:
            flash('アカウント情報が不正です。本登録を完了させてください。', 'error')
            return redirect(url_for('users.login'))

    return render_template('login.html',form=form)




@users.route("/logout")
def logout():
    logout_user()
    flash('ログアウトしました')
    return redirect(url_for("core.index"))




# account (update userform)

@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:

            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.type = form.type.data
        current_user.info = form.info.data
        current_user.university = form.university.data
        current_user.url = form.url.data
        current_user.twitter = form.twitter.data
        current_user.facebook = form.facebook.data
        current_user.instagram = form.instagram.data
        db.session.commit()
        flash('アカウント情報を更新しました')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.info.data = current_user.info
        form.url.data = current_user.url
        form.type.data = current_user.type
        form.twitter.data = current_user.twitter
        form.facebook.data = current_user.facebook
        form.instagram.data = current_user.instagram



    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)

@users.route("/all")
def all():
    page = request.args.get('page',1,type=int)
    sports = User.query.filter(User.type==2)
    cultures = User.query.filter(User.type==3)
    others = User.query.filter(User.type==4)
    return render_template('all.html',sports=sports,cultures=cultures,others=others)

# @users.route('/follow/<username>')
# @login_required
# def follow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         return redirect(url_for('core.index'))
#     if user == current_user:
#         return redirect(url_for('users.user_posts',username=username))
#         # return render_template('user_blog_posts.html',username=username,user=user)
#     current_user.follow(user)
#     db.session.commit()
#     flash('{} さんをフォローしました！'.format(username))
#     return redirect(url_for('users.user_posts',username=username))
#
#
#     # return render_template('user_blog_posts.html',username=username,user=user)
#
# @users.route('/unfollow/<username>')
# @login_required
# def unfollow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         return redirect(url_for('core.index'))
#     if user == current_user:
#         return redirect(url_for('users.user_posts',username=username))
#     current_user.unfollow(user)
#     db.session.commit()
#     flash('{} さんをフォロー解除しました！'.format(username))
#     return redirect(url_for('users.user_posts',username=username))


@users.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        flash('トークンが有効ではありません。', 'error')
        return redirect(url_for('users.login'))

    user = User.query.filter_by(email=email).first()

    if user.email_confirmed:
        flash('このアカウントは既に本登録完了していますので、ログインしてください。', 'info')
        return redirect(url_for('users.login'))
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('ようこそ！KomaNeco！メール認証ありがとうございます。')

    return redirect(url_for('core.index'))

    # return render_template('user_blog_posts.html',username=username)
