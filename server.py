from hashlib import md5

import flask
import pydantic
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

import schema
from models import Session, Ads, User

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


def get_ads(session, ads_id):
    ads = session.get(Ads, ads_id)
    if ads is None:
        raise HttpError(404, "usr not found")
    return ads


class AdsView(MethodView):
    def get(self, ads_id):
        with Session() as session:
            ads = get_ads(session, ads_id)
            return jsonify(
                {
                    "id": ads.id,
                    "user": ads.user,
                    "heading": ads.heading,
                    "description": ads.description,
                    "creation_time": ads.creation_time.isoformat(),
                }
            )

    def post(self):
        validated_json = validate(schema.CreateAds, request.json)
        validated_json["password"] = hash_password(validated_json["password"])
        with Session() as session:
            ads = Ads(**validated_json)
            session.add(ads)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "User already exists")
            return jsonify({"id": ads.id})

    def patch(self, ads_id):
        validated_json = validate(schema.UpdateAds, request.json)
        if "password" in validated_json:
            validated_json["password"] = hash_password(validated_json["password"])
        with Session() as session:
            ads = get_ads(session, ads_id)
            for field, value in validated_json.items():
                setattr(ads, field, value)
            session.add(ads)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "User already exists")
            return jsonify({"id": ads.id})

    def delete(self, ads_id):
        with Session() as session:
            ads = get_ads(session, ads_id)
            session.delete(ads)
            session.commit()
            return jsonify({"status": "success"})


ads_view = AdsView.as_view("adss")
app.add_url_rule(
    "/ads/<int:ads_id>", view_func=ads_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/ads/", view_func=ads_view, methods=["POST"])

if __name__ == "__main__":
    app.run()
