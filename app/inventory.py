from flask import jsonify
from flask import render_template
from flask_login import current_user
from humanize import naturaltime
import datetime
from flask import request

from .models.product import Product
from .models.inventory import InventoryItem
from flask import current_app as app

from flask import Blueprint
bp = Blueprint('inventory', __name__)

from flask import redirect, url_for

@bp.route('/inventory')
def inv():
    itemsInInventory = InventoryItem.get_all_by_uid_since(
        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    return render_template('inventory.html',
        items=itemsInInventory,
        humanize_time=humanize_time)

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

@bp.route('/inventory/view', methods=['GET','POST'])
def inventory_view():
    if request.method == 'POST':
        user_id = request.form['user_id']
        itemsInInventoryView = InventoryItem.get_all_by_uid_since(
            user_id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        return render_template('inventory.html',
            items=itemsInInventoryView,
            humanize_time=humanize_time)
    return render_template('index.html')
