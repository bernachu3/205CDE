#Requisite imports
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, RadioField, IntegerField, validators
from wtforms.validators import DataRequired, Email, ValidationError
from functools import wraps
import MySQLdb.cursors
import hashlib
import string

app = Flask(__name__)
app.secret_key = 'swordfish'

# Database connection details/configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gym'
mysql = MySQL(app)

#Redirects the user to the homepage 
@app.route('/')
def index():
    return redirect(url_for('home'))

#Homepage
@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM news ORDER  BY id DESC LIMIT  3;')
    data = cur.fetchall()
    return render_template('index.html', data=data)

#Function brings user to the features
@app.route('/features')
def features():
    return render_template('features.html')

#Function brings user to the pricing
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

#Function brings user to the merch
@app.route('/merch')
def merch():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM catalog;')
    data = cur.fetchall()
    return render_template('merch.html', data=data)

#Shopping cart for the merch store. Creates a table to hold the data in the server if one doesn't exist,
#Then inserts the value to store the actual items the user purchased
@app.route('/additem', methods=['GET', 'POST'])
def additem():

    if 'logged_in' in session :
        uid = session['id']
        item = request.args.get("item")
        price = request.args.get("price")
        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `user%s_cart` ( `item` VARCHAR(15) PRIMARY KEY, `amt` INT(4), `price` INT(4) )", (uid, ))
        cur.execute("INSERT INTO `user%s_cart` (`item`, `amt`, `price`) VALUES (%s, 1, %s) ON DUPLICATE KEY UPDATE amt = amt + 1", (uid, item, price, ))
        mysql.connection.commit()
        flash("Item added to cart.")
    else:
        flash("To buy something, please login or create an account first.")
    return redirect(url_for('merch'))


@app.route('/about')
def about():
    return render_template('about.html')

#For returning users to login this class stores the username and password
#To retrieve it from the SQL database
class LoginForm(FlaskForm):
    username     = StringField('Username', [validators.DataRequired(),validators.Length(min=4, max=100)])
    password     = PasswordField('New Password', [validators.DataRequired()])
    submit       = SubmitField("Submit")

#This formula takes the user to the login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    #Checks if a form has been submitted and error checking
    if form.validate_on_submit():
        #Hashes password for comparison
        encoded = form.password.data.encode()
        hashed = hashlib.sha256(encoded)
        hexed = hashed.hexdigest()
        #Grab data from MySQL database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (form.username.data, hexed, ))
        account = cursor.fetchone()
        if account:
            #Creates session data
            session['logged_in'] = True
            session['id']        = account['uid']
            session['username']  = account['username']
            #Brings user to the dashboard
            return redirect(url_for('myacc'))
        else:
            flash('No account was found with those credentials.')
            return redirect(url_for('login', form=form))
    return render_template('login.html', form=form)

#Wrapper to redirect user to login page if they attempt to access
#A page without being logged in
def login_needed(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please login before accessing that page.")
            return redirect(url_for('login'))

    return wrap

@app.route('/cart')
@login_needed
def cart():

    data = None

    uid = session['id']
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES LIKE 'user%s_cart'", (uid, ))
    result = cur.fetchone()
    if result:
        cur.execute("SELECT * FROM `user%s_cart`", (uid, ))
        data = cur.fetchall()
        cur.close()
        return render_template('cart.html', data=data)
    else :
        flash("You don't have anything in your cart.")
        return render_template('merch.html')

#This line is similar to add item, but a different redirect for the user who is already at the cart page
@app.route('/additem_cart', methods=['GET', 'POST'])
@login_needed
def additem_cart():

    uid = session['id']
    item = request.args.get("item")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE `user%s_cart` SET amt = amt + 1 WHERE item=%s", (uid, item, ))
    mysql.connection.commit()
    return redirect(url_for('cart'))

@app.route('/subtractitem_cart', methods=['GET', 'POST'])
@login_needed
def subtractitem_cart():

    uid = session['id']
    item = request.args.get("item")
    num = request.args.get("num")
    cur = mysql.connection.cursor()

    if num == '1':
        cur.execute("DELETE FROM `user%s_cart` WHERE item=%s", (uid, item, ))
    else:
        cur.execute("UPDATE `user%s_cart` SET amt = amt - 1 WHERE item=%s", (uid, item, ))

    mysql.connection.commit()
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_needed
def checkout():

    flash("Your order has been received and your account will be charged. Please make sure your credit card information is correct and up to date.")
    return redirect(url_for('myacc'))

# Class for new account registration form
class RegForm(FlaskForm):
    username = StringField(
        'Username', [validators.DataRequired(), validators.Length(min=4, max=100)])
    email = EmailField('Email Address', [
                       validators.DataRequired(), validators.Length(min=6, max=100)])
    password = PasswordField('New Password', [validators.DataRequired(
    ), validators.EqualTo('confirmpw', message='Passwords must match')])
    confirmpw = PasswordField('Confirm Password', [validators.DataRequired()])
    accept_tos = BooleanField('I accept the site rules', [
                              validators.DataRequired()])
    newsletter = BooleanField('Yes, sign me up for the newsletter')
    submit = SubmitField("Submit")

# Method for registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = RegForm()

    # Checks if a form has been submitted and error checking
    if form.validate_on_submit():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = % s', (form.username.data, ))
        account = cursor.fetchone()
        # Checks for username clash
        if account:
            flash('Error: Account already exists')
            return redirect(url_for('register'))
        else:
            encoded = form.password.data.encode()
            hashed = hashlib.sha256(encoded)
            hexed = hashed.hexdigest()
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, 0)',
               (form.username.data, hexed, form.email.data, form.newsletter.data, ))
            mysql.connection.commit()
            cursor.close()
            flash('You have successfully registered. Please sign in.')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

#Class for new account registration form
class RegForm(FlaskForm):
    username     = StringField('Username', [validators.DataRequired(),validators.Length(min=4, max=100)])
    email        = EmailField('Email Address', [validators.DataRequired(),validators.Length(min=6, max=100)])
    password     = PasswordField('New Password', [validators.DataRequired(),validators.EqualTo('confirmpw', message='Passwords must match')])
    confirmpw    = PasswordField('Confirm Password', [validators.DataRequired()])
    accept_tos   = BooleanField('I accept the site rules', [validators.DataRequired()])
    newsletter   = BooleanField('Yes, sign me up for the newsletter')
    submit       = SubmitField("Submit")

#Method for registration
@app.route('/signup', methods=['GET', 'POST'])
def register():

    form = RegForm()

    #Checks if a form has been submitted and error checking
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (form.username.data, ))
        account = cursor.fetchone()
        #Checks for username clash
        if account:
            flash('Error: Account already exists')
            return redirect(url_for('register'))
        else:
            encoded = form.password.data.encode()
            hashed = hashlib.sha256(encoded)
            hexed = hashed.hexdigest()
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s)',
                           (form.username.data, hexed, form.email.data, form.newsletter.data, ))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('login'))

    return render_template('signup.html', form=form)

#Class to take in user's credit card details
class JoinForm(FlaskForm):

    def validate_ccnumber(form, field):

        sum = 0
        oddeven = 16 & 1
        for i in range(0, 16):
            digit = int(field.data[i])
            if not ((i & 1) ^ oddeven):
                digit = digit * 2
            if digit > 9:
                digit = digit - 9

            sum = sum + digit

        if (sum % 10 != 0):
            flash('That does not appear to be a valid credit card number.')
            raise ValidationError()
            
    ccname       = StringField('Name on Credit Card', [validators.DataRequired(), validators.Length(min=10, max=100)])
    ccnumber     = StringField('Credit Card Number', [validators.DataRequired(), validators.Length(min=16, max=16)])
    cvv          = StringField('CVV', [validators.DataRequired(), validators.Length(min=3, max=3)])
    expiry       = IntegerField('Expiration date', [validators.DataRequired()])
    plan         = RadioField('Plan', choices = [('1','Monthly'), ('2','Annual'), ('3','10 Years')])
    submit       = SubmitField("Submit")

#Method to get user's credit card information
@app.route('/join', methods=['GET', 'POST'])
@login_needed
def join():

    form = JoinForm()
    arg = request.args.get("plan")
    arg = int(arg) + 1

    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE `accounts` SET `plan` = % s WHERE `accounts`.`username` = % s ',
                           (form.plan.data, session['username'], ))
        mysql.connection.commit()
        cursor.close()
        flash('Your credit card information has been processed and your billing cycle updated. Thanks for supporting us!')
        return redirect(url_for('myacc'))

    return render_template('join.html', form=form, arg=arg)

@app.route("/logout")
@login_needed
def logout():
    # Removes session data, logs out the current user
   session.pop('logged_in', None)
   session.pop('id', None)
   session.pop('username', None)
   #Informs user of successful logout
   flash('You have been logged out successfully.')
   # Bring user back to login page
   return redirect(url_for('login'))

@app.route('/myacc')
@login_needed
def myacc():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT `accounts`.`plan` FROM `accounts` WHERE `username` = % s', (session['username'], ))
    plan = cursor.fetchone()
    cursor.execute('SELECT * FROM `coach` WHERE `username` = % s', (session['username'], ))
    coaches = cursor.fetchall()
    cursor.execute('SELECT * FROM `room` WHERE `username` = % s', (session['username'], ))
    rooms = cursor.fetchall()
    cursor.close()

    return render_template('myacc.html', plan=plan, coaches=coaches, rooms=rooms)

@app.route('/room')
@login_needed
def room():
    return render_template('room.html')

@app.route('/confirmRoom')
@login_needed
def confirmRoom():

    day = request.args.get("day")

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO `room`(`username`,`day`) VALUES (% s, % s)', (session['username'], day, ))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('myacc'))

@app.route('/coach')
@login_needed
def coach():
    return render_template('coach.html')

@app.route('/confirmCoach')
@login_needed
def confirmCoach():

    day = request.args.get("day")

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO `coach`(`username`,`day`) VALUES (% s, % s)', (session['username'], day, ))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('myacc'))

@app.route('/changeBooking')
@login_needed
def changeBooking():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM `coach` WHERE `username` = % s', (session['username'], ))
    coaches = cursor.fetchall()
    cursor.execute('SELECT * FROM `room` WHERE `username` = % s', (session['username'], ))
    rooms = cursor.fetchall()
    cursor.close()

    return render_template('dbook.html', coaches=coaches, rooms=rooms)

@app.route('/cancelRoom')
@login_needed
def cancelRoom():

    day = request.args.get("day")

    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM `room` WHERE `username` = % s and `day` = % s', (session['username'], day, ))
    mysql.connection.commit()
    cursor.execute('SELECT * FROM `coach` WHERE `username` = % s', (session['username'], ))
    coaches = cursor.fetchall()
    cursor.execute('SELECT * FROM `room` WHERE `username` = % s', (session['username'], ))
    rooms = cursor.fetchall()
    cursor.close()

    flash('Action successful.')

    return render_template('dbook.html', coaches=coaches, rooms=rooms)

@app.route('/cancelCoach')
@login_needed
def cancelCoach():

    day = request.args.get("day")

    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM `coach` WHERE `username` = % s and `day` = % s', (session['username'], day, ))
    mysql.connection.commit()
    cursor.execute('SELECT * FROM `coach` WHERE `username` = % s', (session['username'], ))
    coaches = cursor.fetchall()
    cursor.execute('SELECT * FROM `room` WHERE `username` = % s', (session['username'], ))
    rooms = cursor.fetchall()
    cursor.close()

    flash('Action successful.')

    return render_template('dbook.html', coaches=coaches, rooms=rooms)

#Class to change password
class ChangePWForm(FlaskForm):
    password     = PasswordField('New Password', [validators.DataRequired(),validators.EqualTo('confirmpw', message='Passwords must match')])
    confirmpw    = PasswordField('Confirm Password', [validators.DataRequired()])
    submit       = SubmitField("Submit")

#Method to change password
@app.route('/changepw', methods=['GET', 'POST'])
@login_needed
def changepw():

    form = ChangePWForm()

    if request.method == 'POST' and form.validate():
        encoded = form.password.data.encode()
        hashed = hashlib.sha256(encoded)
        hexed = hashed.hexdigest()
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE `accounts` SET `password` = % s WHERE `accounts`.`username` = % s ', (hexed, session['username'], ))
        mysql.connection.commit()
        cursor.close()
        flash('Password changed successfully.')
        return redirect(url_for('myacc'))

    return render_template('changepw.html', form=form)

#The following two routes handle the user changing their selected billing plan
@app.route('/changeplan')
@login_needed
def changeplan():
    return render_template('changeplan.html')

@app.route('/updateplan')
@login_needed
def updatePlan():

    num = request.args.get('num')

    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE `accounts` SET `plan` = % s WHERE `accounts`.`username` = % s ', (num, session['username'], ))
    mysql.connection.commit()
    cursor.close()
    flash('You have changed your plan successfully.')

    return redirect(url_for('myacc'))

# Runs only if not called from another file
if __name__ =="__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=9163)