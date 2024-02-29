from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from datetime import datetime


class Sighting:
    DB="belt"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.location = data['location']
        self.date = data['date']
        self.number_of_sasquatches = data['number_of_sasquatches']
        self.what_happen=data['what_happen']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        
        self.creator= None
        

    @classmethod 
    def save_sighting(cls,data):
        print('before saving sighting')
        query="INSERT INTO sightings (user_id,location,date,number_of_sasquatches,what_happen) VALUES (%(user_id)s,%(location)s,%(selectedDate)s,%(number_of_sasquatches)s,%(what_happen)s);"
        result=connectToMySQL(cls.DB).query_db(query,data)
        
        return result
    
    @classmethod
    def update_sighting(cls,data):
        print('----------------------before updating sighting')
        query = """UPDATE sightings SET location=%(location)s, date=%(selectedDate)s, number_of_sasquatches=%(number_of_sasquatches)s, what_happen=%(what_happen)s WHERE id=%(id)s"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def delete_sighting(cls,sighting_id):
        query='DELETE FROM sightings WHERE id=%(sighting_id)s'
        data={
            'sighting_id':sighting_id
        }
        connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_all_sightings(cls):
        query = "SELECT * FROM sightings;"        
        results = connectToMySQL(cls.DB).query_db(query)        
        sightings = []        
        for sighting in results:
            sightings.append(cls(Sighting))
        return sightings
    
    @classmethod
    def get_one_sighting_id(cls,sighting_id):
        query = """SELECT * FROM sightings WHERE id=%(sighting_id)s"""
        data={
            'sighting_id':sighting_id
        }
        result=connectToMySQL(cls.DB).query_db(query,data)
        
        return cls(result[0])  

    @classmethod
    def get_all_sightings_with_creator(cls):
        query='SELECT * FROM sightings JOIN users ON sightings.user_id=users.id;'
        results=connectToMySQL(cls.DB).query_db(query)
        
        all_sightings=[]
        for row in results:

            one_sighting=cls(row)

            one_sighting_author_info={
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            author=user.User(one_sighting_author_info)

            one_sighting.creator=author

            all_sightings.append(one_sighting)
        
        return all_sightings

    @classmethod
    def get_one_sighting_with_creator(cls,sighting_id):
        query='SELECT * FROM sightings LEFT JOIN users ON sightings.user_id=users.id WHERE sightings.id=%(sighting_id)s'
        data={
            'sighting_id':sighting_id
        }
        results=connectToMySQL(cls.DB).query_db(query,data)
        sighting_object = cls(results[0])
        
        author_info={
                'id':results[0]['users.id'],
                'first_name':results[0]['first_name'],
                'last_name':results[0]['last_name'],
                'email':results[0]['email'],
                'password':results[0]['password'],
                'created_at':results[0]['users.created_at'],
                'updated_at':results[0]['users.updated_at']
            }
        author_object = user.User(author_info)
        sighting_object.creator = author_object
       
        return sighting_object

    @staticmethod
    def validate_sighting(sighting):
        is_valid=True        
        
        if len(sighting['location'])<=0:
            flash('sighting location is required', "new_sighting")
            is_valid=False
        if len(sighting['number_of_sasquatches'])<=0:
            flash('Number of sasquatches must be at least 1', "new_sighting")
            is_valid=False
        if len(sighting['what_happen'])<=0:
            flash('Notes on what happen at location should be added', "new_sighting")
            is_valid=False
        if len(sighting['what_happen'])>50:
            flash('Notes on what happen should have a maximum of 50 characters', "new_sighting")
            is_valid=False
          
        return is_valid