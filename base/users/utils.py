import os
import secrets
from PIL import Image
from flask import url_for   
from flask_mail import Message
from base import mail
from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    
    output = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output)
    i.save(picture_path)
    
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not request this, just ignore this and no changes have been made!
    '''
    
    try:
        mail.send(msg)
        print("Email sent successfully!")  # Add this line to indicate that the email was sent
    except Exception as e:
        print(f"Email sending failed: {e}")  # Print any error that occurs while sending the email


def get_user_image_file(current_user):
    if current_user.is_authenticated:
        return url_for('static', filename="profile_pics/" + current_user.image_file)
    return None


