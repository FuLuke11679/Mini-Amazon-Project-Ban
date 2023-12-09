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








import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np




















def humanize_time(dt):
   return naturaltime(datetime.datetime.now() - dt)


def calculate_total_price(orderlist):
   total_price = 0
   for item in orderlist:
       price = item.price_per_unit
       total_price += item.quantity * price
   return total_price


@bp.route('/purchases/<int:user_id>/<int:page>', methods = ['GET'])
def purchases(user_id, page):
   purchasedItems = Purchase.get_all(user_id, page = page, per_page=20)
   return render_template('purchases.html',
                   purchasedItems=purchasedItems,
                   user_id = user_id,
                   page = page)


@bp.route('/mypurchases/<int:page>', methods = ['GET'])
def mypurchases(page):
   purchasedItems = Purchase.get_all(current_user.id, page = page, per_page=20)


   recommended_pids = recommend_based_on_purchase_history(current_user.id, user_item_matrix)
   rec_products = Product.get_list_by_ids(recommended_pids)
  
   return render_template('purchases.html',
                   purchasedItems=purchasedItems,
                   rec_products = rec_products,
                   user_id = current_user.id,
                   page = page)
  
@bp.route('/purchases_search', methods=['GET', 'POST'])
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
       return redirect(url_for('purchases.html'))












#recommendation system
file_path = 'db/data/generated/Purchases.csv'
purchases_df = pd.read_csv(file_path, header=None)
column_names = ['id', 'uid', 'oid', 'seller_id', 'pid', 'name', 'photo_url', 'tag', 'quantity', 'price_per_unit', 'total_price', 'time_purchased', 'fulfillment_status']
purchases_df.columns = column_names
user_item_matrix = pd.pivot_table(purchases_df, values='quantity', index='uid', columns='pid', fill_value=0)


def get_similar_users(user_id, matrix):
   # Calculate cosine similarity between the user and all other users
   similarities = cosine_similarity(matrix, [matrix.loc[user_id]])
   # Sort users by similarity (excluding the user itself)
   similar_users = np.argsort(similarities[:, 0])[::-1][1:]
   return similar_users


def recommend_based_on_purchase_history(user_id, matrix, num_recommendations=5):
   # Get similar users
   similar_users = get_similar_users(user_id, matrix)
   real_similar_users = [user for user in similar_users if user in matrix.index]




   # Identify products that similar users have purchased but the target user has not
   recommended_products = matrix.columns[
       (matrix.loc[real_similar_users].sum(axis=0) > 0) & (matrix.loc[user_id] == 0)
   ].tolist()


   # Sort recommended products by the sum of purchases by similar users
   recommended_products = sorted(
       recommended_products,
       key=lambda pid: matrix.loc[real_similar_users, pid].sum(),
       reverse=True
   )


   return recommended_products[:num_recommendations]


@bp.route('/get_orders', methods=['GET', 'POST'])
def get_orders():
   user_id = current_user.id
   orderlist = Purchase.get_all(user_id)  # Assuming you want to get purchases associated with the user
   total_price = calculate_total_price(orderlist)
   return render_template('orders.html',
                          orderlist=orderlist,
                          humanize_time=humanize_time,
                          total_price=total_price,
                          user_id = user_id)

@bp.route('/get_orders_by_modifier', methods=['GET', 'POST'])
def get_orders_by_modifier():
    user_id = current_user.id
    seller_id = request.args.get('seller_id')  
    item_tag = request.args.get('item tag') 
    start_date = request.args.get('start_date')  
    end_date = request.args.get('end_date')  

    orderlist = Purchase.get_all_by_modifier(
        uid=user_id,
        seller_id=seller_id,
        item_tag=item_tag,
        start_date=start_date,
        end_date=end_date
    )
    total_price = calculate_total_price(orderlist)

    return render_template('orders.html',
                           orderlist=orderlist,
                           humanize_time=humanize_time,
                           total_price=total_price,
                           user_id=user_id)


                          
@bp.route('/get_specific_order/<int:order_id>', methods=['GET'])
def get_specific_order(order_id):
   user_id = current_user.id
   orderlist = Purchase.get_all_by_order(user_id, order_id) 
   total_price = calculate_total_price(orderlist)
   return render_template('orders.html',
                          orderlist=orderlist,
                          humanize_time=humanize_time,
                          total_price=total_price,
                          user_id = user_id,
                          order_id = order_id)
