from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

import os

app = Flask(__name__)
# to put the file in same folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)  # initialise the db


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("Database Created!")


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Database Dropped!")


@app.cli.command('db_seed')
def db_seed():
    mercury = Planets(
                      planet_name='Mercury',
                      planet_type='Class D',
                      home_star='Sol',
                      mass=3.258e23,
                      radius=1516,
                      distance=35.98e6
                      )
    venus = Planets(
                      planet_name='Venus',
                      planet_type='Class K',
                      home_star='Sol',
                      mass=4.867e24,
                      radius=3760,
                      distance=67.24e6
                      )
    earth = Planets(
                      planet_name='Earth',
                      planet_type='Class M',
                      home_star='Sol',
                      mass=5.972e24,
                      radius=3959,
                      distance=92.96e6
                      )
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(
        first_name="William",
        last_name="Herschel",
        email="test@test.com",
        password="123"
    )
    db.session.add(test_user)
    db.session.commit()
    print("Database seeded!")


@app.route('/')
def name():
    return 'Hello World'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planetary API.')


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'),404


@app.route('/parameteres')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry {0}, you are not old enough.".format(name)), 401
    else:
        return jsonify(message="Welcome {0}, you are old enough.".format(name))


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry {0}, you are not old enough.".format(name)), 401
    else:
        return jsonify(message="Welcome {0}, you are old enough.".format(name))


@app.route('/planets',methods=["GET"])
def planets():
    planets_list = Planets.query.all()
    print(planets_list)
    return jsonify(planets_list)


# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


if __name__ == '__main__':
    app.run(debug=True)
