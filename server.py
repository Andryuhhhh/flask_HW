from flask import Flask, Response, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from errors import HttpError

from db import Session, Adverts

app = Flask('Adverts')



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
    response = jsonify({"error": err.message})
    response.status_code = err.status_code
    return response


def get_advert_by_id(advert_id: int):
    advert = request.session.get(Adverts, advert_id)

    if advert is None:
        raise HttpError(404, "Advert not found")

    return advert


def add_advert(advert: Adverts):
    request.session.add(advert)

    try:
        request.session.commit()
    except IntegrityError:
        request.session.rollback()
        raise HttpError(409, "advert already exist")





class AdvertView(MethodView):
    def get(self, advert_id: int):
        advert = get_advert_by_id(advert_id)

        print("ADVERT:", advert)
        print("ADVERT DICT:", advert.dict)

        return jsonify(advert.dict)

    def post(self):
        json_data = request.json

        advert = Adverts(
            header=json_data["header"],
            description=json_data["description"],
            owner=json_data["owner"],
        )
        add_advert(advert)

        return jsonify(advert.dict)

    def patch(self, advert_id: int):
        json_data = request.json

        advert = get_advert_by_id(advert_id)

        print("PATCH ADVERT:", advert)
        print("PATCH DATA:", json_data)

        if "description" in json_data:
            advert.description = json_data["description"]

        add_advert(advert)

        return jsonify(advert.dict)

    def delete(self, advert_id: int):
        advert = get_advert_by_id(advert_id)

        request.session.delete(advert)
        request.session.commit()

        return jsonify({"status": "deleted success"})


adverts_view = AdvertView.as_view("adverts")

app.add_url_rule("/adverts/", methods=["POST"], view_func=adverts_view)
app.add_url_rule("/adverts/<int:advert_id>", methods=["GET", "PATCH", "DELETE"], view_func=adverts_view)

app.run()