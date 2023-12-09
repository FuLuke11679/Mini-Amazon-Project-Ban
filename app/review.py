from flask import render_template
from flask import request
from flask_login import current_user
from flask import current_app as app 
import datetime

from .models.review import Review 
from .models.sellerreview import SellerReview

from flask import jsonify
from flask import Blueprint
from flask import redirect, url_for
from humanize import naturaltime

bp = Blueprint('review', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)


#add an initial review that the user can update
@bp.route('/review/add/<int:product_id>', methods=['POST'])
def review_add(product_id):
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
INSERT INTO reviews (uid, pid, review, rating, upvotes, time_posted, photo_url)
VALUES(:uid, :pid, :review, :rating, :upvotes, :time_posted, :photo_url)
""",
                                  uid=current_user.id,
                                  pid = product_id,
                                  review = "You have just added this review.",
                                  rating = 0,
                                  upvotes = 1,
                                  time_posted = datetime.datetime.now(),
                                  photo_url = "https://picsum.photos/200/200")
            return redirect(url_for('users.myprofile'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404


#delete a review
@bp.route('/review/delete/<int:product_id>', methods=['POST'])
def review_delete(product_id):
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
DELETE FROM Reviews
WHERE uid = :uid
AND pid = :pid
""",
                                  uid=current_user.id,
                                  pid =product_id)
        #push them over to wishlist()
            # print(str(product_id) + "pid")
            # print(str(current_user.id) + "uid")
            return redirect(url_for('users.myprofile'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404


#route to update a review
@bp.route('/review/update', methods=['POST', 'GET'])
def review_update():
    product_id = request.form.get('pidChoice')
    review = request.form.get('reviewChoice')
    rating = request.form.get('ratingChoice')
    imageChoice = request.form.get("imageChoice")

    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
UPDATE Reviews
SET review = :review, rating = :rating, time_posted = :time_posted, photo_url = :photo_url
WHERE uid = :uid
AND pid = :pid

""",
                                uid=current_user.id,
                                pid=product_id,
                                review=review,
                                rating=rating,
                                time_posted=datetime.datetime.now(),
                                photo_url= "https://picsum.photos/200/200")
        #push them over to wishlist()
            # print(str(product_id) + "pid")
            # print(str(current_user.id) + "uid")
            return redirect(url_for('users.myprofile'))
        except Exception as e:
            print("Update unsuccessful, sorry :( - "+ str(e))
            return redirect(url_for('users.myprofile'))
    else:
        return jsonify({}), 404

#delete a Seller Review
@bp.route('/sellerreview/delete/<int:seller_uid>', methods=['POST'])
def sellerreview_delete(seller_uid):
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
DELETE FROM SellerReviews
WHERE uid = :uid
AND seller_uid = :suid
""",
                                  uid=current_user.id,
                                  suid=seller_uid)
                                  
            return redirect(url_for('users.myprofile'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404


#update a Seller Review
@bp.route('/sellerreview/update', methods=['POST', 'GET'])
def sellerreview_update():
    seller_uid = request.form.get('suidChoice')
    review = request.form.get('reviewChoice2')
    rating = request.form.get('ratingChoice2')
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
UPDATE SellerReviews
SET review = :review, rating = :rating, time_posted = :time_posted
WHERE uid = :uid
AND seller_uid = :suid

""",
                                uid=current_user.id,
                                suid=seller_uid,
                                review=review,
                                rating=rating,
                                time_posted=datetime.datetime.now())
        #push them over to wishlist()
            # print(str(product_id) + "pid")
            # print(str(current_user.id) + "uid")
            return redirect(url_for('users.myprofile'))
        except Exception as e:
            print("Update unsuccessful, sorry :( - "+ str(e))
            return redirect(url_for('users.myprofile'))
    else:
        return jsonify({}), 404
