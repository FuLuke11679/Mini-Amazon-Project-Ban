from flask import jsonify
from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishListItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)


@bp.route('/wishlist')
def wishlist():
    if (current_user.is_authenticated):
        #idd = WishListItem.get(current_user.id)
        items = WishListItem.get(current_user.id)
        #items = WishListItem.get_all(idd)
        return jsonify([item.__dict__ for item in items])

    else:
        return jsonify({}), 404
