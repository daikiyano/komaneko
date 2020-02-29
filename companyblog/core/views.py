from flask import Flask, render_template,url_for,flash,redirect,request,Blueprint,jsonify
from datetime import datetime
from companyblog.models import BlogPost,PostLike,User
from flask_login import current_user,login_required
from companyblog import db,app


import json
import googlemaps
import pprint # list型やdict型を見やすくprintするライブラリ



core = Blueprint('core',__name__)


###################################################
#######Top Page ################################
###################################################
@core.route('/',methods=['GET','POST'])

def index():

    
#############ajax test########################
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        output = firstname + lastname
        if firstname and lastname:
            return jsonify({'output':'名前は:' + output + 'です'})
        return jsonify({'error' : 'Missing data!'})


    page = request.args.get('page',1,type=int)
    #新着順
    all_posts = BlogPost.query.filter(BlogPost.event_date >= datetime.utcnow()).order_by(BlogPost.date.desc()).paginate(page=page,per_page=10)
    #直近開催イベント
    blog_posts = BlogPost.query.filter(BlogPost.event_date >= datetime.utcnow()).order_by(BlogPost.event_date.asc()).paginate(page=page,per_page=10)

    past_posts = BlogPost.query.filter(BlogPost.event_date <= datetime.utcnow()).order_by(BlogPost.event_date.desc())

    alls = User.query.filter(User.type > 1)
    return render_template('index.html',blog_posts=blog_posts,all_posts=all_posts,url=request.base_url,alls=alls,past_posts=past_posts,key=str(app.config['GOOGLE_MAP_API']))


###################################################




###################################################
#######API with AJAX For Like Button ##############
###################################################

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



###################################################
#######Static Page ################################
###################################################


@core.route('/term')
def term():
    return render_template('term.html')


@core.route('/term/privacy-policy')
def privacy():
    return render_template('privacy.html')


@core.route('/komaneko-member')
def member():
    return render_template('member.html')



@core.route('/komafood',methods=["GET", "POST"])
def komafood():
    key = str(app.config['GOOGLE_MAP_API']) # 上記で作成したAPIキーを入れる
    client = googlemaps.Client(key) #インスタンス生成
    loc = {'lat': 35.6288505, 'lng': 139.65863579999996} # 軽度・緯度を取り出す
    if request.method == 'GET' and request.args.get('category') == 'noodle':
        place_results = client.places_nearby(location=loc, radius=1000, keyword='ラーメン',language='ja') #半径1000m以内のカフェ情報を取得
        print('#############################')
        pprint.pprint(place_results)
    # elif: request.method == 'GET' and request.args.get('category') == 'cafe':
    else:
        place_results = client.places_nearby(location=loc, radius=1000, keyword='カフェ',language='ja') #半径1000m以内のカフェ情報を取得
        pprint.pprint(place_results)
    results = []
    photos = []
    pins = []
    for place_result in place_results['results']:
        pprint.pprint(place_result['geometry']['location'])
        pins.append(place_result['geometry']['location'])
        # pins.update(place_result['name'])
        results.append(place_result)
        if not 'photos' in place_result.keys():
            photo = 'https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/default_profile.png'
            photos.append(photo)
        else:
            p_value = place_result['photos'][0]['photo_reference']
            photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(p_value,str(app.config['GOOGLE_MAP_API']))
            photos.append(photo)
    pprint.pprint(photos)
    pprint.pprint(pins)
    return render_template('comacafe.html',results=results,photos=photos)

