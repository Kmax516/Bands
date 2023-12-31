from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models import band


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_user(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_num'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Unacceptable password/Email","logError")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):  # stored password with hash, followed by form password
        flash("Unacceptable Password/email","logError")
        return redirect('/')
    session['user_num'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_num' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_num']
    }
    return render_template("dashboard.html",user= User.get_by_id(data), bands = band.Band.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')