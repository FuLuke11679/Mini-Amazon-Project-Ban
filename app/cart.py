from flask import render_template
from flask import jsonify
from flask_login import current_user
import datetime
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

@bp.route('/cart')
def cart():
    # find the products current user has wishlisted:
    if current_user.is_authenticated:
        cartlist = CartItem.get_all(
            current_user.id)
        return render_template('cart.html',
                      cartlist=cartlist,
                      humanize_time=humanize_time) 
    else:
        return jsonify({}), 404

     #render the page by adding information to the index.html file

    
@bp.route('/cart_search', methods = ['GET', 'POST'])
def cart_search():
    if request.method == 'POST':
        user_id = request.form['user_id']
        cartlist = CartItem.get_all(user_id)
        return render_template('cart.html',
                      cartlist=cartlist,
                      humanize_time=humanize_time,
                      user_id = user_id) 
    else:
        return render_template('cart.html')

@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    if current_user.is_authenticated:
        CartItem.add(current_user.id, product_id, datetime.datetime.now())
        flash("Item added to cart successfully", "success")
        cartlist = CartItem.get_all(current_user.id)
        return redirect(url_for('cart.cart'))
    else:
        return jsonify({}), 404


    