from flask import render_template
from flask import jsonify
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishListItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)


@bp.route('/wishlist')
def wishlist():
    # find the products current user has wishlisted:
    if current_user.is_authenticated:
        wisheslist = WishListItem.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    return jsonify([item.__dict__ for item in wisheslist])
