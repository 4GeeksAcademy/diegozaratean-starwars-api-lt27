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
from models import db, User, Teacher

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret cualqueir cosa que ustedes deseen"  # Change this!
# hola   hosuper-secret cualqueir cosa que ustedes deseenlasuper-secret cualqueir cosa que ustedes deseen
jwt = JWTManager(app)

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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


# INCIO CODIGO API
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
@jwt_required()
def get_users():
    all_users = User.query.all()
    print(all_users)
    results = list(map(lambda elemento: elemento.serialize() ,all_users))
    print(results)
    

    response_body = {
        "msg": "Traer los usuarios de la BDD"
    }

    return jsonify(results), 200

@app.route('/teacher', methods=['POST'])
def create_teachers():
    # leer los datos del body del teacher
    print("PPOST DE TEACHER TESTTTTTTT")
    print(request)
    print(request.get_json())
    print(request.get_json()["name"])
    print(request.get_json()["city"])    
    # crear en teacher en la BD
    new_teacher = Teacher(name= request.get_json()["name"],age = request.get_json()["age"],city=request.get_json()["city"])
    db.session.add(new_teacher)
    db.session.commit()
    # unir
    #
    response_body = {
        "msg": "Debo crear el teacher"
    }
    return jsonify(response_body), 200



@app.route('/teacher', methods=['GET'])
def get_teachers():
    all_teachers = Teacher.query.all()
    results = list(map(lambda elemento: elemento.serialize() ,all_teachers))
    return jsonify(results), 200


@app.route('/teacher/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):

    print(teacher_id)
    teacher = Teacher.query.filter_by(id=teacher_id).first()
    print(teacher.serialize())
    
    return jsonify(teacher.serialize()), 200


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "The user i not in the system"}), 401
    print(user)
    print(user.serialize())
    if user.password != password:
        return jsonify({"msg": "Bad password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# FIN CODIGO API


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
