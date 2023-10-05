from flask import render_template
from flask import jsonify
from flask_login import current_user
import datetime
from flask import redirect, url_for
from flask import flash

from humanize import naturaltime
from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishListItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)

def humanize_time(dt):
    return naturaltime(datatime.datetime.now() - dt)

@bp.route('/wishlist')
def wishlist():
    # find the products current user has wishlisted:
    if current_user.is_authenticated:
        wisheslist = WishListItem.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        products = Product.get_all(True)
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return render_template('wishlist.html',
                      wisheslist=wisheslist,
                      humanize_time=humanize_time)


@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    if current_user.is_authenticated:
        WishListItem.add(current_user.id, product_id, datetime.datetime.now())
        flash("Item added to wishlist successfully", "success")
        wisheslist = WishListItem.get(current_user.id)
        return redirect(url_for('wishlist.wishlist'))
    else:
        return jsonify({}), 404

