from flask_login import AnonymousUserMixin
from .. import login_manager


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.confirmed = False

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
