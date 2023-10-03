from flask import jsonify
from flask_login import current_user
import datetime

from .models.product import Product
from .models.wishlist import WishItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)


@bp.route('/wishlist')
def index():
    # find the products current user has bought:
    if current_user.is_authenticated:
        wishlists = WishItem.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        wishlists = None
        return jsonfiy({}), 404
    # render the page by adding information to the index.html file
    return jsonify([item.__dict__ for item in wishlists])
