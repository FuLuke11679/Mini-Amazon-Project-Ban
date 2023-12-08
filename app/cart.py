from flask import render_template
from flask import jsonify
from flask_login import current_user
import datetime
from flask import current_app as app 
from flask import redirect, url_for
from flask import flash
from flask import request
from flask import Markup

from humanize import naturaltime
from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishlistItem
from .models.cart import CartItem
from .models.user import User

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

def get_product_name(product_id):
    product = Product.get(product_id)
    return product.name 

def get_seller_id(product_id):
    product = Product.get(product_id)
    return product.seller_id

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
                      get_product_price=get_product_price,
                      get_product_name = get_product_name,
                      user_id = current_user.id,
                      get_seller_id = get_seller_id) 
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
                      user_id = user_id,
                      get_product_name = get_product_name,
                      get_seller_id = get_seller_id) 

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
                      user_id = user_id,
                      get_product_name = get_product_name,
                      get_seller_id = get_seller_id) 
    
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
                      user_id = user_id,
                      get_product_name=get_product_name,
                      get_seller_id = get_seller_id) 
    else:
        return render_template('cart.html')

@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    if current_user.is_authenticated:
        quantity = request.form.get('quantityChoice')
        CartItem.add(current_user.id, product_id, datetime.datetime.now(), quantity)
        flash("Item added to cart successfully", "success")
        cartlist = CartItem.get_all(current_user.id)
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
                      user_id = user_id,
                      get_product_name=get_product_name,
                      get_seller_id=get_seller_id) 
 
@bp.route('/cart_submit')        
def cart_submit():
    cartlist = CartItem.get_all(current_user.id)
    
    return product.price if product else 0  # Default to 0 if product not found


@bp.route('/cart_submit2', methods=['GET', 'POST'])
def cart_submit2():
    user_id = current_user.id
    cartlist = CartItem.get_all(current_user.id)
    orderid = Purchase.get_max_id() + 1
    invalid = CartItem.return_invalid(current_user.id)
    total_price = calculate_total_price(cartlist)
    balance = current_user.balance
    
    if not cartlist:
        flash("Your cart is empty", "info")
        return redirect(url_for('cart.get_cart'))

    if not invalid and balance >= total_price:
        for cart_item in cartlist:
            pid = cart_item.pid
            quantity = cart_item.quantity
            product = Product.get(pid)
            Purchase.create_purchase(id=orderid,
                                     uid=current_user.id,
                                     seller_id=product.seller_id,
                                     pid=pid,
                                     name=product.name,
                                     photo_url=product.photo_url,
                                     tag=product.tag,
                                     quantity=quantity,
                                     price_per_unit=product.price,
                                     total_price=product.price * quantity,
                                     time_purchased=datetime.datetime.now(),
                                     fulfillment_status="In Progress")
            User.updateBal(current_user.id, total_price)
        CartItem.delete_all(user_id)
        flash("Your order has been submitted successfully!", "success")
        return redirect(url_for('cart.get_cart'))
    else:
        error_message = "Please review the following issues: <br>"
        if balance < total_price:
            error_message += f"Insufficient balance. Please add funds to your account. Balance: {balance}, Total Price: {total_price}."
        if invalid:
            error_message += " <br>Some items in your cart have quantities greater than available amounts:<br>"
            for item in invalid:
                amount = Product.get_amount_num(item.pid)
                error_message += f"Product ID: {item.pid}, Quantity: {item.quantity}, Available Amount: {amount}<br>"
        flash(Markup(error_message), "error")
        return redirect(url_for('cart.get_cart'))
    
@staticmethod
def delete_all(user_id):
        try:
            rows = app.db.execute('''
DELETE FROM Carts
WHERE uid = :user_id
''', 
                                user_id=user_id)
            return True
        except Exception as e:
            # Handle the exception (log it, return False, etc.)
            return False
