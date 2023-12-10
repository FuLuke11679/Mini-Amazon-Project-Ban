from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash


from .. import login



#initializes user
class User(UserMixin):
   def __init__(self, id, email, firstname, lastname, address, balance):
       self.id = id
       self.email = email
       self.firstname = firstname
       self.lastname = lastname
       self.address = address
       self.balance = balance

#searches for user by email. IF not found return Email not found.
#if pw incorrect return incorrect password. Other than that return Login successful
   @staticmethod
   def get_by_auth(email, password):
       rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance
FROM Users
WHERE email = :email
""",
                             email=email)
       if not rows: 
           # email not found
           return None, 'Email not found'
       elif not check_password_hash(rows[0][0], password):
           # incorrect password
           return None, 'Incorrect password'
       else:
           return User(*(rows[0][1:])), 'Login successful!'

#checks if an email already exists among current users
   @staticmethod
   def email_exists(email):
       rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                             email=email)
       return len(rows) > 0

#user registration and returns user's id
   @staticmethod
   def register(email, password, firstname, lastname, address, balance):
       try:
           rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address, balance)
VALUES(:email, :password, :firstname, :lastname, :address, :balance)
RETURNING id
""",
                                 email=email,
                                 password=generate_password_hash(password),
                                 firstname=firstname, lastname=lastname,
                                 address=address, balance=balance)
           id = rows[0][0]
           return User.get(id)
       except Exception as e:
           return None



#updates user information to inputs
   @staticmethod
   def update(uid, email, password, firstname, lastname, address):
       try:
           rows = app.db.execute("""
   UPDATE Users
   SET email = :email, firstname = :firstname, lastname = :lastname, address = :address, password = :password
   WHERE id = :uid
""",
                                 uid=uid,email=email,
                                 password=generate_password_hash(password),
                                 firstname=firstname, lastname=lastname,
                                 address=address)


           return True
       except Exception as e:
           return False

#updates balance of user through user id to the balance input
   @staticmethod
   def update_balance(uid, balance):
       try:
           rows = app.db.execute("""
   UPDATE Users
   SET balance = :balance
   WHERE id = :uid
""",
                                 uid=uid, balance=balance)


           return True
       except Exception as e:
           return False

#updates balance by subtracting the user's balance.
   @staticmethod
   def updateBal(uid, subtract):
       try:
           rows = app.db.execute("""
   UPDATE Users
   SET balance = balance - :subtract
   WHERE id = :uid
""",
                                 uid = uid,
                                 subtract = subtract)


           return True
       except Exception as e:
           return False
















   @staticmethod
   @login.user_loader
   def get(id):
       rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, balance
FROM Users
WHERE id = :id
""",
                             id=id)
       return User(*(rows[0])) if rows else None
