from flask import render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase


from flask import redirect, url_for
from flask import request

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    # Get the value of K from the form or use a default value of 10
    k = int(request.args.get('k', 10))

    # Get all available products for sale
    products = Product.get_all(True)

    # Find the products current user has bought
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None

    # Retrieve the top k most expensive products
    top_k_products = Product.get_top_k_expensive(k)

    # Render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           top_k_products=top_k_products,
                           k=k)  # Pass k to the template to pre-fill the input field)

@bp.route('/search_results', methods = ['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        user_id = request.form['user_id']
        return redirect(url_for('purchases.purchases', user_id = user_id))
    return render_template('index.html')
