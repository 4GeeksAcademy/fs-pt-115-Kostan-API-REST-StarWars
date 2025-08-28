from flask import Flask, jsonify, request, Blueprint
from models import db, User, Planets, People, Favorite

api = Blueprint("api", __name__)

# --- USERS ---
@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email and password are required"}), 400
    
    new_user = User(
        email=data["email"],
        password=data["password"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.serialize()), 200



# --- PLANETS ---
@api.route("/planets", methods=["POST"])
def create_planet():
    data = request.get_json()
    if not data.get("name") or not data.get("description"):
        return jsonify({"msg": "Name and description are required"}), 400
    
    new_planet = Planets(
        name=data["name"],
        description=data["description"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@api.route("/planets", methods=["GET"])
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@api.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200



# --- PEOPLE ---
@api.route("/people", methods=["POST"])
def create_person():
    data = request.get_json()
    if not data.get("name") or not data.get("age"):
        return jsonify({"msg": "Name and age are required"}), 400
    
    new_person = People(
        name=data["name"],
        age=data["age"]
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

@api.route("/people", methods=["GET"])
def get_people():
    people_list = People.query.all()
    return jsonify([person.serialize() for person in people_list]), 200

@api.route("/people/<int:person_id>", methods=["GET"])
def get_person(person_id):
    person = People.query.get(person_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize()), 200


# --- FAVORITES ---
@api.route("/users/favorites", methods=["GET"])
def get_current_user_favorites():
    current_user_id = 1 

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    return jsonify([fav.serialize() for fav in favorites]), 200




@api.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    current_user_id = 1

    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    existing_fav = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if existing_fav:
        return jsonify({"msg": "Planet already in favorites"}), 400

    new_fav = Favorite(user_id=current_user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.serialize()), 201



@api.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_person(people_id):
    current_user_id = 1

    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404

    existing_fav = Favorite.query.filter_by(user_id=current_user_id, people_id=people_id).first()
    if existing_fav:
        return jsonify({"msg": "Person already in favorites"}), 400

    new_fav = Favorite(user_id=current_user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.serialize()), 201



@api.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    current_user_id = 1 
    
    favorite = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Planet removed from favorites"}), 200



@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_person(people_id):
    current_user_id = 1 
    
    favorite = Favorite.query.filter_by(user_id=current_user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite person not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Person removed from favorites"}), 200
