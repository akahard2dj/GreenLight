from datetime import datetime
from app.models.user import User
from .. import db


class Post(db.Model):
    __tablename__ = 'posts'
    read_counts = db.Column(db.Integer, default=0)
    comment_counts = db.Column(db.Integer, default=0)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def increase_read_count(self, updated_counts):
        self.read_counts = updated_counts
        db.session.add(self)

        return True

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     title=forgery_py.lorem_ipsum.sentence(),
                     timestamp=forgery_py.date.date(True),
                     author_id=u.id)
            print(p.body, p.timestamp, p.author_id)
            db.session.add(p)
            db.session.commit()

        u = User.query.offset(10).first()
        p = Post(body='와우',
                 title='이거 레알',
                 timestamp=forgery_py.date.date(True),
                 author_id=u.id)
        db.session.add(p)
        db.session.commit()