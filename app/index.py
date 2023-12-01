from flask import render_template, request
from flask_login import current_user
from .models.product import Product
from .models.purchase import Purchase
from .models.review import Review
import datetime
from flask import Blueprint

bp = Blueprint('index', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
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

    return render_template('index.html',
                           avail_products=products
                           purchase_history=purchases,
                           reviews=reviews)  # Removed the top k products and k variable

@bp.route('/search_results', methods = ['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        user_id = request.form['user_id']
        return redirect(url_for('purchases.purchases', user_id = user_id))
    return render_template('index.html')


@bp.route('/product_details', methods=['GET'])
def product_details():
    # Get the product_id from the query parameter
    product_id = request.args.get('product_id')

    # Fetch the product details based on the product_id from your data source
    product = Product.get(product_id)

    # Render the product_details.html template with the product details
    return render_template('product_details.html', product=product)  # Pass the 'product' object
