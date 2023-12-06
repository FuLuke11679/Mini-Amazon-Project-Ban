from flask import render_template
from flask import jsonify
from flask_login import current_user
import datetime
from flask import current_app as app 
from flask import redirect, url_for
from flask import flash
from flask import request

from humanize import naturaltime
from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishlistItem
from .models.cart import CartItem

from flask import Blueprint
bp = Blueprint('cart', __name__)

def humanize_time(dt):
    return naturaltime(datatime.datetime.now() - dt)

def get_product_price(product_id):
    product = Product.get(product_id)
    return product.price if product else 0  # Default to 0 if product not found

def calculate_total_price(cartlist):
    total_price = 0
    for item in cartlist:
        price = get_product_price(item.pid)
        total_price += item.quantity * price
    return total_price

@bp.route('/cart')
def cart():
    # find the products current user has wishlisted:
    if current_user.is_authenticated:
        cartlist = CartItem.get_all(
            current_user.id)
        total_price = calculate_total_price(cartlist)
        return render_template('cart.html',
                      cartlist=cartlist,
                      humanize_time=humanize_time,
                      total_price=total_price,
                      get_product_price=get_product_price) 
    else:
        return jsonify({}), 404

     #render the page by adding information to the index.html file

@bp.route('/get_cart', methods = ['GET', 'POST'])
def get_cart():
        user_id = current_user.id
        cartlist = CartItem.get_all(user_id)
        total_price = calculate_total_price(cartlist)
        return render_template('cart.html',
                      cartlist=cartlist,
                      humanize_time=humanize_time, 
                      total_price=total_price, 
                      get_product_price=get_product_price,
                      user_id = user_id) 

@bp.route('/cart/update_quantity/<int:product_id>', methods = ['GET', 'POST'])
def update_quantity(product_id):
        user_id = current_user.id
        quantity = request.form['quantityChoice']
        rows = app.db.execute("""
UPDATE Carts
SET quantity = :quantity
WHERE uid = :uid AND pid = :pid

    """,
                                uid=user_id,
                                quantity=quantity,
                                pid=product_id)
            #push them over to wishlist()
                # print(str(product_id) + "pid")
                # print(str(current_user.id) + "uid")
        cartlist = CartItem.get_all(user_id)
        total_price = calculate_total_price(cartlist)
        return render_template('cart.html',
                      cartlist=cartlist,
                      humanize_time=humanize_time, 
                      total_price=total_price, 
                      get_product_price=get_product_price,
                      user_id = user_id) 
    
@bp.route('/cart_search', methods = ['GET', 'POST'])
def cart_search():
    if request.method == 'POST':
        user_id = request.form['user_id']
        cartlist = CartItem.get_all(user_id)
        total_price = calculate_total_price(cartlist)
        return render_template('cart.html',
                      cartlist=cartlist,
                      humanize_time=humanize_time, 
                      total_price=total_price, 
                      get_product_price=get_product_price,
                      user_id = user_id) 
    else:
        return render_template('cart.html')

@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    if current_user.is_authenticated:
        quantity = request.form.get('quantityChoice')
        CartItem.add(current_user.id, product_id, datetime.datetime.now(), quantity)
        flash("Item added to cart successfully", "success")
        cartlist = CartItem.display_num(current_user.id, 5, 1)
        return redirect(url_for('cart.cart'))
    else:
        return jsonify({}), 404


@bp.route('/cart/remove_item/<int:product_id>', methods = ['GET', 'POST'])
def remove_item(product_id):
        user_id = current_user.id
        rows = app.db.execute("""
DELETE FROM Carts
WHERE uid = :uid AND pid = :pid

    """,
                                uid=user_id,
                                pid=product_id)
            #push them over to wishlist()
                # print(str(product_id) + "pid")
                # print(str(current_user.id) + "uid")
        cartlist = CartItem.get_all(user_id)
        total_price = calculate_total_price(cartlist)
        return render_template('cart.html',
                      cartlist=cartlist,
                      humanize_time=humanize_time, 
                      total_price=total_price, 
                      get_product_price=get_product_price,
                      user_id = user_id) 
 
@bp.route('/cart_submit')        
def cart_submit():
    cartlist = CartItem.get_all(current_user.id)
    
    return product.price if product else 0  # Default to 0 if product not found