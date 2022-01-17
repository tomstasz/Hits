from faker import Factory
from random import choice

from flask import jsonify, abort, make_response, request
from .app import app, db
from .models import (
    Artists,
    Hits,
    ArtistSchema,
    HitsSchema,
    SingleHitSchema,
    SimpleHitSchema,
)


@app.errorhandler(404)
def not_found(error):
    """Handle 'not found' errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    """Handle 'bad request' errors"""
    return make_response(jsonify({"error": "Bad request"}), 400)


@app.errorhandler(500)
def server_error_request(error):
    """Handle server errors"""
    return make_response(jsonify({"error": "Server error"}), 500)


@app.route("/api/v1/hits", methods=["GET"])
def get_hits():
    """Show list of hits"""
    all_hits = Hits.query.order_by("created_at").limit(20)
    hit_schema = HitsSchema(many=True)
    res = hit_schema.dump(all_hits)

    return jsonify({"hits": res})


@app.route("/api/v1/hits/<int:hit_id>", methods=["GET"])
def get_hit_detail(hit_id):
    """Show single hit details"""
    hit = Hits.query.get(hit_id)
    if not hit:
        abort(404)
    hit_schema = SingleHitSchema()
    res = hit_schema.dump(hit)
    return jsonify({"hit": res})


@app.route("/api/v1/hits", methods=["POST"])
def create_hit():
    """Add new hit to the database"""
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
    res = hit_schema.dump(new_hit)

    return jsonify({"hit": res}), 201


@app.route("/api/v1/hits/<int:hit_id>", methods=["PUT"])
def update_hit(hit_id):
    """Update existing hit"""
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
    res = hit_schema.dump(hit)

    return jsonify({"hit": res})


@app.route("/api/v1/hits/<int:hit_id>", methods=["DELETE"])
def delete_hit(hit_id):
    """Remove hit from the database"""
    hit = Hits.query.get(int(hit_id))
    if not hit:
        abort(404)
    db.session.delete(hit)
    db.session.commit()

    return jsonify({"hit": "deleted"})


# helper functions


@app.route("/populate/<int:artists>/<int:hits>", methods=["GET"])
def populate(artists, hits):
    """Generate false artists and hits"""
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
