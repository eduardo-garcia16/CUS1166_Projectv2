from flask import render_template, flash, redirect, url_for, request, current_app
from app.main.forms import EditProfileForm, BookForm, ItemForm, EditBookForm, EditItemForm
from app.models import User, Book, Item
from flask_login import current_user, login_required
from app import db
from datetime import datetime
from app.main import bp

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET','POST'])
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    books = user.books
    items = user.items
    return render_template('user.html', user=user, books=books, items=items)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@bp.route('/new_book', methods=['GET', 'POST'])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, description=form.description.data, revenue=form.revenue.data, creator = current_user.username)
        db.session.add(book)
        db.session.commit()
        flash('Congratulations, you have added a new BudgetBook!')
        return redirect(url_for('main.user', username=current_user.username))

    return render_template('new_book.html', form=form)

@bp.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    form = EditBookForm()
    current_book = Book.query.filter_by(id=book_id).first_or_404()
    if form.validate_on_submit():
        current_book.title = form.title.data
        current_book.description = form.description.data
        current_book.revenue = form.revenue.data
        db.session.add(current_book)
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.title.data = current_book.title
        form.description.data = current_book.description
        form.revenue.data = current_book.revenue
    return render_template("edit_book.html", form=form, book_id=id)

@bp.route('/book/remove/<int:book_id>', methods=['GET', 'POST'])
@login_required
def remove_book(book_id):
    Book.query.filter(Book.id==book_id).delete()
    db.session.commit()

    return redirect(url_for('main.user', username=current_user.username))

@bp.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(item=form.item.data, purchased=form.purchased.data, creator=current_user.username)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))

    return render_template('new_item.html',form=form)

@bp.route('/item/edit/<int:item_id>', methods=['GET','POST'])
@login_required
def edit_item(item_id):
    form = EditItemForm()
    current_item = Item.query.filter_by(id=item_id).first_or_404()
    if form.validate_on_submit():
        current_item.item =  form.item.data
        current_item.purchased = form.purchased.data
        db.session.add(current_item)
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.item.data = current_item.item
        form.purchased.data = current_item.purchased
    return render_template("edit_item.html", form=form, item_id=id)

@bp.route('/item/remove/<int:item_id>', methods=['GET', 'POST'])
@login_required
def remove_item(item_id):
    Item.query.filter(Item.id==item_id).delete()
    db.session.commit()

    return redirect(url_for('main.user', username=current_user.username))
