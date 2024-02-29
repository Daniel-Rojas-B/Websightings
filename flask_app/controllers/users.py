from flask import Flask, render_template, request, redirect, session  
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_app.models import user, sighting
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    
    if not User.validate_registration(request.form):
        
        return redirect('/')
    data = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password'])
    }
    id= User.save_user(data)
    print("\n\n\n-------->id: ", id)
    
    session['user_id']=id
    

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    sightings = Sighting.get_all_sightings_with_creator()
    print("\n\n\n-------->session: ", session['user_id'])
    return render_template('dashboard.html',user=User.get_user_by_id(data),all_sightings=sightings)


@app.route('/user/login', methods=['POST'])
def login():

    email=request.form['email']
    password=request.form['password']
    
    
    user=User.get_user_by_email(email)
    
    if not user:
        flash('Invalid Credentials', "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password,password):
        flash('Invalid Credentials', "login")
        return redirect('/')
    
    session['user_id']=user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash('Thank you for visiting', "login")
    return redirect('/')

@app.route('/sightings/new')         
def add_new_sighting():   
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':session['user_id']
    }
    
    return render_template("new_sighting.html",user=User.get_user_by_id(data))



@app.route('/sightings')         
def back_to_sightings():   
    
    return redirect('/dashboard')