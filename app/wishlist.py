from flask import render_template
from flask import jsonify
from flask_login import current_user
import datetime
from flask import redirect, url_for
from flask import flash

from humanize import naturaltime
from flask import current_app as app

from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishlistItem
from flask import redirect, url_for

from flask import Blueprint
bp = Blueprint('wishlist', __name__)


def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)


@bp.route('/wishlist')
def wishlist():
    if (current_user.is_authenticated):
        items = WishlistItem.get_all(current_user.id)
        return render_template('wishlist.html',
                      items=items,
                      humanize_time=humanize_time)


    else:
        return jsonify({}), 404 


@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    if current_user.is_authenticated:
        WishlistItem.add(current_user.id, product_id, datetime.datetime.now())
        flash("Item added to wishlist successfully", "success")
        wisheslist = WishlistItem.get(current_user.id)
        return redirect(url_for('wishlist.wishlist'))
    else:
        return jsonify({}), 404

