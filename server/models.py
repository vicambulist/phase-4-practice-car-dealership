from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# This is creating special naming conventions for foreign keys
# Don't necessarily need it, but sometimes safer apparently
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# STEP 01: Set up models. 
#   Make sure to pass in db.Model and SerializerMixin
class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    # STEP 03: Set up relationships
    cars = db.relationship('Car', back_populates = 'owner')
    # STEP 04: Associtation Proxy
    dealerships = association_proxy('cars', 'dealerships')

    # STEP 05: Serialize rules. Don't forget the "," on the single touple
    serialize_rules = ('-cars.owner',)


class Dealership(db.Model, SerializerMixin): 
    __tablename__ = 'dealerships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    cars = db.relationship('Car', back_populates ='dealership')

    # STEP 05: Serialize rules. Don't forget the "," on the single touple
    serialize_rules = ('-cars.dealership',)

class Car(db.Model, SerializerMixin): 
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    date_sold = db.Column(db.Date, nullable=False)

    # STEP 02: Set up foreign keys for the model that joins the other two
    # Since cars are joining the other two, need to add their ids
    #   Don't forget that the ForeignKey
    #       1) starts with db.ForeignKey
    #       2) uses caps
    #       3) no underscore
    #       4) uses table name.id
    #       5) uses ()
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    dealership_id = db.Column(db.Integer, db.ForeignKey('dealerships.id'))

    # Set up relationships
    owner = db.relationship('Owner', back_populates = 'cars')
    dealership = db.relationship('Dealership', back_populates = 'cars')
    # Remember: The model in the middle will have no association proxy

    # STEP 05: Add serialize rules to prevent recursion
    #   When go to owners, don't go back to cars
    #   When go to dealers, don't go back to cars
    #   Also, don't show IDs
    serialize_rules = ('-owner.cars', '-dealership.cars', '-dealership_id', '-owner_id')


# STEP 06: Initialize the database in the CLI:
# flask db init
# flask db migrate
# flask db upgrade


