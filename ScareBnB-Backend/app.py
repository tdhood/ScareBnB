from csv import unregister_dialect
from email.base64mime import header_encode
from email.headerregistry import ContentTypeHeader
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, render_template, request, flash, redirect, json
from flask_debugtoolbar import DebugToolbarExtension

from forms import ListingAddForm, UserAddForm, LoginForm
from models import db, connect_db, User, Listing
from s3 import upload_file, get_images
from botocore.exceptions import ClientError
from flask_cors import CORS

import jwt

load_dotenv()

CURR_USER_KEY = "curr_user"
BUCKET = os.environ["BUCKET"]


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///scarebnb.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = True
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
toolbar = DebugToolbarExtension(app)

connect_db(app)

BUCKET_URL = os.environ["DO_URL"]

# if __name__ == "__main__":
#     app.run(host="localhost", port=5000, debug=True)


# BASE_IMAGE_URL = "https://scare-bnb.sfo2.digitaloceanspaces.com/horror-flick-abandoned-home.jpg"

#############################################################################
# User signup/login/logout



@app.route("/guest", methods=["GET"])
def is_guest():
    print("guest route")
    """Handle guest auth"""

    username = 'guest'
    password = 'guest'
    
    guest = User.authenticate(username, password)

    if guest:
        return jsonify(user=guest[0].serialize(), token=guest[1])
    return jsonify({"error": "Guest authentication failed"}), 401



@app.route("/signup", methods=["GET", "POST"])
def signup():
    print("signup route")
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
        print("username", username)

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

            return jsonify(user=serialized, token=user[1])

        except ClientError as e:
            # TODO: default image
            return jsonify(e)

    return jsonify(errors=form.errors)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success."""

    received = request.json
    form = LoginForm(csrf_enabled=False, data=received)

    if form.validate_on_submit():
        username = received["username"]
        password = received["password"]

        user = User.authenticate(username, password)

        if user[0]:
            serialized = user[0].serialize()

            return jsonify(user=serialized, token=user[1])
        else:
            return jsonify({"msg": "failed to login username or password is invalid"})

    return jsonify(errors=form.errors)


##############################################################################
# General user routes:

# TODO: HostMessaging  UserProfile  UserLikes


@app.get("/guest/listings")
def guest_listings():
    """returns JSON for all available properties
    [{id, title, description, price, image[], host_id, rating}]"""
    image_urls = get_images(bucket=BUCKET)
    listings = Listing.query.all()
    print('listings:', listings)
    serialized = [l.serialize() for l in listings]

    return jsonify(listings=serialized)

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



# @app.get("/listing/<int:id>")
# def single_listing(id):
#     """returns detailed info on single listing as JSON
#     {id, title, description, price, image[], user_id, rating}"""

#     listing = Listing.query.get_or_404(id)
#     serialized = listing.serialize()

#     return jsonify(listing=serialized)


# @app.post("/listing")
# def create_listing():
#     """Create new listing for property

#     Takes Json {data: {title, description, location, price, user_id, rating, files: "string of image file path"}

#     Returns Json {listing: {id, description, price, rating, title, user_id}}"""

#     image_url = ""

#     form = ListingAddForm(csrf_enabled=False)
    
#     if form.validate_on_submit():
#         title = form.data["title"]
#         description = form.data["description"]
#         location = form.data["location"]
#         price = form.data["price"]
#         user_id = form.data["user_id"]
#         rating = form.data["rating"]
#         files = form.data["files"]

#         try:
#             image_url = upload_file(files)
#             print("image_url", image_url)
#         except ClientError as e:
#             # TODO: default image
#             print(e)

#         listing = Listing(
#             title=title,
#             description=description,
#             object_name=image_url[1],
#             location=location,
#             price=price,
#             image_url=image_url[0],
#             user_id=user_id,
#             rating=rating,
#         )

#         db.session.add(listing)
#         db.session.commit()

#         serialized = listing.serialize()

#         return jsonify(listing=serialized)

#     return jsonify(errors=form.errors)

    # @app.patch('/listing/<int:id>')
    # def edit_listing():
    #     """update listing"""

    # @app.delete('/listing/<int:id>')
    # def delete_listing():
    # """Delete listing from database"""

################################################################################
#Favorites
# @app.get("/user/<int:user_id>/favorites")
# def all_listings():
#     """returns JSON for all available properties
#     [{id, title, description, price, image[], user_id, rating}]"""
#     image_urls = get_images(bucket=BUCKET)
#     print("image_urls", image_urls)
#     listings = Listing.query.all()
#     serialized = [l.serialize() for l in listings]
#     print("listings", listings)

#     return jsonify(listings=serialized)
