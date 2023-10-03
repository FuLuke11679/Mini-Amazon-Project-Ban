from flask import render_template
from flask_login import current_user
from flask import current_app as app 
import datetime

from .models.review import Review 

from flask import jsonify
from flask import Blueprint
from flask import redirect, url_for
from humanize import naturaltime

bp = Blueprint('review', __name__)

hRnR = False

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/review')
def review():
    # get all available products for reivew:
    if current_user.is_authenticated:
        items = Review.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
       
        return render_template('review.html',
                      items=items,
                      reviews=items,
                      humanize_time=humanize_time,
                      hideRateNReview=hRnR)
    else:
        items = None
        return render_template('review.html',
                      items=items,
                      reviews=items,
                      humanize_time=humanize_time,
                      hideRateNReview=hRnR)
    # render the page by adding information to the index.html file

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



@bp.route('/review/update', methods=['POST'])
def review_update(product_id, review, rating):
    if current_user.is_authenticated:
        try:
            hRnR = True
            rows = app.db.execute("""
UPDATE Reviews
SET review = :review, rating = :rating
WHERE uid = :uid
AND pid = :pid

""",
                                uid=current_user.id,
                                pid=product_id,
                                review=review,
                                rating=rating)
        #push them over to wishlist()
            # print(str(product_id) + "pid")
            # print(str(current_user.id) + "uid")
            return redirect(url_for('review.review'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404
