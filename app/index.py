from flask import render_template, request
from flask_login import current_user
from flask import redirect, url_for
from .models.user import User
from .models.product import Product
from .models.purchase import Purchase
from .models.review import Review
from humanize import naturaltime
from flask import jsonify
from flask import request, redirect, url_for
from flask_login import current_user  # Import current_user for getting seller_id
from .db import DB

from flask import current_app



import datetime

def is_seller(user_id):
  rows = current_app.db.execute('''
      SELECT id FROM Sellers
      WHERE uid = :user_id
  ''', user_id=user_id)




  return bool(rows)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

from flask import Blueprint
bp = Blueprint('index', __name__)

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.route('/', methods=['GET', 'POST'])
def index():
    #print(request.args.get('page'))
    if request.method == 'POST':
    # Get page value or default 1 (for products for sale display)
        page = 1
    else:
        page = int(request.args.get('page', 1))
    # Get the sorting order from the request, default to ascending
    sort_order = request.args.get('sort_order', 'asc')

    # Get all available products for sale, sorted by price as per user's choice
    products = Product.get_all_sorted(True, sort_order, page=page)

    # Find the products current user has bought
    recent_purchases = None
    if current_user.is_authenticated:
        recent_purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        current_user.isseller = is_seller(current_user.id)
    else:
        current_user.isseller = False
    # print(current_user.__dict__)
    
    # Render the index.html template with the provided variables
    return render_template('index.html',
                           page=page,
                           avail_products=products,
                           recent_purchase_history=recent_purchases) 

'''
@bp.route('/search_results', methods = ['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        user_id = request.form['user_id']
        return redirect(url_for('purchases.purchases', user_id = user_id))
    return render_template('index.html')
'''

@bp.route('/product/<int:product_id>', methods=['GET'])
def product_page(product_id):
    current_product = Product.get(product_id)
    current_seller = User.get(current_product.seller_id)
    top_3_reviews = Review.get_top_3_helpful(product_id)

    associated_reviews = Review.get_reviews_minus_top_3(product_id)
    
    average_rating_a = Review.total_average(product_id)
    if average_rating_a == None:
        average_rating = None
    else:
        average_rating = average_rating_a[0]

    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None

    return render_template('productsPage.html', 
                            current_product=current_product,
                            top_3_reviews=top_3_reviews,
                            associated_reviews=associated_reviews,
                            humanize_time=humanize_time,
                            current_seller=current_seller,
                            num_of_reviews= (len(associated_reviews or "") + len(top_3_reviews or "")),
                            average_rating=average_rating,
                            user_id=user_id)


@bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    tag = request.args.get('tag', '')
    subtag = request.args.get('subtag', '')
    sort_order = request.args.get('sort_order', 'asc')
    print(str(keyword)+"       "+str(tag)+"       "+str(subtag)+"       "+str(sort_order))

    products = []

    if keyword:
        if tag and subtag == "":
            products = Product.search_in_category_sorted(keyword, tag, sort_order)
        elif tag and subtag != "":
            products = Product.search_with_everything(keyword, subtag, sort_order)
        else:
            #return all products with just keyword search
            products = Product.search_sorted(keyword, sort_order)
        
    else:
        if tag and subtag == "":
            products = Product.get_by_tag(tag, sort_order)
        elif tag == "" and subtag =="":
            products = Product.just_order(sort_order)
        else:
            products = Product.get_by_subtag(subtag, sort_order)
    
    subtags = Product.get_subtags_by_tag(tag)  # Fetch subtags based on the selected tag

    return render_template('search_results.html', products=products, 
                           search_term=keyword, tag=tag, subtag=subtag, subtags=subtags)

@bp.route('/get-subtags', methods=['GET'])
def get_subtags():
    tag = request.args.get('tag', '')
    subtags = Product.get_subtags_by_tag(tag)
    return jsonify({'subtags': subtags})


@bp.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    amount = int(request.form['amount'])
    photo_url = request.form['photo_url']
    longDescription = request.form['longDescription']
    tag = request.form['tag']
    subtag = request.form['subtag']

    # Check if a product with the same name exists for the current user
    existing_product = Product.get_by_name_and_seller(name, current_user.id)
    
    if existing_product:
        # Product with the same name already exists for the current user
        return "Product with the same name already exists for your account.", 400

    # Insert into Products and retrieve the new product id
    sql_product = """
    INSERT INTO Products (name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag)
    VALUES (:name, :price, :amount, TRUE, :photo_url, :seller_id, :longDescription, :tag, :subtag)
    RETURNING id
    """
    result = current_app.db.execute(sql_product, name=name, price=price, amount=amount, 
                                    photo_url=photo_url, seller_id=current_user.id, 
                                    longDescription=longDescription, tag=tag, subtag=subtag)
    
    if result:
        # Insert into Inventory
        product_id = result[0][0]  # Accessing the first row's first column which is the id
        sql_inventory = """
        INSERT INTO Inventory (uid, pid, quantity)
        VALUES (:uid, :pid, :quantity)
        """
        current_app.db.execute(sql_inventory, uid=current_user.id, pid=product_id, quantity=amount)

        # Redirect or other response
        return redirect(request.referrer or url_for('default_route'))
    else:
        # Handle the case where product insertion failed
        # Redirect or return an error message
        return "Error adding product", 500

    # Redirect to the same page
    return redirect(request.referrer or url_for('default_route'))
