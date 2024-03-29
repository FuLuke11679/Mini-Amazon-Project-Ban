from flask import render_template, redirect, url_for, flash, request, get_flashed_messages
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import DateField, RadioField, FloatField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .models.review import Review 
from .models.sellerreview import SellerReview
import datetime
from humanize import naturaltime

from flask import current_app as app


from wtforms.fields.simple import HiddenField


from .models.user import User
from .models.purchase import Purchase



from flask import Blueprint
bp = Blueprint('users', __name__)


def humanize_time(dt):
   return naturaltime(datetime.datetime.now() - dt)

#defines class for login form
class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')







#routing to login page and references index.index 
@bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
      return redirect(url_for('index.index'))
    
  get_flashed_messages()
  form = LoginForm()
  if form.validate_on_submit():
      user, message = User.get_by_auth(form.email.data, form.password.data)
      if user:
          login_user(user)
          next_page = request.args.get('next')
          if not next_page or url_parse(next_page).netloc != '':
              next_page = url_for('index.index')
              return redirect(next_page)




      else:
          flash(message, 'error')
          return redirect(url_for('users.login'))




    
  return render_template('login.html', title='Sign In', form=form)



#The TopUpForm class is a FlaskForm used to create a form for changing a user's balance, 
# incorporates validation for non-negative amounts and fields for credit card information.
class TopUpForm(FlaskForm):
  def validate_amount(form, field):
     if field.data and float(field.data) < 0:
         raise ValidationError('Amount must be non-negative!')
  #only update with 0 or positive amounts


  amount = FloatField('Amount', validators=[DataRequired()])
  action = RadioField('Action', choices = [('deposit', 'Deposit'), ('withdraw', 'Withdraw')], validators=[DataRequired()])


  credit_card_number = StringField('Credit Card Number', validators=[Length(min=15, max=16)])
  cvv = StringField('CVV', validators=[Length(min=3, max=4), DataRequired()], )
  expiry_date = DateField('Expiry Date', format='%Y-%m-%d', validators=[DataRequired()])




  submit = SubmitField('Change balance')








class UpdateInfoForm(FlaskForm):

#checks if an email is already in use when updating info
  def validate_email(self, email):
      if email.data:
          if email.data != current_user.email and User.email_exists(email.data):
              raise ValidationError('Email is already in use. Choose a different one.')




  firstname = StringField('First Name')
  lastname = StringField('Last Name')
  email = StringField('Email')
  address = StringField('Address')
  password = PasswordField('New Password', validators = [DataRequired()])
  password2 = PasswordField(
      'Repeat Password', validators=[DataRequired(),
                                     EqualTo('password',
                                     message='Passwords must match')]
  )




  submit = SubmitField('Update Profile')








class RegistrationForm(FlaskForm):



#checks if registered balance is 0
  def validate_balance(form, field):
     if field.data != 0:
         raise ValidationError('Balance must be 0!')
  #this is to make sure you can only register with a balance of 0




  firstname = StringField('First Name', validators=[DataRequired()])
  lastname = StringField('Last Name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  address = StringField('Address', validators=[DataRequired()])
  balance = FloatField('Balance', validators=[DataRequired(), validate_balance])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
      'Repeat Password', validators=[DataRequired(),
                                     EqualTo('password',
                                     message='Passwords must match')])
  submit = SubmitField('Register')



#checks if a user with this email already exists when registering
  def validate_email(self, email):
      if User.email_exists(email.data):
          raise ValidationError('Already a user with this email.')







#routing for registering
@bp.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
      form = UpdateInfoForm()
      if form.validate_on_submit():
      # Update user information in the database if not blank
          email = form.email.data if form.email.data else current_user.email
          password = form.password.data if form.password.data else current_user.password
          firstname = form.firstname.data if form.firstname.data else current_user.firstname
          lastname = form.lastname.data if form.lastname.data else current_user.lastname
          address = form.address.data if form.address.data else current_user.address




          if User.update(current_user.id, #pass current userid as identifying element
                      email,
                      password,
                      firstname,
                      lastname,
                      address):
                    
              return redirect(url_for('index.index'))



#if form is validated on submitting and submission works, redirects to login page
  else:
      form = RegistrationForm()
      if form.validate_on_submit():
          if User.register(form.email.data,
                          form.password.data,
                          form.firstname.data,
                          form.lastname.data,
                          form.address.data,
                          form.balance.data):
              flash('Congratulations, you are now a registered user! Login to your profile!')
              return redirect(url_for('users.login'))
  return render_template('register.html', title='Register', form=form)







#route for top_up. Defines functions to deposit or withdraw from/to balance
@bp.route('/top_up', methods=['GET', 'POST'])
def top_up():
  form = TopUpForm()
  if form.validate_on_submit():
      action = form.action.data
      amount = form.amount.data


      if action == 'deposit':
           balance = current_user.balance + amount
           if User.update_balance(current_user.id, balance):
              return redirect(url_for('users.myprofile'))
      elif action == 'withdraw':
          if amount <= current_user.balance:
               balance = current_user.balance - amount
               User.update_balance(current_user.id, balance)
               return redirect(url_for('users.myprofile'))  # Redirect to the user's profile page
  
          else:
              return redirect(url_for('users.myprofile'))  # Redirect to the user's profile page
  else:
      return render_template('top_up.html', title='Topup', form=form)





#defines logging out routing and points back to index.index
@bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index.index'))



#defines route to myprofile and renders myprofile.html template with reviews, sellerreviews, and time.
@bp.route('/myprofile')
def myprofile():
    if current_user.is_authenticated:
        reviews = Review.get_all_by_uid_since(current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        sellerReviews = SellerReview.get_all_by_uid_since(current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        reviews = None
        sellerReviews = None

    # print(reviews)

    return render_template('myprofile.html', 
                        reviews=reviews,
                        sellerReviews=sellerReviews,
                        humanize_time=humanize_time)





#defines route for a public profile of a user. Renders template 
#with whether or not a user is a seller and other subsequent information
@bp.route('/publicprofile/<int:user_id>', methods = ['GET'])
def publicprofile(user_id):
    #user_id = request.form['user_id']
    seller = is_seller(user_id)
    userInfo = User.get(user_id)
    
    average_rating_a = SellerReview.total_average(user_id)
    if average_rating_a == None:
        average_rating = None
    else:
        average_rating = average_rating_a[0]
    
    reviews_for_this_seller = SellerReview.reviews_for_this_seller(user_id)
    num_of_reviews = len(reviews_for_this_seller or "")


    return render_template('publicprofile.html',
                    user_id = user_id, 
                    userInfo = userInfo, 
                    seller = seller,
                    reviews_for_this_seller=reviews_for_this_seller,
                    humanize_time=humanize_time,
                    average_rating = average_rating,
                    num_of_reviews=num_of_reviews)




#defines routing for user_search. Renders profile page displaying the corresponding user information
@bp.route('/user_search', methods=['GET', 'POST'])
def user_search():
    if request.method == 'POST':
        user_id = request.form['user_id']
        seller = is_seller(user_id)
        userInfo = User.get(user_id)

        #get all reviews and number of reviews for a seller
        reviews_for_this_seller = SellerReview.reviews_for_this_seller(user_id)
        num_of_reviews = len(reviews_for_this_seller  or "")

        #average rating of seller for summary info
        average_rating_a = SellerReview.total_average(user_id)
        if average_rating_a == None:
            average_rating = None
        else:
            average_rating = average_rating_a[0]

        return render_template('publicprofile.html',
                    user_id = user_id, 
                    userInfo = userInfo, 
                    seller = seller,
                    reviews_for_this_seller=reviews_for_this_seller,
                    humanize_time=humanize_time,
                    num_of_reviews = num_of_reviews,
                    average_rating = average_rating)
    else:
        return render_template('index.html')


#determines whether or not a user is a seller.
def is_seller(user_id):
  rows = app.db.execute('''
      SELECT id FROM Sellers
      WHERE uid = :user_id
  ''', user_id=user_id)




  return bool(rows)
