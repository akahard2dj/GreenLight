from flask_login import AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False

    def is_administrator(self):
        return False