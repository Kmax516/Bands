from flask import render_template,redirect,request,session
from flask_app import app
# ...server.py
from flask_app.models import user, band    





@app.route('/new/sighting')
def bands():
    if 'user_num' in session:
        data ={
    'id': session['user_num']
    }
        return render_template('new.html',user=user.User.get_by_id(data))
      
    return redirect('/new/sighting')

@app.route('/create/band',methods=['POST'])
def create_band():
    if 'user_num' in session:
        print(request.form)
      
    if not band.Band.validate_band(request.form):
    
          return redirect('/new/sighting')
    
    data = {
          'band_name' : request.form['band_name'],
          'genre' : request.form['genre'],
          'home_city' : request.form['home_city'],
          'user_id'  : session ['user_num'],
        }
    band.Band.save(data)
    return redirect('/dashboard')

@app.route('/bands/delete/<int:id>')
def delete(id):
     if 'user_num' not in session:
         return redirect('/logout')
        
     data ={
        'id': id
      }
     band.Band.delete(data)
    
     return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_page(id):
    data = {
        'id': id
    }
    data1 ={
    'id': session['user_num'] 
    }
    return render_template("edit.html", band = band.Band.get_by_id(data), user=user.User.get_by_id(data1))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
   
     if 'user_num' in session:
        print(request.form)
      
     if not band.Band.validate_band(request.form):
    
          return redirect ( f'/edit/{id}')
     data = {
        'id': id,
        "band_name":request.form['band_name'],
        "genre": request.form['genre'],
        "home_city": request.form['home_city'],
    }
     band.Band.update(data)
     return redirect('/dashboard')

@app.route('/mybands')
def display():
    data = {
        'id': session['user_num']
    }
    return render_template("display.html", user1 = user.User.get_one_band(data), user=user.User.get_by_id(data))