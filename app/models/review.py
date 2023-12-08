from flask import current_app as app

#review class
class Review:
    def __init__(self, id, uid, pid, review, rating, upvotes, time_posted, photo_url):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.review = review
        self.rating = rating
        self.upvotes = upvotes
        self.time_posted = time_posted
        self.photo_url = photo_url

    #get a review based on the id
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, review, rating, upvotes, time_posted, photo_url
FROM Reviews
WHERE id = :id
''', id=id)

        return Review(*(rows[0])) if rows else None

    #get all reviews from a given user since
    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE uid = :uid
AND time_posted >= :since
ORDER BY time_posted DESC
''', 
uid = uid, 
since = since)
        return [Review(*row) for row in rows]

    #get five most recent reviews by a given user since
    @staticmethod
    def get_most_recent_five_by_uid(uid, since):
        rows = app.db.execute('''
    SELECT *
    FROM Reviews
    WHERE uid = :uid
    AND time_posted >= :since
    ORDER BY time_posted DESC
    LIMIT 5
    ''', 
    uid = uid, 
    since = since)
        return [Review(*row) for row in rows]

    #get reviews for a given product
    @staticmethod
    def get_by_product(pid):
        rows = app.db.execute('''
            SELECT *
            FROM Reviews
            WHERE pid = :pid
            ''', pid=pid
        )

        return  [Review(*row) for row in rows] if rows else None

    #get the top 3 most upvoted review on a product
    @staticmethod
    def get_top_3_helpful(pid):
        rows = app.db.execute('''
            SELECT *
            FROM Reviews
            WHERE pid = :pid
            ORDER BY upvotes DESC, time_posted DESC
            LIMIT 3
            ''', pid=pid
        )

        return  [Review(*row) for row in rows] if rows else None

    #get the all the reviews excepting the top 3 most popular ones for a product
    @staticmethod
    def get_reviews_minus_top_3(pid):
        rows = app.db.execute('''
            SELECT * FROM Reviews
            WHERE pid = :pid
            EXCEPT
            (SELECT *
            FROM Reviews
            WHERE pid = :pid
            ORDER BY upvotes DESC, time_posted DESC
            LIMIT 3)
            ORDER BY time_posted DESC
            ''', pid=pid
        )

        return  [Review(*row) for row in rows] if rows else None

    #get the total average rating for a given product
    @staticmethod
    def total_average(pid):
        rows = app.db.execute('''
            SELECT AVG(rating) 
            FROM Reviews 
            WHERE pid = :pid 
            GROUP BY pid;
            ''', pid=pid
        )

        return [round(row, 2) for row in rows[0]] if rows else None