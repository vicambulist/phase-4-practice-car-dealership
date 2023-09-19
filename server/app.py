#!/usr/bin/env python3
# This first line is called a shibang, becuase # = shi and ! = bang
# It makes the program an executable so that in the CLI like ./app.py


# STEP 09: Import request, jsonify, and datetime for routes
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

from models import db, Dealership, Owner, Car

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

# write your routes here!

# STEP 09: Set up routes:

# POST / cars
@app.post('/cars')
def create_car():
    # Start by getting the data
    data = request.json
    '''Sometimes, we can use the following code to shortcut things:
    $ ew_car = Car(**data)
    This "**" is a "keyword argument" so that you don't have to write it all out.
    But in this case, we can't because of how we need to make the date'''
    # Make new car
    new_car = Car(
    make=data["make"],
    model=data["model"],
    owner_id=data["owner_id"],
    dealership_id=data["dealership_id"],
    date_sold=datetime.date(**data["date_sold"])
    )

    # Add to database and commit
    db.session.add(new_car)
    db.session.commit()
    
    #Return it with to_dict
    return new_car.to_dict(), 201

    # STEP 10: Turn on the server, and test it in Postman


    # Instead of above return, could also use jsonify to be specific (though it defaults to it)
    # return jsonify( new_car.to_dict() ), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
