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

@bp.route('/purchases/<int:user_id>/<int:page>', methods = ['GET'])
def purchases(user_id, page):
    purchasedItems = Purchase.get_all(user_id, page = page, per_page=20)
    return render_template('purchases.html',
                    purchasedItems=purchasedItems, 
                    user_id = user_id, 
                    page = page)
    
@bp.route('/purchases_search', methods = ['GET', 'POST'])
def purchases_search():
    if request.method == 'POST':
        user_id = request.form['user_id']
        page = int(request.form.get('page', 1))
        purchasedItems = Purchase.get_all(user_id, page)
        return render_template('purchases.html',
                      purchasedItems=purchasedItems, 
                      user_id = user_id, 
                      page = page) 
    else:
        return render_template('purchases.html')
    
