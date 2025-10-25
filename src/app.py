"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Vehicle, Favorite, GenderEnum
from sqlalchemy import select
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Endpoints de  usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    users = db.session.execute(select(User)).scalars().all()
    users = list(map(lambda item: item.serialize(), users))
    return jsonify(users), 200


@app.route("/user/<int:theid>", methods=['GET'])
def get_one_user(theid):
    user = db.session.get(User, theid)
    if user is None:
        return jsonify({"message": f"User ID {theid} not found, please verify"}), 404
    return jsonify(user.serialize()), 200


@app.route("/user", methods=["POST"])
def add_new_user():
    body = request.get_json()
    if body is None:
        return jsonify({"message": "You need tu specify the request body as a json object"})
    if "email" not in body or "username" not in body or "name" not in body:
        return jsonify({"message": "You need specify: name, username and email"})
    if body.get("password") is None:
        return jsonify({"message": "You need specify the password"})

    user = User.query.filter_by(email=body["email"]).first()
    if user is not None:
        return jsonify({"message": "User exist"}), 400
    user_username = User.query.filter_by(username=body["username"]).first()
    if user_username is not None:
        return jsonify({"message": "Username exist"}), 400
    user = User(email=body["email"], password=body["password"], name=body["name"], username=body["username"])
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify({"message": "Your user save successfully"}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": "Internal Server Error: Could not save user"}), 500


@app.route("/user/<int:theid>", methods=["DELETE"])
def delete_user(theid):
    user = db.session.get(User, theid)
    if user is None:
        return jsonify({"message": f"User ID {theid} not found, please verify"}), 404
    db.session.delete(user)
    try:
        db.session.commit()
        return jsonify({"message": f"Your user delete successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error delete User: {err.args}"}), 500


# Endpoints de personajes
@app.route('/people', methods=['GET'])
def get_all_peoples():
    peoples = db.session.execute(select(People)).scalars().all()
    peoples = list(map(lambda item: item.serialize(), peoples))
    return jsonify(peoples), 200


@app.route("/people/<int:theid>", methods=['GET'])
def get_one_people(theid):
    people = db.session.get(People, theid)
    if people is None:
        return jsonify({"message": f"People ID {theid} not found, please verify"}), 404
    return jsonify(people.serialize()), 200


@app.route("/people", methods=["POST"])
def add_new_people():
    body = request.get_json()
    if body is None:
        return jsonify({"message": "You need tu specify the request body as a json object"})
    if "full_name" not in body or "gender" not in body or "description" not in body or "url" not in body:
        return jsonify({"message": "You need specify: full_name, gender, url, description and height(optional)"})

    people = People.query.filter_by(full_name=body["full_name"]).first()
    if people is not None:
        return jsonify({"message": "People exist"}), 400
    height_value = body.get("height") 
    people = People(full_name=body["full_name"], gender=body["gender"], description=body["description"], height=height_value, url=body["url"])
    db.session.add(people)
    try:
        db.session.commit()
        return jsonify({"message": "Your people save successfully"}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": "Internal Server Error: Could not save user"}), 500


@app.route("/people/<int:theid>", methods=["DELETE"])
def delete_people(theid):
    people = db.session.get(People, theid)
    if people is None:
        return jsonify({"message": f"People ID {theid} not found, please verify"}), 404
    db.session.delete(people)
    try:
        db.session.commit()
        return jsonify({"message": f"Your people delete successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error delete User: {err.args}"}), 500


# Endpoints de planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = db.session.execute(select(Planet)).scalars().all()
    planets = list(map(lambda item: item.serialize(), planets))
    return jsonify(planets), 200


@app.route("/planets/<int:theid>", methods=['GET'])
def get_one_planet(theid):
    planet = db.session.get(Planet, theid)
    if planet is None:
        return jsonify({"message": f"Planet ID {theid} not found, please verify"}), 404
    return jsonify(planet.serialize()), 200


@app.route("/planets", methods=["POST"])
def add_new_planet():
    body = request.get_json()
    if body is None:
        return jsonify({"message": "You need tu specify the request body as a json object"})
    if "name" not in body or "description" not in body or "url" not in body:
        return jsonify({"message": "You need specify: name, description, url, population (optional) and climate (optional)"})

    planet = Planet.query.filter_by(name=body["name"]).first()
    if planet is not None:
        return jsonify({"message": "Planet exist"}), 400
    
    climate_value= body.get("climate")
    population_value= body.get("population")
    planet = Planet(name=body["name"], description=body["description"], population=population_value, url=body["url"], climate=climate_value)
    db.session.add(planet)
    try:
        db.session.commit()
        return jsonify({"message": "Your planet save successfully"}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": "Internal Server Error: Could not save user"}), 500


@app.route("/planets/<int:theid>", methods=["DELETE"])
def delete_planet(theid):
    planet = db.session.get(Planet, theid)
    if planet is None:
        return jsonify({"message": f"Planet ID {theid} not found, please verify"}), 404
    db.session.delete(planet)
    try:
        db.session.commit()
        return jsonify({"message": f"Your planet delete successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error delete User: {err.args}"}), 500


# Endpoints de Vehículos
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles = db.session.execute(select(Vehicle)).scalars().all()
    vehicles = list(map(lambda item: item.serialize(), vehicles))
    return jsonify(vehicles), 200


@app.route("/vehicles/<int:theid>", methods=['GET'])
def get_one_vehicle(theid):
    vehicle = db.session.get(Vehicle, theid)
    if vehicle is None:
        return jsonify({"message": f"Vehicle ID {theid} not found, please verify"}), 404
    return jsonify(vehicle.serialize()), 200


@app.route("/vehicles", methods=["POST"])
def add_new_vehicle():
    body = request.get_json()
    if body is None:
        return jsonify({"message": "You need tu specify the request body as a json object"})
    if "description" not in body or "name" not in body or "url" not in body:
        return jsonify({"message": "You need specify: name, description, url, model (optional) and capacity (optional)"})

    vehicle = Vehicle.query.filter_by(name=body["name"]).first()
    if vehicle is not None:
        return jsonify({"message": "Vehicle exist"}), 400
    
    model_value= body.get("model")
    capacity_value= body.get("capacity")
    vehicle = Vehicle(model=model_value, capacity=capacity_value, name=body["name"], url=body["url"], description=body["description"])
    db.session.add(vehicle)
    try:
        db.session.commit()
        return jsonify({"message": "Your vehicle save successfully"}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": "Internal Server Error: Could not save user"}), 500


@app.route("/vehicles/<int:theid>", methods=["DELETE"])
def delete_vehicle(theid):
    vehicle = db.session.get(Vehicle, theid)
    if vehicle is None:
        return jsonify({"message": f"Vehicle ID {theid} not found, please verify"}), 404
    db.session.delete(vehicle)
    try:
        db.session.commit()
        return jsonify({"message": f"Your vehicle delete successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error delete User: {err.args}"}), 500


# Endpoints favoritos

@app.route("/users/<int:theid>/favorites", methods=['GET'])
def get_user_favorites(theid):
    user = db.session.get(User, theid)
    if user is None:
        return jsonify({"message": f"User ID {theid} not found."}), 404
    favorites = user.favorites_item
    favorites_list = [item.serialize() for item in favorites]
    return jsonify(favorites_list), 200



# Agregar personaje a favoritos de user con id x
@app.route("/users/<int:theid>/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(theid, people_id):
    user = db.session.get(User, theid)
    if user is None:
        return jsonify({"message": f"User with id {theid} not found."}), 404
    people = db.session.get(People, people_id)
    if people is None:
        return jsonify({"message": f"People with id {people_id} not found."}), 404

    existe_favorito = db.session.execute(select(Favorite).where(Favorite.user_id == theid, Favorite.people_id == people_id)).scalar_one_or_none()
    if existe_favorito:
        return jsonify({"message": "The people is already in the favorites."}), 409

    new_favorite = Favorite(user_id=theid, people_id=people_id)
    db.session.add(new_favorite)
    
    try:
        db.session.commit()
        return jsonify({"message": "Person added to favorites successfully"}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error adding favorite: {err.args}"}), 500
    


# Eliminar un personaje de favoritos
@app.route("/users/<int:theid>/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(theid, people_id):
    favorite_delete = db.session.execute(select(Favorite).where(Favorite.user_id == theid, Favorite.people_id == people_id)).scalar_one_or_none()
    if favorite_delete is None:
        return jsonify({"message": "Favorite people not found for this user."}), 404
    db.session.delete(favorite_delete)
    try:
        db.session.commit()
        return jsonify({"message": "Favorite people deleted successfully."}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error deleting favorite: {err.args}"}), 500



# Añadir un planeta a favoritos
@app.route("/users/<int:theid>/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(theid, planet_id):
    user = db.session.get(User, theid)
    if user is None:
        return jsonify({"message": f"User with id {theid} not found."}), 404
    planet = db.session.get(Planet, planet_id)
    if planet is None:
        return jsonify({"message": f"Planet with id {planet_id} not found."}), 404

    existing_favorite = db.session.execute(select(Favorite).where(Favorite.user_id == theid, Favorite.planet_id == planet_id)).scalar_one_or_none()
    if existing_favorite:
        return jsonify({"message": "The planet is already in the favorites."}), 409

    new_favorite = Favorite(user_id=theid, planet_id=planet_id)
    db.session.add(new_favorite)
    
    try:
        db.session.commit()
        return jsonify({"message": "Planet added to favorites successfully"}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error adding favorite: {err.args}"}), 500
    

# Eliminar un planeta de favoritos
@app.route("/users/<int:theid>/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(theid, planet_id):
    favorite_delete = db.session.execute(select(Favorite).where(Favorite.user_id == theid, Favorite.planet_id == planet_id)).scalar_one_or_none()
    if favorite_delete is None:
        return jsonify({"message": "Favorite planet not found for this user."}), 404
    db.session.delete(favorite_delete)
    try:
        db.session.commit()
        return jsonify({"message": "Favorite planet deleted successfully."}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error deleting favorite: {err.args}"}), 500



# Añadir un vehículo a favoritos
@app.route("/users/<int:theid>/favorite/vehicle/<int:vehicle_id>", methods=["POST"])
def add_favorite_vehicle(theid, vehicle_id):
    user = db.session.get(User, theid)
    if user is None:
        return jsonify({"message": f"User with id {theid} not found."}), 404
    vehicle = db.session.get(Vehicle, vehicle_id)
    if vehicle is None:
        return jsonify({"message": f"Vehicle with id {vehicle_id} not found."}), 404

    existing_favorite = db.session.execute(select(Favorite).where(Favorite.user_id == theid, Favorite.vehicle_id == vehicle_id)).scalar_one_or_none()
    if existing_favorite:
        return jsonify({"message": "The vehicle is already in the favorites."}), 409

    new_favorite = Favorite(user_id=theid, vehicle_id=vehicle_id)
    db.session.add(new_favorite)
    
    try:
        db.session.commit()
        return jsonify({"message": "Vehicle added to favorites successfully"}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error adding favorite: {err.args}"}), 500
    

# Eliminar un vehículo de favoritos
@app.route("/users/<int:theid>/favorite/vehicle/<int:vehicle_id>", methods=["DELETE"])
def delete_favorite_vehicle(theid, vehicle_id):
    favorite_delete = db.session.execute(select(Favorite).where(Favorite.user_id == theid, Favorite.vehicle_id == vehicle_id)).scalar_one_or_none()
    if favorite_delete is None:
        return jsonify({"message": "Favorite vehicle not found for this user."}), 404
    db.session.delete(favorite_delete)
    try:
        db.session.commit()
        return jsonify({"message": "Favorite vehicle deleted successfully."}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"message": f"Error deleting favorite: {err.args}"}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
