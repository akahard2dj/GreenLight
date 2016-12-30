from flask import current_app
from flask_login import UserMixin

import random, string

from .role import Role
from .permission import Permission
from .. import db, login_manager
from . import password_hash as hashing


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# todo
# werkzeug.security uses a sha1 algorithm for hashing password.
# sha1 is not less safe than sha256


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    confirmation_code = db.Column(db.String(10))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    # todo
    # school name
    # member_since
    # last_seen

    def __init__(self, **kwargs):
        self.confirmation_code = ''.join(random.SystemRandom()
                                         .choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                                         for _ in range(7))

        try:
            self.username = kwargs['username']
        except KeyError:
            raise

        try:
            self.email = kwargs['email']
        except KeyError:
            raise

        try:
            self.password = kwargs['password']
        except KeyError:
            raise

        try:
            self.confirmed = kwargs['confirmed']
        except KeyError:
            pass

        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        #self.password_hash = generate_password_hash(password)
        self.password_hash = hashing.hashing_sha256(password)

    def verify_password(self, password):
        #return check_password_hash(self.password_hash, password)
        return hashing.check_hashing_sha256(self.password_hash, password)

    def reset_password(self, new_password):
        self.password = new_password
        db.session.add(self)

        return True

    def reset_username(self, new_username):
        self.username = new_username
        db.session.add(self)

    def to_json(self):
        json_user = {
            'username': self.username
        }
        return json_user

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def user_confirmed(self):
        self.confirmed = True

        db.session.add(self)
        return True

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        import random
        import string
        import forgery_py

        random.seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=''.join(random.SystemRandom()
                                   .choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                                   for _ in range(7)),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

