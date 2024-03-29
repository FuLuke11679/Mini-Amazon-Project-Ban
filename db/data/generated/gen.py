from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
from datetime import timedelta

num_users = 100
num_products = 200
num_purchases = 1000
num_wishlistitems = 2200
num_sellers = 20
num_inventory = 1000
num_reviews_per_user = 20


Faker.seed(0)
fake = Faker()

#defines csv writer with dialect and quoting
def get_csv_writer(f):
    return csv.writer(f, quoting=csv.QUOTE_MINIMAL, dialect='unix')

#generates number of users by user input
def gen_users(num_users):
    usersStore = []
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
               print(f'{uid}', end=' ', flush=True)
            
            currentUser = {}
        
            profile = fake.profile()
            currentUser['profile'] = profile
        
            email = profile['mail']
            currentUser['email'] = email

            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            currentUser['password'] = password

            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            currentUser['firstname'] = firstname

            lastname = name_components[-1]
            currentUser['lastName'] = lastname
            
            address = profile['address']
            currentUser['address'] = address
            
            balance = 0
            currentUser['balance'] = balance 

            currentRow = [uid, email, password, firstname, lastname, address, balance]
            writer.writerow(currentRow)
            usersStore.append(currentUser)

        print(f'{num_users} generated')
    return(usersStore)
   

#generates all potential subtags
def generate_subtag(tag):
    # Define sub-categories for each main category
    subtags = {
        'Groceries': ['Frozen', 'Fruits', 'Vegetables', 'Candy'],
        'Basics': ['Clothing', 'Household', 'Personal Care'],
        'Music': ['Rock', 'Pop', 'Hip-Hop', 'Jazz'],
        'Books': ['Fiction', 'Non-Fiction', 'Science Fiction', 'Mystery'],
        'Tech': ['Electronics', 'Computers', 'Accessories'],
        'Pharmacy': ['Medicine', 'Healthcare', 'Vitamins'],
        'Fashion': ['Men\'s Clothing', 'Women\'s Clothing', 'Footwear']
    }
    
    return random.choice(subtags[tag])
#generates products by a number of products and number of available sellers
def gen_products(num_products, available_sellers):
    tags = ['Groceries', 'Basics', 'Music', 'Books', 'Tech', 'Pharmacy', 'Fashion']
    products = []
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            randAmount = fake.random_int(max=99)
            amount =  f'{str(randAmount)}'
            available = randAmount > 0 

            if available == True:
                available_pids.append(pid)
            photo_url = fake.image_url(width=640, height=480)
            seller_id = fake.random_element(elements=available_sellers)
            longDescription = fake.sentence(nb_words=100)
            tag = random.choice(tags)
            subtag = generate_subtag(tag)  # Generate subtag based on main tag
            writer.writerow([pid, name, price, amount, available, photo_url, seller_id, longDescription, tag, subtag])
           
            currentProduct = {
                "id": pid,
                "name": name,
                "price":price,
                "amount":amount,
                "available":available,
                "photo_url":photo_url,
                "seller_id":seller_id,
                "longDescription":longDescription,
                "tag":tag,
                "subtag":subtag
            }
            products.append(currentProduct)

        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids, products

#generates carts by a number of wishlist items, and available pids that have already been initialized
def gen_Carts(num_wishlistitems, available_pids):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        for id in range(num_wishlistitems):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_added = fake.date_time()
            quantity = fake.random_int(min = 1, max = 20)
            writer.writerow([id, uid, pid, time_added, quantity])
        print(f'{num_wishlistitems} generated')
    return

#generates inventory corresponding to the available sellers
def gen_inventory(num_inventory, available_pids, available_sellers):
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for id in range(num_inventory):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_element(elements=available_sellers)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_inventory} generated')
    return

#ggenerates sellers given a number of sellers and number of users
def gen_sellers(num_sellers, num_users):
    available_sellers = fake.random_elements(elements=[x for x in range(num_users)], unique=True, length=num_sellers)
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)    

        for i in range(num_sellers):
            if i % 2 == 0:
                print(f'{i}', end=' ', flush=True)
            available_sellers.append(available_sellers[i])
            writer.writerow([i, available_sellers[i]])
        print(f'{num_sellers} generated')
    return available_sellers
#generates purchases for an input of number of purchases and number of products
def gen_purchases(num_purchases, products):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)

        for oid in range(num_purchases//200):
            start_offset = 5 - oid
            end_offset = 4 - oid

            start_date = f'-{start_offset}y'
            end_date = f'-{end_offset}y' if oid < 4 else 'now'

            order_timestamp = fake.date_time_between(start_date=start_date, end_date=end_date)

            for id in range(oid * 200, (oid + 1) * 200):
                if id % 100 == 0:
                    print(f'{id}', end=' ', flush=True)

                uid = fake.random_int(min=0, max=num_users-1)
                product = random.choice(products)
                seller_id = product['seller_id']
                pid = product['id']
                name = product['name']
                photo_url = product['photo_url']
                tag = product['tag']
                quantity = fake.random_int(min=1, max=20)
                price_per_unit = float(product['price'])
                total_price = quantity * price_per_unit

                # Use the same timestamp for all purchases within the order
                time_purchased = order_timestamp

                fulfillment_status = random.choice(['Fulfilled', 'In Progress'])

                writer.writerow([id, uid, oid, seller_id, pid, name, photo_url, tag, quantity, price_per_unit, total_price, time_purchased, fulfillment_status])

        print(f'{num_purchases} generated')
    return

#defines gen_reviews as a function that generates fake reviews given inputs for products
def gen_reviews(users, num_reviews_per_user, num_users, available_pids):
    reviewDict = {
        "1": "abhors",
        "2": "hates",
        "3": "could care less either way about",
        "4": "likes",
        "5": "adores"
    }
    
    with open('Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        num_reviews = num_users * num_reviews_per_user
        for i in range(num_users):
            poss_pids = fake.random_elements(elements=available_pids, length=num_reviews_per_user, unique=True)
            for j in range(num_reviews_per_user):
                if (((i*num_reviews_per_user) + j) % 100 == 0):
                    print(f'{((i*num_reviews_per_user) + j)}', end=" ", flush=True)
                uid = i
                pid = poss_pids[j]
                rating = fake.random_int(min=1, max=5)
                review = f'{users[i]["firstname"]} {reviewDict[str(rating)]} this product!'
                time_purchased = fake.date_time()
                upvotes = fake.random_int(min=0, max=num_users-1)
                photo_url = fake.image_url(width=200, height=200)
                writer.writerow([((i*num_reviews_per_user) + j) , uid, pid, review, rating, upvotes, time_purchased, photo_url])
        print(f'{num_reviews} generated')
    return
#generates fake reviews for sellers given the following inputs
def gen_sellerReviews(users, num_reviews_per_seller, available_sellers, num_sellers, num_users):
    reviewDict = {
        "1": "abhors",
        "2": "hates",
        "3": "could care less either way about",
        "4": "likes",
        "5": "adores"
    }

    with open('SellerReviews.csv', 'w') as g:
        writer = get_csv_writer(g)
        print('SellerReviews...', end=' ', flush=True)
        num_sellerReviews = num_users * num_reviews_per_seller
        for i in range(num_users): 
            particular_sellers =  fake.random_elements(elements=available_sellers, length=num_reviews_per_seller, unique=True)
            #print(particular_sellers)
            for j in range(num_reviews_per_seller):
                if (((i*num_reviews_per_seller) + j) % 200 == 0):
                    print(f'{((i*num_reviews_per_seller) + j)}', end=" ", flush=True)
                uid = i
                seller_uid = particular_sellers[j]
                rating = fake.random_int(min=1, max=5)
                review = f'{users[i]["firstname"]} {reviewDict[str(rating)]} this seller!'
                time_purchased = fake.date_time()
                upvotes = fake.random_int(min=0, max=num_users-1)
                writer.writerow([((i*num_reviews_per_seller) + j), uid, seller_uid, review, str(rating), upvotes, time_purchased])
        print(f'{num_sellerReviews} generated')
    return

#executes all generate functions
users = gen_users(num_users)
available_sellers = gen_sellers(num_sellers, num_users)
num_reviews_per_seller = 2 #len(available_sellers) #num_of_sellerReviews_per_user
# poss_ids = fake.random_elements(elements=available_sellers, length=num_reviews_per_seller, unique=True)
available_pids, products = gen_products(num_products, available_sellers)
gen_purchases(num_purchases, products)
gen_Carts(num_purchases, available_pids)
gen_inventory(num_inventory, available_pids, available_sellers)
gen_reviews(users, num_reviews_per_user, num_users, available_pids)
gen_sellerReviews(users, num_reviews_per_seller, list(set(available_sellers)), num_sellers, num_users)
gen_Carts(num_purchases, available_pids)

