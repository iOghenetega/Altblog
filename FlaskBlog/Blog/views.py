from flask import Blueprint, render_template
from flask_login import current_user, login_required

from .model import Post

views = Blueprint('views', __name__)

@views.route('/')
#view all posts
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=posts)

@views.route('/post/<int:id>')
#view single post
def view_post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('post.html', post=post, user=current_user)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route('/contact')
def contact():
    return render_template('contact.html', user=current_user)
