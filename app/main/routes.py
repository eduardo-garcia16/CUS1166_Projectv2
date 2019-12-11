from flask import render_template, flash, redirect, url_for, request, current_app
from app.main.forms import EditProfileForm, BookForm, EditBookForm
from app.models import User, Book
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
@login_required
def index():
    return render_template('index.html')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    books = user.books
    return render_template('user.html', user=user, books=books)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
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

#@app.route('/edit_book', methods=['GET', 'POST'])
#@login_required
#def edit_book():
#    form =
