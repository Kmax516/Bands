from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.band import Band

class User:

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.bands = []



    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL("band_schema").query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("band_schema").query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("band_schema").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("band_schema").query_db(query,data)
        data = {'id':id}
        return cls(results[0])
    
    
    @classmethod
    def get_one_band(cls, data ): 
        query = "SELECT * FROM users LEFT JOIN bands on users.id = bands.user_id WHERE users.id = %(id)s;" 
        results = connectToMySQL('band_schema').query_db(query,data) 
        print(results)  
        User = cls(results[0])  
        for row in results: 
            band = { 
                'id': row['bands.id'],
                'band_name': row['band_name'],
                'genre': row['genre'],
                'home_city': row['home_city'],
                'created_at': row['bands.created_at'],
                'updated_at': row['bands.updated_at']
            }
            User.bands.append(Band(band))  #dojo class from ninjas table appended or added to the ninjas list created with the appropriate data filling in each slot.
        return User









    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("band_schema").query_db(query,user)
        if len(results) >= 1:
            flash("Email unusable.","regError",)
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Incorrect Email", "regError",)
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "regError",)
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "regError")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be no less then 8 characters", "regError")
            is_valid= False
        if user['password'] != user['verify']:
            flash("Passwords dont align","regError",)
        # if User.get_by_email(user):
        #     is_valid= False
        #     flash( "Choose another email", "regError")


        return is_valid

   