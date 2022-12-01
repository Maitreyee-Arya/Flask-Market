from market import app, db
from market.models import Item
from flask import render_template, redirect, url_for, flash, session
from market.forms import RegisterForm, LoginForm, Add_Item, Edit_item
from market.models import User


@app.route('/')
@app.route('/home')
def home_page():
	return render_template("home.html")


@app.route('/market')
def market_page():
	if 'admin' in session or 'user' in session:
		items = Item.query.all()
		return render_template('market.html', items=items)
	else:
		flash(f'You need to login first to access the page', category='danger')
		return redirect(url_for('login_mode'))


@app.route('/register',methods=['GET','POST'])
def register_page():
	form = RegisterForm()
	if form.validate_on_submit():
		user_to_create = User(
							username = form.username.data,
							email = form.email.data,
							password = form.password.data
		)
		db.session.add(user_to_create)
		db.session.commit()
		session['user'] = form.username.data
		return redirect(url_for('market_page'))
	else:
		for err_msg in form.errors.values():
			flash(f"There was an error while creating an account : {err_msg}", category='danger')
	return render_template("register.html", form=form)


@app.route('/login_mode')
def login_mode():
	return render_template("login_mode.html")


@app.route('/user_login',methods=['GET','POST'])
def user_login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User.query.filter_by(username=username).first()
		if user and user.password==password:
			session['user'] = username
			return redirect(url_for('market_page'))
		else:
			flash(f'User name or password incorrect.',category='danger')
	else:
		for err_msg in form.errors.values():
			flash(err_msg,category='danger')
	return render_template("login.html",form=form)


@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.username.data=='admin' and form.password.data=='admin':
			session['admin'] = form.username.data
			return redirect(url_for('admin_home'))
		else:
			flash(f"username or password incorrect",category='danger')
		for err_msg in form.errors.values():
			flash(err_msg,category='danger')
	return render_template("login.html",form=form)


@app.route('/admin_home')
def admin_home():
	items = Item.query.all()
	return render_template("admin_home.html",items=items)


@app.route('/add_item',methods=['GET','POST'])
def add_item():
	form = Add_Item()
	if form.validate_on_submit():
		name = form.name.data
		price = form.price.data
		barcode = form.barcode.data
		desc = form.desc.data
		item = Item(name=name,price=price,barcode=barcode,desc=desc)
		db.session.add(item)
		db.session.commit()
		flash(f'Item added successfully',category='success')
		return redirect(url_for('admin_home'))
	else:
		for err_msg in form.errors.values():
			flash(err_msg,category='danger')
	return render_template("add_item.html",form=form)


@app.route('/edit_item/<int:id>',methods=['GET','POST'])
def edit_item(id):
	form = Edit_item()
	item = Item.query.filter_by(id=id).first()
	if form.validate_on_submit():
		item.name = form.name.data
		item.price = form.price.data
		item.barcode = form.barcode.data
		item.desc= form.desc.data
		db.session.commit()
		flash(f'Item updated successfully',category='success')
		return redirect(url_for('admin_home'))
	return render_template("edit_item.html", form = form,item=item)


@app.route('/delete_item/<int:id>')
def delete_item(id):
	item = Item.query.filter_by(id=id).first()
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('admin_home'))


@app.route('/logout')
def logout():
	if 'user' in session:
		session.pop('user')
	if 'admin' in session:
		session.pop('admin')
	return redirect(url_for('home_page'))