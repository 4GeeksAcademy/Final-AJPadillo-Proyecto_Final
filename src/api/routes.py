"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route("/login", methods=["POST"])
def login():
    # Obtiene el email y password del cuerpo de la solicitud JSON. Si no se proporcionan, se establece como None.
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # Verifica si el email o password no fueron proporcionados
    if email is None or password is None:
        return jsonify({"msg": "Usuario o Password erroneos"}), 401
    # Busca al usuario en la base de datos por su email
    user_query = User.query.filter_by(email=email)
    user = user_query.first()  # Obtiene el primer resultado de la consulta
    # Si no se encuentra el usuario, devuelve un mensaje de error
    if user is None:
        return jsonify({"msg": "Usuario o Password erroneos"}), 401
    # Verifica que el email y password coincidan con los del usuario en la base de datos
    if user.email != email or user.password != password:
        return jsonify({"msg": "Usuario o Password erroneos"}), 401
    # Si todo es correcto, crea un token de acceso para el usuario usando su id como identidad
    access_token = create_access_token(identity=user.id)
    # Devuelve el token de acceso como respuesta JSON
    return jsonify(access_token=access_token)

@api.route('/signup', methods=['POST'])
def create_user():
    # Obtiene los datos del cuerpo de la solicitud JSON
    data = request.json
    # Crea un nuevo usuario con el email y password proporcionados
    new_user = User(email=data['email'], password=data['password'])
    # Añade el nuevo usuario a la sesión de la base de datos
    db.session.add(new_user)
    # Confirma los cambios en la base de datos (guarda el nuevo usuario)
    db.session.commit()
    # Devuelve los datos del nuevo usuario como respuesta JSON
    return jsonify({"user": new_user.serialize()}), 200

@api.route("/current-user", methods=["GET"])
@jwt_required()  # Requiere que el usuario esté autenticado con JWT
def get_current_user():
    # Obtiene la identidad del usuario actual desde el token JWT
    current_user_id = get_jwt_identity()
    # Verifica si no se encontró la identidad del usuario
    if current_user_id is None:
        return jsonify({"msg": "Usuario no encontrado"}), 401
    # Busca al usuario en la base de datos usando su id
    user_query = User.query.get(current_user_id)
    # Si no se encuentra el usuario, devuelve un mensaje de error
    if user_query is None:
        return jsonify({"msg": "Usuario no encontrado"}), 401
    # Serializa los datos del usuario para enviarlos como JSON
    user = user_query.serialize()
    # Devuelve los datos del usuario actual como respuesta JSON
    return jsonify(current_user=user), 200