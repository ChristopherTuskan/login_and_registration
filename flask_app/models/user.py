from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        
    @staticmethod
    def validate_user(reg_user,users):
        is_valid = True # we assume this is true
        num = 0
        upr = 0
        for i in reg_user['password']:
            print(i)
            if i.isdigit():
                num += 1
            if i.isupper():
                upr += 1
        
        if num<1 and upr<1:
            flash('Password needs at least 1 number and 1 uppercase letter', 'category1')
            is_valid = False

        if len(reg_user['first_name']) < 2:
            flash("First Name must be at least 2 characters.", 'category1')
            is_valid = False

        if len(reg_user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", 'category1')
            is_valid = False
            
        if len(reg_user['password']) < 8:
            flash("Password must be at least 8 characters", 'category1')
            
        if not reg_user['password'] == reg_user['confirm_password']:
            flash("Password and Confirm Password do not match", 'category1')
            is_valid=False

        if not EMAIL_REGEX.match(reg_user['email']):
            flash("Invalid email address!", 'category1')
            is_valid = False
            
        for other_user in users:
            if (reg_user['email'] == other_user.email):
                flash("Email address needs to be unique", 'category1')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login(login_user,users):
        is_valid = True
        for other_user in users:
            if login_user['email'] == other_user.email:
                print(bcrypt.check_password_hash(other_user.password, login_user['password']))
                if bcrypt.check_password_hash(other_user.password, login_user['password']):
                    print('good password and email')
                    return is_valid
            else:
                print('bad email or password')
                flash('Invalid Email/Password', 'category2')
                is_valid = False
                return is_valid
        


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('login_and_registration').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL("login_and_registration").query_db(query, data)
        return user_id

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL('login_and_registration').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL('login_and_registration').query_db(query,data)
        return cls(result[0])