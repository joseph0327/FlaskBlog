from flask import render_template, url_for, request
from base.models import Post
from flask_login import login_user, current_user
from base.users.utils import get_user_image_file  
from flask import Blueprint

main = Blueprint('main',__name__)    

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page',1,type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    image_file = get_user_image_file(current_user)
    return render_template('home.html', post=post, image_file=image_file)


@main.route('/about')
def about():

    image_file = None
    if current_user.is_authenticated:
        image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
        
    return render_template('about.html', title='about', image_file=image_file)