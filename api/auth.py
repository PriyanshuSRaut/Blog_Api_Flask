from flask import Blueprint, jsonify, request as req, make_response as res
from database import db
from sqlalchemy import text
from exception import UserDefined
import re

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.get("/login")
def login():
    return jsonify({"Message": "This is login api"}), 200

@auth.post("signup")
def signup():
    try:
        if req.is_json:
            userName = req.json.get("username")
            userEmail = req.json.get("useremail")
            userPassword = req.json.get("userpassword")

            if userName and userEmail and userPassword:
                if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', userEmail):
                    if re.search("\d{2,}", userPassword) and re.search("\W{1,}", userPassword) and re.search("[A-z]{5,}", userPassword):
                        with db.connect() as conn:
                            email_exist = conn.execute(text(f'''SELECT * FROM users WHERE user_email = \"{userEmail}\"''')).mappings().first()
                            name_exist = conn.execute(text(f'''SELECT * FROM users WHERE user_name = \"{userName}\"''')).mappings().first()

                            if email_exist:
                                raise UserDefined({"message" : "Email Exist!", "exist": "email"})
                            elif name_exist:
                                raise UserDefined({"message" : "Username is already taken.", "exist": "name"})
                            else:
                                result = conn.execute(text("INSERT INTO blog_users (user_name, user_email, user_password)")).__dict__
                                if result.get("rowcount"):
                                    # TODO: send a verification email
                                    return jsonify({"message": "Please check your email to verify the account."})
                                else:
                                    raise UserDefined({"message": "Some error occured! Please try again later."})
                            
                    else:
                        raise UserDefined({"message": "Invalid Password Format! Password Must be combination of digits, letters and special characters and minimum length must be 8."})
                else:
                    raise UserDefined({"message": "Invalid Email!"})
            else:
                raise UserDefined({"message": "Insufficient Data!"})
    except(UserDefined, Exception) as e:
        if isinstance(e, UserDefined):
            # return jsonify({"Message": e.args[0]})
            return jsonify(e.args[0])

        
        # return jsonify({"Message": username}), 201
        # with db.connect() as conn:
            
        
        # return l