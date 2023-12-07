from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_wishlistitems = 2200
num_sellers = 20
num_inventory = 1000

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, quoting=csv.QUOTE_NONE, dialect='unix')


def gen_users(num_users):
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
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
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
            writer.writerow([pid, name, price, amount, available])
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

def gen_sellers(num_sellers):
    available_sellers = []
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)    
        for uid in range(num_sellers):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            available_sellers.append(uid)
            writer.writerow([uid])
        print(f'{num_users} generated')
    return available_sellers
            

def gen_inventory(num_inventory, available_pids, available_sellers):
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for id in range(num_inventory):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_element(elements=available_sellers)
            pid = fake.random_element(elements=available_pids)
            time_purchased = fake.date_time()
            quantity = fake.random_int(min = 1, max = 20)
            writer.writerow([id, uid, pid, time_purchased, quantity])
        print(f'{num_purchases} generated')
    return

gen_users(num_users)
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids)
gen_Carts(num_purchases, available_pids)
available_sellers = gen_sellers(num_sellers)
gen_inventory(num_inventory, available_pids, available_sellers)
