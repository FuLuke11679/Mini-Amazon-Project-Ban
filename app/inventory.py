from flask import jsonify
from flask import render_template
from flask_login import current_user
from humanize import naturaltime
import datetime
from flask import request

from .models.product import Product
from .models.purchase import Purchase
from .models.purchaseorder import PurchaseOrder
from .models.inventory import InventoryItem
from flask import current_app as app

from flask import Blueprint
bp = Blueprint('inventory', __name__)

from flask import redirect, url_for

@bp.route('/inventory', methods=['GET', 'POST'])
def inv():
    if(InventoryItem.get_seller(current_user.id)[0] == 0):
        return redirect(url_for('index.index'))
    itemsInInventory = InventoryItem.get_all_by_uid_since(
        current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    return render_template('inventory.html',
        items=itemsInInventory,
        humanize_time=humanize_time)

@bp.route('/inventory/add', methods=['POST'])
def inventory_add():
    product_id = request.form['product_id']
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
INSERT INTO Inventory(uid, pid, time_added, quantity)
VALUES(:uid, :pid, :time_added, 1)
""",
                                  uid=current_user.id,
                                  pid=product_id,
                                  time_added=datetime.datetime.now())
            return redirect(url_for('inventory.inv'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/inventory/view', methods=['GET','POST'])
def inventory_view():
    if request.method == 'POST':
        user_id = request.form['user_id']
        if(InventoryItem.get_seller(user_id)[0] == 0):
            return redirect(url_for('index.index'))
        itemsInInventoryView = InventoryItem.get_all_by_uid_since(
            user_id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        return render_template('inventoryview.html',
            items=itemsInInventoryView,
            humanize_time=humanize_time)
    return('index.html')

@bp.route('/inventory/delete/<int:product_id>', methods=['POST'])
def inventory_delete(product_id):
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
DELETE FROM Inventory
WHERE uid = :uid
AND pid = :pid
""",
                                  uid=current_user.id,
                                  pid=product_id)
            return redirect(url_for('inventory.inv'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404
    
@bp.route('/inventory/update/<int:product_id>', methods=['POST'])
def inventory_update(product_id):
    new_quantity = request.form['quantity']
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
UPDATE Inventory
SET quantity = :quantity                                 
WHERE uid = :uid
AND pid = :pid
""",
                                  uid=current_user.id,
                                  pid=product_id,
                                  quantity=new_quantity)
            return redirect(url_for('inventory.inv'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404

@bp.route('/inventory/register', methods=['GET', 'POST'])
def inventory_register():
    if(InventoryItem.get_seller(current_user.id)[0] == 1):
        return redirect(url_for('index.index'))
    if current_user.is_authenticated:
        numSellers = InventoryItem.get_num()[0]
        try:
            rows = app.db.execute("""
INSERT INTO Sellers
VALUES(:id, :uid)
""",
                                  id = numSellers,
                                  uid=current_user.id)
            return redirect(url_for('inventory.inv'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404
    
@bp.route('/inventory/order_fulfill', methods=['GET', 'POST'])
def inventory_order_fulfill():
    if current_user.is_authenticated:
        user_id = current_user.id
        orderlist = PurchaseOrder.get_all_seller_id(user_id)  # Assuming you want to get purchases associated with the user
        return render_template('orderfulfillment.html',
                           orderlist=orderlist,
                           humanize_time=humanize_time,
                           user_id=user_id)
    else:
        return jsonify({}), 404
    
@bp.route('/inventory/confirm_fulfill/<int:order_id>/<int:product_id>', methods=['GET', 'POST'])
def inventory_confirm_fulfill(order_id, product_id):
    if current_user.is_authenticated:
        try:
            rows = app.db.execute("""
UPDATE Purchases
SET fulfillment_status = 'Fulfilled'                                 
WHERE id = :id
AND pid = :pid
""",
                                  id=order_id,
                                  pid=product_id)
            return redirect(url_for('inventory.inventory_order_fulfill'))
        except Exception as e:
            print(str(e))
            return jsonify({}), 404
    else:
        return jsonify({}), 404
    