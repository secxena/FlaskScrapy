#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, flash,render_template,redirect,url_for,request,session
from flask import send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import logging,csv,os
from functools import wraps
from sqlalchemy.exc import IntegrityError
from logging import Formatter, FileHandler
from forms import *
from models import db,app,bcrypt,User

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# Automatically tear down SQLAlchemy.

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()


# Login required decorator.

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#if already logged in redirect to dashboard

def already_in(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('dashboard'))
        else:
            return test(*args, **kwargs)
    return wrap

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/home')
@app.route('/index')
@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/register',methods=['POST','GET'])
def register():
    error = None
    status_code=200
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            new_user = User(form.name.data,form.email.data,bcrypt.generate_password_hash(form.password.data))
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering.')
                return redirect(url_for('login'))
            except IntegrityError:
                error = 'That username and/or email already exists'
                return render_template('forms/register.html',error=error,form=form)
    return render_template('forms/register.html', form=form, error=error),status_code


@app.route('/login',methods=['POST','GET'])
@already_in
def login():
    error=None
    status_code=200
    form = LoginForm(request.form)
    if request.method=='POST':
        if form.validate():
            user =User.query.filter_by(name=request.form['name']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['name'] = user.name
                flash('Welcome!')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid username or password.'
        else:
            error = 'Both fields are required.'
    return render_template('forms/login.html', form=form, error=error),status_code


@app.route('/dashboard')
@login_required
def dashboard():
    '''rendering the data of given csv file into a table on dashboard'''

    error = None
    with open('Test-Orders_DB.csv', 'rU') as infile:
        reader = csv.DictReader(infile)
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    if header == 'cost_price':
                        try:
                            value = float(value)*66 #dollar value $1=66INR
                            value = round(value,1)  #price rounded to 1 decimal
                        except ValueError:
                            value = 'NA'
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]
    return render_template('dashboard/dashboard.table.html',data=data, error=error)


@app.route('/order',methods=['POST','GET'])
@login_required
def order():
    '''This renders a form which insert given order into orders csv file'''
    error=None
    status_code=200
    form = OrderForm(request.form)
    if request.method=='POST':
        if form.validate():
            order_id = str(request.form['order_id'])
            order_status = request.form['order_status']
            product_name = request.form['product_name']
            product_url = request.form['product_url']
            cost_price = request.form['cost_price']
            print order_id,order_status,product_name,product_url,cost_price
            #Only intering necessory data, other fields are blank
            insertData = ['\n',order_status,order_id,'','','',product_name,product_url,'','','','','','','','','','','','','','','',cost_price,'','','','\n']
            appendFile = open('Test-Orders_DB.csv','ab')
            writer = csv.writer(appendFile)
            writer.writerow(insertData)
            flash('Order Details Inserted')
            return redirect(url_for('dashboard'))
        else:
            error = 'Please fill all fields.'
    return render_template('dashboard/dashboard.create.html', form=form, error=error),status_code


@app.route('/spider',methods=['POST','GET'])
@login_required
def spider():
    '''This deploys the spider '''
    error=None
    status_code=200
    flash("It Normally takes 5 Minutes,Please wait after deploying ")
    if request.method == 'POST':
        os.system('scrapy crawl lys &')
        return redirect(url_for('download'))
    return render_template('dashboard/dashboard.spider.html',error=error),status_code


@app.route('/download')
@login_required
def download():
    '''Render Available CSV into table works as a file Manager'''
    error=None
    status_code=200
    filelist = {}
    flash("Click The download Icon to download the File")
    for file in os.listdir("."):
        if file.endswith(".csv") and file!='Test-Orders_DB.csv':
            filelist[file] = os.path.join(".", file)
            print file
    return render_template('dashboard/dashboard.download.html',data=filelist,error=error),status_code

@app.route('/<path:filename>', methods=['GET', 'POST'])
def downloadfile(filename):
    '''Sending raw file to the User'''
    return send_from_directory(directory='.', filename=filename)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('login'))

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
