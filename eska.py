import os
from datetime import datetime
from faker import Factory
from random import choice

from flask import Flask, jsonify, abort, make_response, request
from flask_marshmallow.fields import AbsoluteURLFor
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from marshmallow.fields import Nested


# Setup and config


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL"
) or "sqlite:////" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

# Models


class Artists(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hits = db.relationship("Hits", backref="artist", lazy="dynamic")

    def __repr__(self):
        return "<Artist {} {}>".format(self.first_name, self.last_name)


class Hits(db.Model):
    __tablename__ = "hits"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    title_url = db.Column(db.String(120))
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<Hit {}>".format(self.title)


# Serializers


class ArtistSchema(ma.ModelSchema):
    class Meta:
        model = Artists
        fields = ("id", "first_name", "last_name")


class HitsSchema(ma.ModelSchema):
    title_url = AbsoluteURLFor("get_hit_detail", hit_id="<id>")

    class Meta:
        model = Hits
        fields = ("id", "title", "title_url")


class SingleHitSchema(ma.ModelSchema):
    title_url = AbsoluteURLFor("get_hit_detail", hit_id="<id>")
    artist = Nested(ArtistSchema)

    class Meta:
        model = Hits
        exclude = ["updated_at"]


class SimpleHitSchema(ma.ModelSchema):
    artist = Nested(ArtistSchema)

    class Meta:
        model = Hits
        fields = ("id", "title", "artist")


# Error handlers


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}), 400)


@app.errorhandler(500)
def bad_request(error):
    return make_response(jsonify({"error": "Server error"}), 500)


# Views


@app.route("/api/v1/hits", methods=["GET"])
def get_hits():
    all_hits = Hits.query.order_by("created_at").limit(20)
    hit_schema = HitsSchema(many=True)
    res = hit_schema.dump(all_hits).data

    return jsonify({"hits": res})


@app.route("/api/v1/hits/<int:hit_id>", methods=["GET"])
def get_hit_detail(hit_id):
    hit = Hits.query.get(hit_id)
    if not hit:
        abort(404)
    hit_schema = SingleHitSchema()
    res = hit_schema.dump(hit).data

    return jsonify({"hit": res})


@app.route("/api/v1/hits", methods=["POST"])
def create_hit():
    if (
        not request.json
        or "title" not in request.json
        or "artist_id" not in request.json
    ):
        abort(400)
    title = request.json["title"]
    artist_id = request.json["artist_id"]
    check_artist = Artists.query.get(artist_id)
    if not check_artist:
        abort(400)
    if not isinstance(title, str) and not isinstance(artist_id, int):
        abort(400)

    new_hit = Hits(title=title, artist_id=artist_id)

    db.session.add(new_hit)
    db.session.commit()

    hit_schema = SimpleHitSchema()
    res = hit_schema.dump(new_hit).data

    return jsonify({"hit": res}), 201


@app.route("/api/v1/hits/<int:hit_id>", methods=["PUT"])
def update_hit(hit_id):

    hit = Hits.query.get(int(hit_id))

    if not hit:
        abort(400)
    if (
        "title" not in request.json
        and "artist_id" not in request.json
        and "title_url" not in request.json
    ):
        abort(400)
    if "title" in request.json:
        title = request.json["title"]
        if not isinstance(title, str):
            abort(400)
        hit.title = title
    if "artist_id" in request.json:
        artist_id = request.json["artist_id"]
        check_artist = Artists.query.get(artist_id)
        if not check_artist:
            abort(400)
        if not isinstance(artist_id, int):
            abort(400)
        hit.artist_id = artist_id
    if "title_url" in request.json:
        title_url = request.json["title_url"]
        if not isinstance(title_url, str):
            abort(400)
        hit.title_url = title_url

    db.session.commit()

    hit_schema = SingleHitSchema()
    res = hit_schema.dump(hit).data

    return jsonify({"hit": res})


@app.route("/api/v1/hits/<int:hit_id>", methods=["DELETE"])
def delete_hit(hit_id):
    hit = Hits.query.get(int(hit_id))
    if not hit:
        abort(404)
    db.session.delete(hit)
    db.session.commit()

    return jsonify({"hit": "deleted"})


# helper functions


@app.route("/populate/<int:artists>/<int:hits>", methods=["GET"])
def populate(artists, hits):
    fake = Factory.create()
    t1 = [
        "Tajemnica",
        "Śmierć",
        "Kod",
        "Zabójstwo",
        "Śledztwo",
        "Proces",
        "Gra",
        "Bogactwo",
        "Teoria",
        "Miłość",
        "Dane",
        "Szyfry",
        "Zagadka",
        "Manipulacja",
        "Szansa",
        "Żal",
        "Broń",
        "Zdrowie",
        "Herezja",
        "Porwanie",
        "Poszukiwania",
        "Zabawa",
        "Programy",
        "Pieniądze",
        "Komunikat",
        "Leczenie",
        "Psychoterapia",
        "Rozrywka",
        "Ból",
        "Dziewczyny",
        "Chłopaki",
        "Druhny",
        "Rodzice",
        "Dzieci",
        "Dziadkowie",
        "Narzeczone",
        "Żony",
        "Szaleńcy",
        "Prześladowcy",
        "Smutek",
        "Zabawki",
        "Samotność",
        "Krew",
    ]

    t2 = [
        "Afrodyty",
        "Da Vinci",
        "ucznia",
        "Newtona",
        "Einsteina",
        "rycerza",
        "wojownika",
        "lęku",
        "sportowców",
        "komputerów",
        "nauki",
        "czarownic",
        "kierowców",
        "żołnierzy",
        "przyrody",
        "dla profesjonalistów",
        "naukowców",
        "zwierząt",
        "w Kosmosie",
        "na bogato",
        "w Polsce",
        "w Azji",
        "w Afryce",
        "w Europie",
        "w Ameryce",
        "we współczesnym świecie",
        "w górach",
        "nad morzem",
        "na rynku",
        "w polityce",
        "Polaków",
        "Europy",
        "na wojnie",
        "dla każdego",
        "w weekend",
        "w twoim domu",
        "lekarzy",
        "królów",
        "prezydentów",
        "zapomnianych",
        "Złego",
        "bogów",
        "szpiega",
        "w deszczu",
        "tyrana",
        "milionerów",
        "w wielkim mieście",
        "dla dzieci",
        "w ciemności",
    ]

    for _ in range(artists):
        artist_name = "{}".format(fake.first_name())
        artist_surname = "{}".format(fake.last_name())

        a = Artists(first_name=artist_name, last_name=artist_surname)

        db.session.add(a)
        db.session.commit()

    counter = 0
    art = Artists.query.all()
    for _ in art:
        counter += 1

    for _ in range(hits):
        h = Hits()
        h.title = "{} {}".format(choice(t1), choice(t2))
        h.artist_id = choice(range(1, counter + 1))
        db.session.add(h)
        db.session.commit()

    return jsonify({"database": "populated"})


if __name__ == "__main__":
    app.run()
