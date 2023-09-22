from flask import jsonify, url_for, redirect, render_template
from flask_login import current_user
import datetime
from humanize import naturaltime

from .models.wishlist import WishlistItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)


def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)


@bp.route('/wishlist')
def wishlist():
    if current_user.is_authenticated:
        items = WishlistItem.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        return render_template('wishlist.html',
                               items=items,
                               humanize_time=humanize_time)
    else:
        return jsonify({}), 404


@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    if current_user.is_authenticated:
        WishlistItem.add(current_user.id, product_id, datetime.datetime.now())
        return redirect(url_for('wishlist.wishlist'))
    else:
        return jsonify({}), 404
