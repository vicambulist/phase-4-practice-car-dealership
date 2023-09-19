#!/usr/bin/env python3

from app import app
from models import db, Dealership, Owner, Car
from faker import Faker
# STEP 07: For seeding, import random here for the random choice
import random

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        # STEP 07: Set up seeding. 
        #   Start with clearing old data. Use prints to track
        print("Deleteing old data")
        Car.query.delete()
        Owner.query.delete()
        Dealership.query.delete()

        print("Seeding owners...")

        owners_list = []

        for _ in range(5):
            owner = Owner(
                first_name=faker.first_name(),
                last_name=faker.last_name()
            )
            owners_list.append(owner)

        db.session.add_all(owners_list)
        db.session.commit()


        print("Seeding dealerships...")

        dealerships_list = []

        for _ in range(5):
            dealer = Dealership(
                name=faker.company(),
                address=faker.street_address()
            )
            dealerships_list.append(dealer)

        db.session.add_all(dealerships_list)
        db.session.commit()


        print("Seeding cars...")

        cars_list = []
        # Set up a list of manufacturers and use random choice below
        manufacturers = ("Ford", "Chevrolet", "Kia", "Toyota", "Chrysler", "Telsa")

        # You can install custom packages for faker here if you need.
        # We are using a random choice from our list
        for _ in range(10):
            car = Car(
                make=random.choice(manufacturers),
                model=faker.first_name(),
                # Use the "date_between" function
                date_sold=faker.date_between(start_dat='-100y', end_date='today'),
                # Set up foreign keys
                dearlership=random.choice(dealerships_list),
                owner=random.choice(dealerships_list)
            )

            cars_list.append(car)

        db.session.add_all(cars_list)
        db.session.commit()

        print("Seeding complete!")

# STEP 08: Run seed.py to populate the database





''' Note:if you want to run the app as an executable, run this code in CLI:
$ sudo chmod +rwx seed.py

"sudo" means "super do"
"rwx" means read, write, execute. d means directory
"chmod" means change mode

To show permissions of a file, use this code in CLI:
$ ls -l   ]

You will have to type in your password

To list out all available:
$ man chmod

'''
