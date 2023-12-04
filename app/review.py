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

def findById(reviewSet, givenId):
    for elem in reviewSet:
        if str(elem.id) == str(givenId):
            return elem

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)


@bp.route('/review', methods = ['POST','GET'])
def review():
    # get all available products for reivew:
    idToUse = request.form.get('searchReviewChoice')
    items = Review.get_all_by_uid_since(
        idToUse, datetime.datetime(1980, 9, 14, 0, 0, 0))
    sItems = SellerReview.get_all_by_uid_since(
                    idToUse, datetime.datetime(1980, 9, 14, 0, 0, 0))
    
    for review in items:
        print(review.upvotes)

    return render_template('review.html',
                    reviews=items,
                    sellerReviews = sItems, 
                    humanize_time=humanize_time,
                    composedItems=None)
    
    # render the page by adding information to the index.html file



#for future
# @bp.route('/review')
# def review():
#     # get all available products for reivew:
#     if current_user.is_authenticated:
#         items = Review.get_all_by_uid_since(
#             current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
#         sItems = SellerReview.get_all_by_uid_since(
#                         current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
       
#         return render_template('review.html',
#                       reviews=items,
#                       sellerReviews = sItems, 
#                       humanize_time=humanize_time,
#                       composedItems=None)
#     else:
#         items = None
#         return render_template('review.html',
#                       reviews=items,
#                       sellerReviews = sItems,
#                       humanize_time=humanize_time,
#                       composedItems=None)
#     # render the page by adding information to the index.html file

@bp.route('/review/add/<int:product_id>', methods=['POST'])
def review_add(product_id):
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
INSERT INTO reviews (uid, pid, review, rating, time_posted)
VALUES(:uid, :pid, :review, :rating, :time_posted)
""",
                                  uid=current_user.id,
                                  pid = product_id,
                                  review = "",
                                  rating = 0,
                                  time_posted = datetime.datetime.now())
            return redirect(url_for('review.review'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404

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
            return redirect(url_for('review.review'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404



@bp.route('/review/update', methods=['POST', 'GET'])
def review_update():
    product_id = request.form.get('pidChoice')
    review = request.form.get('reviewChoice')
    rating = request.form.get('ratingChoice')
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
UPDATE Reviews
SET review = :review, rating = :rating, time_posted = :time_posted
WHERE uid = :uid
AND pid = :pid

""",
                                uid=current_user.id,
                                pid=product_id,
                                review=review,
                                rating=rating,
                                time_posted=datetime.datetime.now())
        #push them over to wishlist()
            # print(str(product_id) + "pid")
            # print(str(current_user.id) + "uid")
            return redirect(url_for('review.review'))
        except Exception as e:
            print("Update unsuccessful, sorry :( - "+ str(e))
            return redirect(url_for('review.review'))
    else:
        return jsonify({}), 404


@bp.route('/review/feedback')
def feedback():
    if current_user.is_authenticated:
        reviewItems = Review.get_most_recent_five_by_uid(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        sellerReviewItems = SellerReview.get_most_recent_five_by_uid(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        print("PRINTING REVIEW ITEMS")
        sortTogetherDict = { ("r"+str(r.id)):(r.time_posted) for r in reviewItems}
        
        # print("PRINTING SELLER REVIEW ITEMS")
        for srItem in sellerReviewItems:
            sortTogetherDict["s"+str(srItem.id)] = srItem.time_posted
        
        composedItems = []
        for k,v in sorted(sortTogetherDict.items(),key=lambda x:x[1], reverse=True):
            ktype = k[0]
            kRest = k[1:]
            
            if len(composedItems) < 5:
                if ktype == "r":
                    composedItems.append([ktype, findById(reviewItems, kRest)])
                else:
                    composedItems.append([ktype, findById(sellerReviewItems, kRest)])

        # for c in composedItems:
        #     print(c)
        
        items = None
        return render_template('review.html',
                      reviews=None,
                      sellerReviews=None,
                      humanize_time=humanize_time,
                      composedItems=composedItems)
    else:
        items = None
        return render_template('review.html',
                      reviews=None,
                      sellerReviews = None,
                      humanize_time=humanize_time,
                      composedItems=None)

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
                                  
            return redirect(url_for('review.review'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404



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
            return redirect(url_for('review.review'))
        except Exception as e:
            print("Update unsuccessful, sorry :( - "+ str(e))
            return redirect(url_for('review.review'))
    else:
        return jsonify({}), 404
