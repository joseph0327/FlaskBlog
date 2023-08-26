from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, abort
from base.models import Post
from base.post.forms import PostForm
from base import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from base.users.utils import get_user_image_file



post = Blueprint('post',__name__)    
  
  
@post.route('/post/<int:post_id>')
@login_required
def posts(post_id):
    post = Post.query.get_or_404(post_id)
    
    image_file = get_user_image_file(current_user)
    
    return render_template('post.html', title=post.title , post=post, image_file=image_file)

@post.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    
    if form.validate_on_submit():
        post = Post(title =form.title.data, content = form.content.data, author= current_user  )
        db.session.add(post)
        db.session.commit()
        
        flash("Your post has been submitted", "success")
        return redirect(url_for('main.home'))
    
    image_file = get_user_image_file(current_user)
    return render_template('createpost.html', title='New Post', form=form, image_file=image_file)





@post.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        
        flash('Your post has been updated', 'success')
        return redirect(url_for('main.home'))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('createpost.html', title='Update Post', form=form)


@post.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('main.home'))

