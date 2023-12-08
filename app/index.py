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

    # Get all available products for sale
    
    products = Product.get_all(True, page)

    # Find the products current user has bought
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        reviews = Review.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
        reviews = None

    # Retrieve the top k most expensive products
    top_k_products = Product.get_top_k_expensive(k)

    return render_template('index.html',
                           page=page,
                           avail_products=products,
                           recent_purchase_history=purchases,
                           top_k_products=top_k_products,
                           k=k)  # Pass k to the template to pre-fill the input field)

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

    associated_reviews = Review.get_reviews_minus_top_3(product_id)
    
    average_rating = Review.total_average(product_id)[0]
    # print(product_id)
    # print(associated_reviews.review)
    return render_template('productsPage.html', 
                            current_product=current_product,
                            top_3_reviews=top_3_reviews,
                            associated_reviews=associated_reviews,
                            humanize_time=humanize_time,
                            current_seller=current_seller,
                            num_of_reviews= (len(associated_reviews or "") + len(top_3_reviews or "")),
                            average_rating=average_rating)