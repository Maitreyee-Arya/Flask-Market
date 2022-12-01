from market import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(30), nullable = False, unique = True)
	email = db.Column(db.String(40), nullable = False, unique = True)
	password = db.Column(db.String(30), nullable = False)
	#items = db.relationship('Item', backref = 'owned_by', lazy = True)


class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False, unique = True)
	price = db.Column(db.Integer(), nullable = False)
	barcode = db.Column(db.String(12), nullable=False, unique = True)
	desc = db.Column(db.String(1024))
	#owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

	def __repr__(self):
		return f'Item {self.name}'