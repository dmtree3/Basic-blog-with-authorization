from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, title='Home', posts=posts)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash("Post can't be empty", category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category='success')
            return redirect(url_for('views.home'))
    return render_template('create-post.html', title='Create a post', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist", category='error')
    elif current_user.id != post.user.id:
        flash('No permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')
    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Username does not exist', category='error')
        return redirect(url_for('views.home'))
    posts = Post.query.filter_by(author=user.id).all()
    return render_template('post.html', user=current_user, posts=posts, username=username)


@views.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Profile does not exist', category='error')
        return redirect(url_for('views.home'))
    return render_template('profile.html', user=user, username=username)


@views.route("/comments/<username>")
@login_required
def comments(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Username does not exist', category='error')
        return redirect(url_for('views.home'))
    comments = Comment.query.filter_by(author=user.id).all()
    return render_template('comments.html', user=user, comments=comments, username=username)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash("Comment can't be empty", category='error')
    else:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Comment created', category='success')
        else:
            flash('Post does not exist', category='error')
    return redirect(url_for('views.home'))


@views.route("/post/<post_id>")
@login_required
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        flash('Post with that id does not exist', category='error')
        return redirect(url_for('views.home'))
    return render_template('single-post.html', post=post, user=current_user)


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist', category='error')
    elif comment.author != current_user.id and comment.post.author != current_user.id:
        flash("You don't have permission to delete that comment", category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted")
    return redirect(url_for('views.home'))



