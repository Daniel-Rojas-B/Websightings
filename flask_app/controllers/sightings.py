from flask import Flask, render_template, request, redirect, session  
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User
from flask_app.models import user, sighting
from flask import flash


@app.route('/sighting/add', methods=['POST'])         
def add_sighting():  
    if 'user_id' not in session:
        return redirect('/logout')    
    
    if not Sighting.validate_sighting(request.form):
        return redirect('/sightings/new')
    
    sighting.Sighting.save_sighting(request.form)   
    return redirect("/dashboard")



@app.route('/sightings')         
def all_sightings():   
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    sightings = Sighting.get_all_sightings_with_creator()
    
    return render_template("dashboard.html",user=User.get_user_by_id(data), all_sightings=sightings)

@app.route('/sighting/create', methods=['POST'])
def create_sighting():
    data={
        "name":request.form['name'],
        "user_id":session['user_id']
    }
    Sighting.save_sighting(data)

@app.route('/sighting/view/<sighting_id>')
def view_sighting(sighting_id,):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    sightings = Sighting.get_all_sightings_with_creator()
    sighting_=sighting.Sighting.get_one_sighting_id(sighting_id)
    
    sighting_posted_by=Sighting.get_one_sighting_with_creator(sighting_id)
    

    return render_template('view_sighting.html',sighting_with_author=sighting_posted_by, sighting=sighting_, all_sightings=sightings, user=User.get_user_by_id(data))

@app.route('/sighting/edit/<sighting_id>')
def edit_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/logout')  
    
    data = {
        'id':session['user_id']
    }

    sighting_=sighting.Sighting.get_one_sighting_id(sighting_id)    
    return render_template('edit_sighting.html',sighting=sighting_, user=User.get_user_by_id(data))

@app.route('/sighting/update/<sighting_id>', methods=['POST'])         
def update_sighting(sighting_id):  
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':session['user_id']
    }
    sighting_=sighting.Sighting.get_one_sighting_id(sighting_id)

    if not Sighting.validate_sighting(request.form):
        return render_template('edit_sighting.html',sighting=sighting_,user=User.get_user_by_id(data))
    
    sighting.Sighting.update_sighting(request.form)   
    return redirect('/sightings')

 
@app.route('/sighting/delete/<sighting_id>')         
def delete_sighting(sighting_id):  
    if 'user_id' not in session:
        return redirect('/logout')
    
    sighting.Sighting.delete_sighting(sighting_id)
    return redirect('/dashboard')  
