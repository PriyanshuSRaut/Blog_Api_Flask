from flask import Blueprint, jsonify, request as req, make_response as res, render_template as render
from database import db
from sqlalchemy import text
from exception import UserDefined
from sendMail import send_mail
from os import getenv
from dotenv import load_dotenv
# from flask_jwt import jwt_required, encode_token
from datetime import datetime, timedelta
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from werkzeug.security import generate_password_hash, check_password_hash
import re

load_dotenv()

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
                            email_exist = conn.execute(text(f'''SELECT * FROM blog_users WHERE user_email = \"{userEmail}\"''')).mappings().first()
                            name_exist = conn.execute(text(f'''SELECT * FROM blog_users WHERE user_name = \"{userName}\"''')).mappings().first()

                            # print(email_exist, name_exist)

                            if email_exist:
                                raise UserDefined({"message" : "Email Exist!", "exist": "email"})
                                # if not email_exist.get
                            elif name_exist:
                                raise UserDefined({"message" : "Username is already taken.", "exist": "name"})
                            else:
                                # result = conn.execute(text(f'''INSERT INTO blog_users (user_name, user_email, user_password) VALUES ("{userName}", "{userEmail}", "{generate_password_hash(userPassword)}")''')).rowcount
                                # if result:
                                token = encode({"data": {"email": userEmail, "name": userName, "pass": generate_password_hash(userPassword)}, "exp": datetime.utcnow() + timedelta(minutes=3) }, getenv("SECRET_KEY")).decode("utf-8")
                                send_mail(
                                    "Blogger Email Verification",
                                    getenv("EMAIL"),
                                    [userEmail],
                                    f'''
                                    <div style="max-width: 600px; margin: 0 auto;">
                                        <h1 style="text-align: center; font-size: 32px; font-weight: bold;">Verify your email address</h1>
                                        <p style="font-size: 18px; line-height: 1.5;">Please click the button below to verify your email address and activate your account:</p>
                                        <div style="text-align: center;">
                                            <a href="{req.root_url}api/auth/verify?token={token}" style="background-color: #1e90ff; color: #fff; display: inline-block; padding: 16px 24px; font-size: 18px; text-decoration: none; border-radius: 4px;">Verify Email Address</a>
                                        </div>
                                        <p style="font-size: 18px; line-height: 1.5;">If you did not request to verify your email address, please ignore this message.</p>
                                    </div>
                                    '''
                                )
                                return jsonify({"message": "Please check your email to verify the account."})
                                # else:
                                #     raise UserDefined({"message": "Some error occured! Please try again later."})
                            
                    else:
                        raise UserDefined({"message": "Invalid Password Format! Password Must be combination of digits, letters and special characters and minimum length must be 8."})
                else:
                    raise UserDefined({"message": "Invalid Email!"})
            else:
                raise UserDefined({"message": "Insufficient Data!"})
    except(UserDefined, Exception) as e:
        if isinstance(e, UserDefined):
            # return jsonify({"Message": e.args[0]})
            print(e.args[0])
            return jsonify(e.args[0]), 400
        
        print(e)
        return jsonify({"message": "Server Error"}), 500
    

@auth.get("/verify")
def verify():
    try:
        token = req.args.get("token")
        if token:
            data = decode(token, getenv("SECRET_KEY"))
            with db.connect() as conn:
                verifyUser = conn.execute(text(f'''INSERT INTO blog_users (user_name, user_email, user_password, verified) VALUES ("{data.get("data").get("name")}", "{data.get("data").get("email")}", "{data.get("data").get("pass")}", TRUE)''')).rowcount
                print(verifyUser)
                if verifyUser:
                    return render("verified.html")

        
        raise UserDefined({"message": "Token is required"})
    except (Exception, InvalidTokenError, ExpiredSignatureError) as e:
        if isinstance(e, UserDefined):
            return jsonify(e.args[0]), 400
        
        if isinstance(e, InvalidTokenError) or isinstance(e, ExpiredSignatureError):
            return jsonify({"message": "Invalid Token"}), 401
    
        print(e)
        
        return jsonify({"message": "Server Error"}), 500