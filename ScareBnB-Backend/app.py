from csv import unregister_dialect
from email.base64mime import header_encode
from email.headerregistry import ContentTypeHeader
import os
from werkzeug.utils import secure_filename                                                                                
from dotenv import load_dotenv

from flask import Flask, jsonify, render_template, request, flash, redirect, json
from flask_debugtoolbar import DebugToolbarExtension
import logging

from forms import ListingAddForm, UserAddForm, LoginForm
from models import db, connect_db, User, Listing
from s3 import upload_file, get_images, S3_CONFIGURED
from botocore.exceptions import ClientError
from flask_cors import CORS

import jwt


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
load_dotenv()

CURR_USER_KEY = "curr_user"
BUCKET = os.environ["BUCKET"]


app = Flask(__name__)
CORS(
    app,
    origins=["http://localhost:3000", "http://10.0.1.198:3000", "http://127.0.0.1:3000"],
    supports_credentials=True,
    allow_headers=["Content-Type", "AuthToken"],
)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///scarebnb.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
toolbar = DebugToolbarExtension(app)
logger.info(f"connecting to db at {app.config['SQLALCHEMY_DATABASE_URI']}")


connect_db(app)

BUCKET_URL = os.environ["DO_URL"]

if __name__ == "__main__":
    in_development = os.environ.get("FLASK_ENV") == "development"
    app.run(host="127.0.0.1", port=5000, debug=True)


# BASE_IMAGE_URL = "https://scare-bnb.sfo2.digitaloceanspaces.com/horror-flick-abandoned-home.jpg"

#############################################################################
# User signup/login/logout


@app.route("/guest", methods=["GET"])
def is_guest():
    print("guest route")
    """Handle guest auth"""

    username = "guest"
    password = "guest"

    guest = User.authenticate(username, password)

    if guest:
        return jsonify(user=guest[0].serialize(), token=guest[1])
    return jsonify({"error": "Guest authentication failed"}), 401


@app.route("/signup", methods=["GET", "POST"])
def signup():
    logger.info("signup route")
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    # if CURR_USER_KEY in session:
    #     del session[CURR_USER_KEY]
    received = request.json

    form = UserAddForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():
        username = received["username"]
        password = received["password"]
        email = received["email"]
        first_name = received["first_name"]
        last_name = received["last_name"]
        bio = received["bio"]
        is_host = False

        try:
            user = User.signup(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                bio=bio,
                is_host=is_host,
                # image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

            serialized = user[0].serialize()

            print("signup successfully made user", user)
            return jsonify(user=serialized, token=user[1])

        except ClientError as e:
            # TODO: default image
            return jsonify(e)
    logger.info(f"form errored {form.errors}")
    return jsonify(errors=form.errors)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success."""

    print("made it to login route")
    received = request.json
    form = LoginForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():
        username = received["username"]
        password = received["password"]

        user = User.authenticate(username, password)

        if user[0]:
            serialized = user[0].serialize()

            print("login route returned user info")
            return jsonify(user=serialized, token=user[1])
        else:
            return jsonify({"msg": "failed to login username or password is invalid"})

    return jsonify(errors=form.errors)


##############################################################################
# General user routes:

# TODO: HostMessaging  UserProfile  UserLikes


@app.get("/all_listings")
def guest_listings():
    """returns JSON for all available properties
    [{id, title, description, price, image[], host_id, rating}]"""
    image_urls = get_images(bucket=BUCKET)
    listings = Listing.query.all()
    print("listings:", listings)
    serialized_list = [l.serialize() for l in listings]

    return jsonify(listings=serialized_list)


###############################################################################
# Listing routes:

# TODO: homepage  individualListings


# @app.get("/guest")
# def all_listings():
#     """returns JSON for all available properties
#     [{id, title, description, price, image[], user_id, rating}]"""
#     image_urls = get_images(bucket=BUCKET)
#     listings = Listing.query.all()
#     print('listings:', listings)
#     serialized = [l.serialize() for l in listings]

#     return jsonify(listings=serialized)


@app.get("/listing/<int:id>")
def single_listing(id):
    """returns detailed info on single listing as JSON
    {id, title, description, price, image[], user_id, rating}"""

    listing = Listing.query.get_or_404(id)
    serialized = listing.serialize()

    return jsonify(listing=serialized)


@app.post("/newlisting")
def create_listing():                                                                                                      
    # Retrieve text data from request.form                                                                                 
    title = request.form.get("title")                                                                                      
    description = request.form.get("description")                                                                          
    location = request.form.get("location")                                                                                
    price_str = request.form.get("price")                                                                                  
    user_id_str = request.form.get("user_id")                                                                              
                                                                                                                           
    # Basic validation for presence                                                                                        
    if not all([title, description, location, price_str, user_id_str]):                                                    
        return jsonify(errors={"msg": "Missing required form fields."}), 400                                               
                                                                                                                           
    try:                                                                                                                   
        price = int(price_str)                                                                                             
        user_id = int(user_id_str)                                                                                         
    except ValueError:                                                                                                     
        return jsonify(errors={"msg": "Price and User ID must be integers."}), 400                                         
                                                                                                                           
    # Retrieve the file object from request.files                                                                          
    # The key 'files' must match the name used in FormData.append('files', ...) in the frontend                            
    uploaded_file_object = request.files.get('files')                                                                      
                                                                                                                           
    if not uploaded_file_object or uploaded_file_object.filename == '':                                                    
        return jsonify(errors={"msg": "No image file selected or provided."}), 400                                         
                                                                                                                           
    filename = secure_filename(uploaded_file_object.filename)                                                              
    # Define a temporary directory (ensure it exists and is writable)                                                      
    temp_dir = "/tmp" # Or a configured upload folder                                                                      
    if not os.path.exists(temp_dir):                                                                                       
        os.makedirs(temp_dir, exist_ok=True)                                                                               
    temp_server_path = os.path.join(temp_dir, filename)                                                                    
                                                                                                                           
    image_url_s3 = ""                                                                                                      
    object_name_s3 = ""                                                                                                    
                                                                                                                           
    try:                                                                                                                   
        # Save the uploaded file to the temporary server path                                                              
        uploaded_file_object.save(temp_server_path)                                                                        
                                                                                                                           
        # Pass the path of the file on the server to your S3 upload function                                               
        s3_response = upload_file(temp_server_path) # from s3.py                                                           
                                                                                                                           
        if s3_response and isinstance(s3_response, list) and len(s3_response) == 2:                                        
            image_url_s3 = s3_response[0]                                                                                  
            object_name_s3 = s3_response[1]                                                                                
        else:                                                                                                              
            # Handle S3 upload failure                                                                                     
            logger.error(f"S3 upload failed or returned unexpected data: {s3_response}")                                   
            if S3_CONFIGURED: # Assuming S3_CONFIGURED is accessible from s3.py                                            
                return jsonify(errors={"msg": "Failed to upload image to S3."}), 500                                       
            # Fallback for when S3 is not configured (placeholder logic in s3.py)                                          
            if not S3_CONFIGURED and s3_response:                                                                          
                 image_url_s3 = s3_response[0]                                                                             
                 object_name_s3 = s3_response[1]                                                                           
            else:                                                                                                          
                 return jsonify(errors={"msg": "Image processing failed."}), 500                                           
                                                                                                                           
    except Exception as e:                                                                                                 
        logger.error(f"Error during file processing or S3 upload: {e}")                                                    
        return jsonify(errors={"msg": f"Server error during file upload: {str(e)}"}), 500                                  
    finally:                                                                                                               
        # Clean up the temporary file from the server                                                                      
        if os.path.exists(temp_server_path):                                                                               
            os.remove(temp_server_path)                                                                                    
                                                                                                                           
    # Create and save the Listing object to the database                                                                   
    try:                                                                                                                   
        listing = Listing(                                                                                                 
            title=title,                                                                                                   
            description=description,                                                                                       
            object_name=object_name_s3,                                                                                    
            location=location,                                                                                             
            price=price,                                                                                                   
            image_url=image_url_s3,                                                                                        
            host_id=user_id,                                                                                               
            rating=0                                                                                                       
        )                                                                                                                  
        db.session.add(listing)                                                                                            
        db.session.commit()                                                                                                
        serialized = listing.serialize()                                                                                   
        return jsonify(listing=serialized), 201                                                                            
    except Exception as e:                                                                                                 
        db.session.rollback()                                                                                              
        logger.error(f"Database error after file upload: {e}")                                                             
        return jsonify(errors={"msg": "Failed to save listing to database."}), 500  

# @app.patch('/listing/<int:id>')
# def edit_listing():
#     """update listing"""

# @app.delete('/listing/<int:id>')
# def delete_listing():
# """Delete listing from database"""


################################################################################
# Favorites
# @app.get("/user/<int:user_id>/favorites")
# def all_liestings():
#     """returns JSON for all available properties
#     [{id, title, description, price, image[], user_id, rating}]"""
#     image_urls = get_images(bucket=BUCKET)
#     print("image_urls", image_urls)
#     listings = Listing.query.all()
#     serialized = [l.serialize() for l in listings]
#     print("listings", listings)

#     return jsonify(listings=serialized)
