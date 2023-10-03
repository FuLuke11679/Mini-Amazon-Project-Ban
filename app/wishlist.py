from flask import render_template
from flask_login import current_user
from flask import current_app as app 
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishlistItem
from flask import jsonify
from flask import Blueprint
from flask import redirect, url_for
from humanize import naturaltime

bp = Blueprint('wishlist', __name__)



def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/wishlist')
def wishlist():
    # get all available products for sale:
    # find the products current user has on wishlist:
    if current_user.is_authenticated:
        items = WishlistItem.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
       
        return render_template('wishlist.html',
                      items=items,
                      humanize_time=humanize_time)
    else:
        items = None
        return render_template('wishlist.html',
                      items=items,
                      humanize_time=humanize_time)
    # render the page by adding information to the index.html file

@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    if current_user.is_authenticated:
        #update wishes with the new product
        #product in structure of id, uid, pid, time_purchased
        #in this case - current_user.id, product_id, datetime.now()

        try:
            rows = app.db.execute("""
INSERT INTO wishes (uid, pid, time_added)
VALUES(:uid, :pid, :time_added)
""",
                                  uid=current_user.id,
                                  pid = product_id,
                                  time_added = datetime.datetime.now())
        #push them over to wishlist()
            return redirect(url_for('wishlist.wishlist'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404
    

 
