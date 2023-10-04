from flask import jsonify
from flask import render_template
from flask_login import current_user
import datetime

from flask import current_app as app

from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishlistItem
from flask import redirect, url_for

from flask import Blueprint
bp = Blueprint('wishlist', __name__)

from humanize import naturaltime

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)


@bp.route('/wishlist')
def wishlist():
    if (current_user.is_authenticated):
        items = WishlistItem.get_all(current_user.id)
        #return jsonify([item.__dict__ for item in items])
        return render_template('wishlist.html',
                      items=items,
                      humanize_time=humanize_time)


    else:
        return jsonify({}), 404 


@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
        rows = app.db.execute("""
INSERT INTO Wishes(uid, pid, time_added)
VALUES(:uid, :pid, :time_added)
""",
                                  uid=current_user.id,
                                  pid=product_id,
                                  time_added=datetime.datetime.now())
        return redirect(url_for('wishlist.wishlist'))
