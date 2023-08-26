from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request
from base.models import User, Post
from base.users.forms import Registration, Login, UpdateAcountForm, RequestResetForm, ResetPasswordForm
from base import db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from base.users.utils import get_user_image_file, save_picture, send_reset_email

  
users = Blueprint('users',__name__)    



@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect (url_for('main.home'))
    form = Registration()
    if form.validate_on_submit():
        #hash the password
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password = hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)


@users.route('/login',methods=['GET', 'POST'])
def login():
    form = Login()
    
    if current_user.is_authenticated:
        return redirect (url_for('main.home'))
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect (url_for('main.home'))
        else:
            flash('Logged in not successful! Please check the details.', 'danger')
            
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect (url_for('main.home'))



@users.route('/account',methods=['GET', 'POST'])
@login_required
def account():
    form= UpdateAcountForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        if form.picture.data:  # Check if a new picture was uploaded
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
               
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    
    image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', 
                           title='account', 
                           image_file=image_file,
                           form=form
                           )
  


@users.route('/user/<string:username>')
@login_required
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    post = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    
    image_file = get_user_image_file(current_user)
    return render_template('userspost.html', post=post, image_file=image_file, user=user)





    
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    
    if current_user.is_authenticated:
        return redirect (url_for('main.home'))
    
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user) 
        
        flash('An email was sent with instructions to reset your password', 'info')
  
        return redirect(url_for('users.login'))
    
        # flash('An email was sent with instructions to reset your password', 'info')
        # return redirect(url_for('login'))
        
    return render_template('reset_request.html', title='Reset Password', form=form)



@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect (url_for('main.home'))   
    
    user  = User.verify_reset_token(token)
    
    if user is None:
        flash('this is an invalid expire token', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        #hash the password
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_password 
        db.session.commit()
        flash(f'Password updated', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('reset_token.html', title='Reset Password', form=form )

