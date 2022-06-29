from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafe=[cafe.to_dict() for cafe in cafes])


@app.route("/search")
def search_cafe():
    query_location = request.args.get("loc")
    cafe = Cafe.query.filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error="Not Found: Sorry, we don't have a cafe at that location")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    new_cafe = Cafe(name=request.form.get("name"), map_url=request.form.get("map_url"), img_url=request.form.get("img_url"), location="Mississauga", seats="30", has_toilet=1, has_wifi=1, has_sockets=1, can_take_calls=0, coffee_price="$2")
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response="success: Successfully add the new cafe")


@app.route("/update-price/<int:cafe_id>", methods=["GET", "PATCH"])
def update_cafe_price(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe:
        cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(success="Successfully updated the price")
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})


@app.route("/report-closed/<cafe_id>", methods=["GET", "DELETE"])
def delete_cafe(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe:
        api_key = request.args.get("api-key")
        if api_key == "fhnq092348cb02392cn4":
            cafe_to_delete = Cafe.query.get(cafe.id)
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(success="Successfully delete the cafe")
        else:
            return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api")
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
