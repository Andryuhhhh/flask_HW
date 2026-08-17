from flask import Flask, Response, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from db import Session, User
from errors import HttpError
from schema import CreateUser, UpdateUser, validate

app = Flask("hello_world")
bcrypt = Bcrypt(app)


def hash_password(password: str) -> str:
    password = password.encode()
    hashed_password = bcrypt.generate_password_hash(password)
    hashed_password = hashed_password.decode()
    return hashed_password


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    response = jsonify({"error": err.error_message})
    response.status_code = err.status_code
    return response


def hello_world(some_id: int):
    print(f"{some_id=}")
    qs = request.args
    age = qs.get("age")
    print(f"{qs=}")
    json_data = request.json
    print(f"{json_data=}")
    headers = request.headers
    headers.get("Authorization")
    print(f"{headers=}")

    response: Response = jsonify({"hello": "world"})
    response.status_code = 201
    return response


def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "user already exist")


class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate(CreateUser, request.json)

        user = User(
            name=json_data["name"], password=hash_password(json_data["password"])
        )
        add_user(user)

        return jsonify(user.id_dict)

    def patch(self, user_id: int):
        json_data = validate(UpdateUser, request.json)
        user = get_user_by_id(user_id)
        if "name" in json_data:
            user.name = json_data["name"]
        if "password" in json_data:
            user.password = hash_password(json_data["password"])
        add_user(user)
        return jsonify(user.id_dict)

    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "deleted"})


user_view = UserView.as_view("users")

app.add_url_rule("/hello/world/<int:some_id>", methods=["POST"], view_func=hello_world)
app.add_url_rule(
    "/users/<int:user_id>", methods=["GET", "PATCH", "DELETE"], view_func=user_view
)
app.add_url_rule("/users", methods=["POST"], view_func=user_view)
app.run()
