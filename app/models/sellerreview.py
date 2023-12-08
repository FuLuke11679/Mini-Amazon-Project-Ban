from flask import current_app as app

#SellerReview class
class SellerReview:
    def __init__(self, id, uid, seller_uid, review, rating, upvotes, time_posted):
        self.id = id
        self.uid = uid
        self.seller_uid = seller_uid
        self.review = review
        self.rating = rating
        self.upvotes = upvotes
        self.time_posted = time_posted

    #get an individual seller review
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, seller_uid, review, rating
FROM SellerReviews
WHERE id = :id
''', id=id)

        return SellerReview(*(rows[0])) if rows else None

    #get all the seller reviews created by a given user since
    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
WHERE uid = :uid
AND time_posted >= :since
ORDER BY time_posted DESC
''', 
uid = uid, 
since = since)
        return [SellerReview(*row) for row in rows]

    #get the most recent five by a given user since
    @staticmethod
    def get_most_recent_five_by_uid(uid, since):
        rows = app.db.execute('''
SELECT *
FROM SellerReviews
WHERE uid = :uid
AND time_posted >= :since
ORDER BY time_posted DESC
LIMIT 5
''', 
uid = uid, 
since = since)
        return [SellerReview(*row) for row in rows]

    #get all the seller reviews based on the seller_uid
    @staticmethod
    def reviews_for_this_seller(seller_uid):
        rows = app.db.execute('''
            SELECT * FROM SellerReviews
            WHERE seller_uid = :seller_uid
            ORDER BY time_posted DESC
            ''', seller_uid=seller_uid
        )

        return  [SellerReview(*row) for row in rows] if rows else None

    #get the average rating based on seller uid
    @staticmethod
    def total_average(seller_uid):
        rows = app.db.execute('''
            SELECT AVG(rating) 
            FROM SellerReviews 
            WHERE seller_uid = :seller_uid 
            GROUP BY seller_uid;
            ''', seller_uid = seller_uid
        )

        return [round(row, 2) for row in rows[0]] if rows else None