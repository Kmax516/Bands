from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user



class Band:

    def __init__(self,data):
        self.id = data['id']
        self.band_name = data['band_name']
        self.genre = data['genre']
        self.home_city = data['home_city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        # self.user_id = data['user_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO bands (band_name,genre,home_city,user_id,created_at,updated_at) VALUES (%(band_name)s,%(genre)s,%(home_city)s,%(user_id)s,Now(),Now());"
        return connectToMySQL("band_schema").query_db(query,data)
    
    @staticmethod
    def validate_band(band):
        is_valid = True
        query = "SELECT * FROM bands;"
        results = connectToMySQL("band_schema").query_db(query,band)
        if len(band['band_name']) < 2:
            flash("Band name must be at least 2 characters",)
            is_valid= False
        if len(band['genre']) < 2:
            flash("Music Genre must be at least 2 characters",)
            is_valid= False
        if len(band['home_city']) < 1:
            flash("Home city must be at least 1 character",)
            is_valid= False
        return is_valid
    
    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM bands WHERE id = %(id)s;"
        
        return connectToMySQL("band_schema").query_db(query, data)

    @classmethod
    def update(cls,data):
        query = "UPDATE bands SET band_name=%(band_name)s, genre=%(genre)s, home_city=%(home_city)s,updated_at = NOW(), created_at = Now() WHERE id = %(id)s;"
        return connectToMySQL("band_schema").query_db(query,data)

    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM bands Join users on bands.user_id = users.id Where bands.id = %(id)s;"
        results = connectToMySQL("band_schema").query_db(query,data)
        if len(results) == 0:
            return None
        else:
            # data = {'id':id}
            user_d = results[0]
            band_object = cls(user_d)
            new_user_d = {
                'id' : user_d ['users.id'],
                'first_name': user_d['first_name'],
                'last_name' : user_d['last_name'],
                'email': user_d['email'],
                'password' : user_d['password'],
                'created_at' : user_d['users.created_at'],
                'updated_at' : user_d['users.updated_at']
             }
        
            user_object = user.User(new_user_d)
            band_object.creator = user_object
       
            # return cls(results[0])
        return band_object
    
    @classmethod
    def get_all(cls): # no data needed since grabbing all
        query = "SELECT * FROM bands Join users on bands.user_id = users.id;"
        results = connectToMySQL("band_schema").query_db(query)
        if len(results) == 0:
            return []
        else:
            # 
            band_object_list = []
            for user_d in results:
                print(user_d)
            
                band_object = cls(user_d)
                new_user_d = {
                'id' : user_d ['users.id'],
                'first_name': user_d['first_name'],
                'last_name' : user_d['last_name'],
                'email': user_d['email'],
                'password' : user_d['password'],
                'created_at' : user_d['users.created_at'],
                'updated_at' : user_d['users.updated_at']
                }
        
                user_object = user.User(new_user_d)
                band_object.creator = user_object
                band_object_list.append(band_object)
            return band_object_list