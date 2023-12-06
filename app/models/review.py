from flask import current_app as app

class Review:
    def __init__(self, id, uid, pid, review, rating, upvotes, time_posted):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.review = review
        self.rating = rating
        self.upvotes = upvotes
        self.time_posted = time_posted

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, review, rating
FROM Reviews
WHERE id = :id
''', id=id)

        return Review(*(rows[0])) if rows else None

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

    @staticmethod
    def get_by_product(pid):
        rows = app.db.execute('''
            SELECT *
            FROM Reviews
            WHERE pid = :pid
            ''', pid=pid
        )

        return  [Review(*row) for row in rows] if rows else None

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