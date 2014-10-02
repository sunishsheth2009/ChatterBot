from app import db

class Chats(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(64), index = True, unique = True)
    answer = db.Column(db.String(120), index = True, unique = True)

    def __repr__(self):
        return '<Answer %r>' % (self.answer)


class Positive(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(64), index = True, unique = True)
    answer = db.Column(db.String(120), index = True, unique = True)

    def __repr__(self):
        return '<Answer %r>' % (self.answer)


class Negative(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(64), index = True, unique = True)
    answer = db.Column(db.String(120), index = True, unique = True)

    def __repr__(self):
        return '<Answer %r>' % (self.answer)

class Assertive(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(64), index = True, unique = True)
    answer = db.Column(db.String(120), index = True, unique = True)

    def __repr__(self):
        return '<Answer %r>' % (self.answer)

class Wikipedia(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(64), index = True, unique = True)
    answer = db.Column(db.String(120), index = True, unique = True)

    def __repr__(self):
        return '<Answer %r>' % (self.answer)

