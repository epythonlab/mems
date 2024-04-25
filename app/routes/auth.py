# Import necessary modules and classes
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.users import User  # Make sure to import your User model


from app import db, login_manager
from . import auth_bp

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        uname = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(email=uname).first()

        if not user:
            flash("Sorry! Incorrect email or password!", 'danger')
            return redirect(url_for('auth_bp.login'))
        elif not check_password_hash(user.password, password):
            flash("Sorry! Password is incorrect or Your account is disabled.", 'danger')
            return redirect(url_for('auth_bp.login'))

        login_user(user)  # Log in the user
        # Debugging messages
        print("User:", user)
        print("Logged in successfully!")

        # Redirect to the index page or any other desired page
        return redirect(url_for('index_bp.index'))


# # Define your logout route
# @auth_bp.route('/logout')
# @login_required  # Protect this route, only logged-in users can access it
# def logout():
#     logout_user()  # Log out the user
#     return redirect(url_for('auth_bp.login'))  # Redirect to the login page

# # ... Define other routes like register, signup, change_password, etc.

# Protect unauthorized access
@auth_bp.route('/unauthorized')
def unauthorized():
    flash("Login to access this page.")
    return redirect(url_for('auth_bp.login'))

# # Load user for Flask-Login

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

# print(current_user.get_id())

@auth_bp.route('/register/', methods=['POST', 'GET'])
def register():
    return render_template('signup.html')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    # get form values
    email = request.form.get('username').strip()
    fname = request.form.get('fname').strip()
    lname = request.form.get('lname').strip()
    password = request.form.get('password').strip()
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exist.', 'danger')
        return redirect(url_for('auth_bp.register'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(first_name=fname, last_name=lname, email=email, password=generate_password_hash(password, method='sha256'), active=0)
    import uuid
    new_user.fs_uniquifier = uuid.uuid4()
    db.session.add(new_user)
    db.session.commit()

    # # # generate token for email confirmation
    # # token = s.dumps(email, salt='email-confirmation')
    # # send confirmation message
    # msg = Message('Confirm Email', recipients=[email])
    # link = url_for('auth_bp.verify_email', token=token, _external=True)
    # msg.body = 'Your link is {}'.format(link)
    # #mail.send(msg)
    # # retrieve user_id and role_id
    # user_datastore.add_role_to_user(email, 'author')
    # db.session.commit()
    # flash('Successfuly registered. The token is {}'.format(token), 'success')

    return redirect(url_for('auth_bp.login'))

# # confirm email
# @auth_bp.route('/verify_email/<token>')
# def verify_email(token):
#     try:
#         # load token
#         email = s.loads(token, salt='email-confirmation', max_age=20)
#         return 'The token works'
#     except exc.SignatureExpired:
#         return 'Signature Expired!'
#     except exc.BadTimeSignature:
#         return 'Signature does not match!'


"""Logout- redirect to login page"""
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

# """Handle unauthorized_handdler"""
# @login_manager.unauthorized_handler
# def unauthorized():
#     """Redirect unauthorized users to Login page."""
#     flash("Login to access this page.")
#     return redirect(url_for('auth_bp.login'))

"""Change an existing user's password."""
@auth_bp.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    try:
        if request.method=='POST':
            user = User.query.filter_by(id=current_user.id).first()
            if not check_password_hash(user.password, request.form.get('oldpassword')):
                flash("ይቅርታ! አሮጌው የይለፍ ቃል ተሳስተዋል። እባክዎ ደግመው ይሞክሩ!")
                return redirect(url_for('dashboard_bp.dashboard'))
            else:
                user.password = generate_password_hash(request.form['newpassword'], method='sha256')
                db.session.commit()
                flash('የይለፍ ቃል በትክክል ተቀይሯል።', 'success')
                return redirect(url_for('auth_bp.login'))


    except Exception as e:
        print(e)
        
