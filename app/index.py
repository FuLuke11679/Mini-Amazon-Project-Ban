from flask import render_template, request
from flask_login import current_user
from flask import redirect, url_for
from .models.user import User
from .models.product import Product
from .models.purchase import Purchase
from .models.review import Review
from humanize import naturaltime

import datetime

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    # Get page value or default 1 (for products for sale display)
    page = int(request.args.get('page', 1))

    # Get the value of K from the form or use a default value of 10
    k = int(request.args.get('k', 10))

    # Get the sorting order from the request, default to ascending
    sort_order = request.args.get('sort_order', 'asc')

    # Get all available products for sale, sorted by price as per user's choice
    products = Product.get_all_sorted(True, page, 10, sort_order)

    # Find the products current user has bought
    recent_purchases = None
    if current_user.is_authenticated:
        recent_purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))

    # Retrieve the top k most expensive products
    top_k_products = Product.get_top_k_expensive(k)

    # Render the index.html template with the provided variables
    return render_template('index.html',
                           page=page,
                           avail_products=products,
                           recent_purchase_history=recent_purchases,
                           top_k_products=top_k_products,
                           k=k)  # Pass k to the template to pre-fill the input field


@bp.route('/search_results', methods = ['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        user_id = request.form['user_id']
        return redirect(url_for('purchases.purchases', user_id = user_id))
    return render_template('index.html')


@bp.route('/product/<int:product_id>', methods=['GET'])
def product_page(product_id):
    current_product = Product.get(product_id)
    current_seller = User.get(current_product.seller_id)
    top_3_reviews = Review.get_top_3_helpful(product_id)
    print(top_3_reviews)
    associated_reviews = Review.get_reviews_minus_top_3(product_id)
    # print(product_id)
    # print(associated_reviews.review)
    return render_template('productsPage.html', 
                            current_product=current_product,
                            top_3_reviews=top_3_reviews,
                            associated_reviews=associated_reviews,
                            humanize_time=humanize_time,
                            current_seller=current_seller)


@bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    tag = request.args.get('tag')
    sort_order = request.args.get('sort_order', 'asc')
    if keyword:
        if tag:
            products = Product.search_in_category_sorted(keyword, tag, sort_order)
        else:
            products = Product.search_sorted(keyword, sort_order)
    else:
        products = []  # Handle this as you see fit

    return render_template('search_results.html', products=products, search_term=keyword, tag=tag)


