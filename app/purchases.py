from flask import jsonify
from flask import render_template
from flask_login import current_user
import datetime

from flask import current_app as app

from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishlistItem
from flask import redirect, url_for
from flask import request

from flask import Blueprint
bp = Blueprint('purchases', __name__)

from humanize import naturaltime

@bp.route('/purchases/<int:user_id>', methods = ['GET'])
def purchases(user_id):
    purchasedItems = Purchase.get_all(user_id)
    return render_template('purchases.html',
                    items=purchasedItems, user_id = user_id)
    
@bp.route('/purchases_search', methods = ['GET', 'POST'])
def purchases_search():
    if request.method == 'POST':
        user_id = request.form['user_id']
        purchasedItems = Purchase.get_all(user_id)
        return render_template('purchases.html',
                      purchaseditems=purchasedItems, user_id = user_id) 
    else:
        return render_template('purchases.html')
    
    
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
