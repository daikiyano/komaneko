

from datetime import datetime
from flask import render_template,url_for,flash,redirect,request,Blueprint,jsonify
from flask_login import login_user,current_user,logout_user,login_required
from companyblog import db,app
from companyblog.models import User,BlogPost,PostLike
from companyblog.users.forms import RegistrationForm,LoginForm,UpdateUserForm,SignupForm,EmailForm
from companyblog.users.picture_handler import add_profile_pic
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from threading import Thread
from flask_mail import Message
from companyblog import mail
from PIL import Image
import random
import boto3
import base64
from io import BytesIO


s3 = boto3.client(
    's3',
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
    )

users = Blueprint('users',__name__)

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    # msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()

def send_confirmation_email(user_email,username):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_url = url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url,username=username)

    send_email('KomaNeco仮登録完了メール', [user_email], html)

def send_login_email(user_email,username):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    confirm_url = url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'magic_mail.html',
        confirm_url=confirm_url,username=username)

    send_email('KOMANEKO メール認証によるログインを受け付けました', [user_email], html)


def change_confirmation_email(user_email,username):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_url = url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'change_email_confirmation.html',
        confirm_url=confirm_url,username=username)

    send_email('KOMANEKOメールアドレス変更完了のお願い', [user_email], html)


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
        try:
            user = User(email=form.email.data,
                        username=form.username.data,
                        name=form.name.data,
                        club_name=form.club_name.data,
                        university=form.university.data,
                        type=form.type.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            send_confirmation_email(user.email,user.username)
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
        except IntegrityError:
            db.session.rollback()
            flash('エラーが発生しました。')
    return render_template('register.html',form=form)

@users.route('/signup',methods=['GET','POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User(email=form.email.data,
                        username=form.username.data,
                        name=form.club_name.data,
                        club_name=form.club_name.data,
                        university=form.university.data,
                        type=form.type.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()
            send_confirmation_email(user.email,user.username)
            flash('。{}宛に確認メールをお送りいたしましたので、本登録を完了させてください。'.format(user.email), 'success')
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
        except IntegrityError:
            db.session.rollback()
            flash('エラーが発生しました。')
    return render_template('signup.html',form=form)

#login_view

@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.email_confirmed == True:
            # if user.check_password(form.password.data) and user is not None:
            #     user.authenticated = True
            #     db.session.add(user)
            #     db.session.commit()
            #     login_user(user)
            send_login_email(user.email,user.username)
            flash('{}宛に確認メールをお送りしましたので、ご確認ください。'.format(user.email))
            return redirect(url_for('core.index'))
               
                # return redirect(url_for('core.index'))
            # next = request.args.get('next')
            # if next == None or not next[0]=='/':
            #     next = url_for('core.index')
            #     flash('ログインしてください')
            #     return redirect(next)
        else:
            flash('アカウント情報が不正です。本登録を完了させてください。', 'error')
            return redirect(url_for('users.login'))

    return render_template('login.html',form=form)




@users.route("/logout")
def logout():
    logout_user()
    flash('ログアウトしました')
    return redirect(url_for("core.index"))



@users.route('/image',methods=['POST'])
@login_required
def image():
    # if request.method == "GET":
    if request.method == 'POST': 
        # print(request.form['image'])
        enc_data = request.form['image']
        # enc_data = add_profile_pic(request.form['image'])
        dec_data = base64.b64decode(enc_data.split(',')[1]) # 環境依存の様(","で区切って本体をdecode)
        dec_img  = Image.open(BytesIO(dec_data))
        print(BytesIO(dec_data))
        print(dec_img)
        image = add_profile_pic(dec_img)
        image = "{}png".format(image)
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(app.config['AWS_BUCKET'])
        my_bucket.Object(image).put(Body=BytesIO(dec_data))
        test = 'https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/{}'
        images = test.format(image)
        print(images)
        current_user.profile_image = images
        db.session.commit()
        return jsonify({'image': images})


@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    likes = PostLike.query.filter(PostLike.user_id==current_user.id)
    
    form = UpdateUserForm()
    if form.validate_on_submit():

        if current_user.type == 1 and form.type.data != 1:
            flash('個人から団体アカウントに変更はできません')
            return redirect(url_for('users.account'))
        elif current_user.type > 1 and form.type.data == 1:
            flash('団体から個人に変更はできません')
            return redirect(url_for('users.account'))
        # if form.picture.data:
        #     print(form.picture.data)
        #     image = add_profile_pic(form.picture.data)
        #     s3_resource = boto3.resource('s3')
        #     my_bucket = s3_resource.Bucket(app.config['AWS_BUCKET'])
        #     my_bucket.Object(image).put(Body=form.picture.data)
        #     test = 'https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/{}'
        #     images = test.format(image)

            

        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.event = form.event.data
        current_user.club_name = form.club_name.data
        current_user.email = current_user.email
        current_user.type = form.type.data
        current_user.info = form.info.data
        current_user.university = form.university.data
        current_user.url = form.url.data
        current_user.club_number = form.club_number.data
        current_user.club_place = form.club_place.data
        current_user.club_active = form.club_active.data
        current_user.money = form.money.data
        current_user.twitter = form.twitter.data
        current_user.facebook = form.facebook.data
        current_user.instagram = form.instagram.data
        db.session.commit()
        flash('アカウント情報を更新しました')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.club_name.data = current_user.club_name
        form.university.data = current_user.university
        form.event.data = current_user.event
        form.email.data = current_user.email
        form.info.data = current_user.info
        form.url.data = current_user.url
        form.club_number.data = current_user.club_number
        form.club_place.data = current_user.club_place
        form.club_active.data = current_user.club_active
        form.money.data = current_user.money
        form.type.data = current_user.type
        form.twitter.data = current_user.twitter
        form.facebook.data = current_user.facebook
        form.instagram.data = current_user.instagram




    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form,likes=likes)

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    users = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=users).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    likes = PostLike.query.filter(PostLike.user_id==users.id)


    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=users,urls=request.base_url,likes=likes)

@users.route("/all")
def all():
    page = request.args.get('page',1,type=int)
    # sports = User.query.filter(User.type==2)
    # cultures = User.query.filter(User.type==3)
    # others = User.query.filter(User.type==4)
    alls = User.query.filter(User.type > 1)
    return render_template('all.html',alls=alls)





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

# @users.route('/users/<int:user_id>/delete',method=["POST"])
# @login_required
#
# def delete_user(user_id):
#
#     user = User.query.get_or_404(user_id)
#
#     if user.id != current_user.id:
#         abort(403)
#
#     db.session.delete(user)
#     db.session.commit()


@users.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        flash('トークンが有効ではありません。', 'error')
        return redirect(url_for('users.login'))

    user = User.query.filter_by(email=email).first()

# if user doesn't exist
    if not user.email_confirmed:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('ようこそ！KOMANEKOへ！本登録していただきありがとうございます。')
        return redirect(url_for('core.index'))
    else:
#if user exist
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('ようこそ！KOMANEKOへ！メール認証ありがとうございます。')

    return redirect(url_for('core.index'))

@users.route('/email_change', methods=["GET", "POST"])
@login_required
def user_email_change():
    form = EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user_check = User.query.filter_by(email=form.email.data).first()
                if user_check is None:
                    user = current_user
                    user.email = form.email.data
                    user.email_confirmed = True
                    user.email_confirmed_on = None
                    user.email_confirmation_sent_on = datetime.now()
                    db.session.add(user)
                    db.session.commit()
                    change_confirmation_email(user.email,user.username)
                    flash('{}宛に確認メールをお送りいたしましたので、メールアドレスの変更を完了させてください'.format(user.email))
                    return redirect(url_for('users.account'))
                else:
                    flash('このメールアドレスは既に登録されています')
            except IntegrityError:
                flash('このメールアドレスは既に登録されています')
    return render_template('email_change.html', form=form)
