from flask import Flask, Response, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from db import Session, User

app = Flask("hello_world")


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


class UserView(MethodView):
    def get(self, user_id: int):
        with Session() as session:
            user = session.get(User, user_id)
            if user is None:
                response = jsonify({"error": "user not found"})
                response.status_code = 404
                return response
            return jsonify(user.dict)

    def post(self):
        json_data = request.json
        if "name" not in json_data or "password" not in json_data:
            response = jsonify({"error": "name and password are required"})
            response.status_code = 400
            return response

        if not isinstance(json_data["name"], str):
            response = jsonify({"error": "name must be a string"})
            response.status_code = 400
            return response

        if not isinstance(json_data["password"], str):
            response = jsonify({"error": "password must be a string"})
            response.status_code = 400
            return response

        with Session() as session:
            user = User(name=json_data["name"], password=json_data["password"])
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                response = jsonify({"error": "user already exist"})
                response.status_code = 409
                return response

            return jsonify(user.id_dict)

    def patch(self, user_id: int):
        json_data = request.json
        with Session() as session:
            user = session.get(User, user_id)
            if user is None:
                response = jsonify({"error": "user not found"})
                response.status_code = 404
                return response
            if "name" in json_data:
                user.name = json_data["name"]
            if "password" in json_data:
                user.password = json_data["password"]
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                response = jsonify({"error": "user already exist"})
                response.status_code = 409
                return response
            return jsonify(user.id_dict)

    def delete(self, user_id: int):
        with Session() as session:
            user = session.get(User, user_id)
            if user is None:
                response = jsonify({"error": "user not found"})
                response.status_code = 404
                return response
            session.delete(user)
            session.commit()
            return jsonify({"status": "deleted"})


user_view = UserView.as_view("users")

app.add_url_rule("/hello/world/<int:some_id>", methods=["POST"], view_func=hello_world)
app.add_url_rule(
    "/users/<int:user_id>", methods=["GET", "PATCH", "DELETE"], view_func=user_view
)
app.add_url_rule("/users", methods=["POST"], view_func=user_view)
app.run()
