from hashlib import md5

import flask
import pydantic
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

import schema
from models import Session, User

app = flask.Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


def validate(validation_schema, validation_data):
    try:
        model = validation_schema(**validation_data)
        return model.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


def hash_password(password: str):
    password = password.encode()
    password = md5(password).hexdigest()
    return password


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({"status": "error", "description": er.message})
    response.status_code = er.status_code
    return response


def get_user(session, user_id):
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, "usr not found")
    return user


class UserView(MethodView):
    def get(self, user_id):
        with Session() as session:
            user = get_user(session, user_id)
            return jsonify(
                {
                    "id": user.id,
                    "email": user.email,
                    "creation_time": user.creation_time.isoformat(),
                }
            )

    def post(self):
        validated_json = validate(schema.CreateUser, request.json)
        validated_json["password"] = hash_password(validated_json["password"])
        with Session() as session:
            user = User(**validated_json)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "User already exists")
            return jsonify({"id": user.id})

    def patch(self, user_id):
        validated_json = validate(schema.UpdateUser, request.json)
        if "password" in validated_json:
            validated_json["password"] = hash_password(validated_json["password"])
        with Session() as session:
            user = get_user(session, user_id)
            for field, value in validated_json.items():
                setattr(user, field, value)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "User already exists")
            return jsonify({"id": user.id})

    def delete(self, user_id):
        with Session() as session:
            user = get_user(session, user_id)
            session.delete(user)
            session.commit()
            return jsonify({"status": "success"})


user_view = UserView.as_view("users")
app.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/user/", view_func=user_view, methods=["POST"])

if __name__ == "__main__":
    app.run()
