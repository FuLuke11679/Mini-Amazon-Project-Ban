from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishlistItem
from flask import jsonify
from flask import Blueprint
bp = Blueprint('wishlist', __name__)


@bp.route('/wishlist')
def wishlist():
    # get all available products for sale:
    # find the products current user has on wishlist:
    if current_user.is_authenticated:
        items = WishlistItem.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
       
        return jsonify([item.__dict__ for item in items])
    else:
        items = None
        return jsonify({}), 404
    # render the page by adding information to the index.html file
 
