from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .model import Post, User

auth = Blueprint('auth', __name__)


@auth.route('/contact')
def contact():
    return render_template('contact.html', user=current_user)

@auth.route('/about')
def about():
    return render_template('about.html', user=current_user)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(str(user.password), password):
                flash("Logged in sucessfully", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password! Try Again.", category='error')
        else:
            flash(f"User with username '{username}' does not exist!", category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        age = request.form.get('age')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        gender = request.form.get('gender')
        
        usernameInDb = User.query.filter_by(username=username).first()
        if usernameInDb:
            flash(f"The Username '{username}' is already taken! Try another.")

        
        user = User.query.filter_by(email=email).first()
        if user:
            flash(f"User with email '{email}' already exist!", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category="error")
        elif len(firstName) < 2 or len(lastName) < 2:
            flash("Your name cannot be less than 2 characters", category="error")
        elif len(password1) < 7:
            flash("password must be greater than 6 characters", category="error")
        elif password1 != password2:
            flash("Password does not match", category="error")
        else:
            new_user = User(
                    email=email, 
                    username = username,
                    age = age,
                    firstName = firstName,
                    lastName = lastName, 
                    gender = gender,
                    password = generate_password_hash(password1, method='sha256')
                    )
            db.session.add(new_user)
            db.session.commit()
            flash("You have Successfully Created An Account !", category="success")


            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)


@auth.route('/create', methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        body = request.form.get('body')

        if len(title) < 4:
            flash("Tite is too Short!!!", category='error')
        elif len(body) < 10:
            flash("Post content is too short!!!", category='error')
        else:
            new_post = Post(title=title, body=body, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash("New Post Created!", category='success')
            
            return redirect(url_for('views.home'))
    
    return render_template('create_post.html', user=current_user)


@auth.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit(id):
    post = Post.query.filter_by(id=id).first()
    title = post.title
    body = post.body
    if request.method == "POST":
        new_title = request.form.get('title')
        new_body = request.form.get('body')

        if len(new_title) < 4:
            flash("Title is too Short!!!", category='error')
        elif len(new_body) < 10:
            flash("Article is too short!!!", category='error')
        else:
            post.title = new_title
            post.body = new_body
            db.session.commit()
            flash("You have successfully updated your post!", category='success')
            
            return redirect(url_for('views.home'))
    
    return render_template('edit.html', user=current_user, title=title, body=body)

