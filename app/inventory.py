from flask import jsonify
from flask import render_template
from flask_login import current_user
from humanize import naturaltime
import datetime

from .models.product import Product
from .models.inventory import InventoryItem
from flask import current_app as app

from flask import Blueprint
bp = Blueprint('inventory', __name__)

from flask import redirect, url_for

@bp.route('/inventory')
def inv():
    # find the products current user has bought:
    if current_user.is_authenticated:
        itemsInInventory = InventoryItem.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        return render_template('inventory.html',
            items=itemsInInventory,
            humanize_time=humanize_time)
    else:
        wishlists = None
        return jsonfiy({}), 404

@bp.route('/inventory/add/<int:product_id>', methods=['POST'])
def inventory_add(product_id):
        rows = app.db.execute("""
INSERT INTO Inventory(uid, pid, time_added)
VALUES(:uid, :pid, :time_added)
""",
                                  uid=current_user.id,
                                  pid=product_id,
                                  time_added=datetime.datetime.now())
        return redirect(url_for('inventory.inv'))

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

