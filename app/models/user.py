from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.balance = balance

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

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

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


    @staticmethod
    def update(uid, email, password, firstname, lastname, address, balance):
        try:
            rows = app.db.execute("""
    UPDATE Users
    SET email = :email, firstname = :firstname, lastname = :lastname, address = :address, balance = :balance, password = :password
    WHERE id = :uid
""",
                                  uid=uid,email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname,
                                  address=address, balance=balance)

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
