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

    # key = app.config['GOOGLE_MAP_API'] # 上記で作成したAPIキーを入れる
    # client = googlemaps.Client(key) #インスタンス生成

    # geocode_result = client.geocode('駒澤大学') # 位置情報を検索
    # loc = geocode_result[0]['geometry']['location'] # 軽度・緯度の情報のみ取り出す
    # place_result = client.places_nearby(location=loc, radius=1000, keyword='カフェ') #半径200m以内のレストランの情報を取得
    # # pprint.pprint(place_result)
    # results = []
    # photos = []

    # for i,place in enumerate(place_result['results']):
    #     my_place_id =place['place_id']
    #     my_fields = ['name','type','url','photo','vicinity','website','international_phone_number','rating']
       
    #     place_details = client.place(place_id = my_place_id,fields = my_fields,language='ja')
        
    #     # pprint.pprint(place_details)
    #     results.append(place_details)
    #     # pprint.pprint(place_details['result']['name'])
    #     # pprint.pprint(place_details['result']['url'])
    #     result = place_details['result']
    #     pprint.pprint(result)

    #     if not 'photos' in result.keys():
    #         photo = 'https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/default_profile.png'
    #         photos.append(photo)
    #     else:
    #         p_value = result['photos'][0]
    #         photos_photo_reference = p_value['photo_reference']
    #         pprint.pprint(photos_photo_reference)
    #         photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(photos_photo_reference,str(app.config['GOOGLE_MAP_API']))
    #         photos.append(photo)
    #     if i == 7:
    #         break;
    
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
    all_posts = BlogPost.query.filter(BlogPost.event_date >= datetime.utcnow()).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    #直近開催イベント
    blog_posts = BlogPost.query.filter(BlogPost.event_date >= datetime.utcnow()).order_by(BlogPost.event_date.asc()).paginate(page=page,per_page=5)

    past_posts = BlogPost.query.filter(BlogPost.event_date <= datetime.utcnow()).order_by(BlogPost.event_date.desc())

    alls = User.query.filter(User.type > 1)
    return render_template('index.html',blog_posts=blog_posts,all_posts=all_posts,url=request.base_url,alls=alls,past_posts=past_posts)


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


@core.route('/komafood')
def komafood():
    # key = app.config['GOOGLE_MAP_API'] # 上記で作成したAPIキーを入れる
    # client = googlemaps.Client(key) #インスタンス生成

    # geocode_result = client.geocode('駒澤大学') # 位置情報を検索
    # loc = geocode_result[0]['geometry']['location'] # 軽度・緯度を取り出す
    # place_result = client.places_nearby(location=loc, radius=1000, keyword='カフェ') #半径1000m以内のカフェ情報を取得
    # pprint.pprint(place_result)
    
    # # リスト作成
    # results = []
    # photos = []
    # for place in place_result['results']:
    #     my_place_id =place['place_id']
    #     # 検索結果の取得したい情報を選択
    #     my_fields = ['name','type','url','photo','vicinity','website','formatted_phone_number','rating']
       
    #     place_details = client.place(place_id = my_place_id,fields = my_fields,language='ja')
    #   #デバッグ
    #     results.append(place_details)
    #     result = place_details['result']
    #     # pprint.pprint(result)

    #     # 配列にphotosが存在しないとき、NO IMAGE画像を表示。
    #     if not 'photos' in result.keys():
    #         photo = 'https://'+str(app.config['AWS_BUCKET'])+'.s3-ap-northeast-1.amazonaws.com/default_profile.png'
    #         photos.append(photo)
    #     # 配列にphotosが存在するとき、画像情報を取得。
    #     else:
    #         p_value = result['photos'][0]
    #         photos_photo_reference = p_value['photo_reference']
    #         pprint.pprint(photos_photo_reference)
    #         photo = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}'.format(photos_photo_reference,str(app.config['GOOGLE_MAP_API']))
    #         photos.append(photo)
    # # pprint.pprint(results)
    return render_template('comacafe.html')




