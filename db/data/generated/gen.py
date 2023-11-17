from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_sellers = 20
num_wishlistitems = 2200
num_sellers = 20
num_inventory = 1000
num_reviews_per_user = 20
num_reviews_per_seller = 100

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, quoting=csv.QUOTE_NONE, dialect='unix')


def gen_users(num_users):
    users = []
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            row = [uid, email, password, firstname, lastname]
            writer.writerow(row)
            users.append({"uid":uid, "email":email,"password":password,"firstname":firstname,"lastname":lastname})
        print(f'{num_users} generated')
    return(users)


def gen_products(num_products, available_sellers):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            randAmount = fake.random_int(max=10)
            amount =  f'{str(randAmount)}'
            available = randAmount > 0 
            if available == True:
                available_pids.append(pid)
            photo_url = fake.image_url(width=640, height=480)
            seller_id = fake.random_element(elements=available_sellers)
            writer.writerow([pid, name, price, amount, available, photo_url, seller_id])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

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
                writer.writerow([((i*num_reviews_per_user) + j) , uid, pid, review, rating, upvotes, time_purchased])
        print(f'{num_reviews} generated')
    return

def gen_sellerReviews(users, num_reviews_per_seller, available_sellers, num_sellers):
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
        num_sellerReviews = num_sellers * num_reviews_per_seller
        for i in range(num_sellers):
            #poss_ids = fake.random_element(elements=available_sellers, length=num_reviews_per_seller, unique=true)
            for j in range(num_reviews_per_seller):
                if (((i*num_reviews_per_seller) + j) % 200 == 0):
                    print(f'{((i*num_reviews_per_seller) + j)}', end=" ", flush=True)
                uid = i
                seller_uid = available_sellers[i]
                rating = fake.random_int(min=1, max=5)
                review = f'{users[i]["firstname"]} {reviewDict[str(rating)]} this seller!'
                time_purchased = fake.date_time()
                upvotes = fake.random_int(min=0, max=num_users-1)
                writer.writerow([((i*num_reviews_per_seller) + j), uid, seller_uid, review, str(rating), upvotes, time_purchased])
        print(f'{num_sellerReviews} generated')
    return


users = gen_users(num_users)
available_sellers = gen_sellers(num_sellers, num_users)
available_pids = gen_products(num_products, available_sellers)
gen_purchases(num_purchases, available_pids)
gen_Carts(num_purchases, available_pids)
gen_inventory(num_inventory, available_pids, available_sellers)
gen_reviews(users, num_reviews_per_user, num_users, available_pids)
gen_sellerReviews(users, num_reviews_per_seller, available_sellers, num_sellers)
gen_Carts(num_purchases, available_pids)

