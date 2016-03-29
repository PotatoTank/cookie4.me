from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    rfid = db.Column(db.String(120), index=True, unique=True)
    cookies = db.Column(db.Integer, index=True, default=0)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # python 2
        except NameError:
            return str(self.id) # python 3

    def get_cookies(self):
        try:
            return unicode(self.cookies)
        except NameError:
            return str(self.cookies)

    def add_cookies(self, num):
        self.cookies = self.cookies + num

    def __repr__(self):
        return '<User %r>' % (self.nickname)

