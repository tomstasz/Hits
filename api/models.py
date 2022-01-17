from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from flask_marshmallow.fields import AbsoluteURLFor
from marshmallow.fields import Nested
from .app import db


class Artists(db.Model):
    """Artist performing hits"""

    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hits = db.relationship("Hits", backref="artist", lazy="dynamic")

    def __repr__(self):
        return "<Artist {} {}>".format(self.first_name, self.last_name)


class Hits(db.Model):
    """Hit performed by artist"""

    __tablename__ = "hits"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    title_url = db.Column(db.String(120))
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<Hit {}>".format(self.title)


class ArtistSchema(ModelSchema):
    """Schema to serialize artist objects"""

    class Meta:
        model = Artists
        fields = ("id", "first_name", "last_name")


class HitsSchema(ModelSchema):
    """Schema to serialize list of hit objects"""

    title_url = AbsoluteURLFor("get_hit_detail", hit_id="<id>")

    class Meta:
        model = Hits
        fields = ("id", "title", "title_url")


class SingleHitSchema(ModelSchema):
    """Schema to serialize single hit object"""

    title_url = AbsoluteURLFor("get_hit_detail", hit_id="<id>")
    artist = Nested(ArtistSchema)

    class Meta:
        model = Hits
        exclude = ["updated_at"]


class SimpleHitSchema(ModelSchema):
    """Simplified schema to serialize single hit object"""

    artist = Nested(ArtistSchema)

    class Meta:
        model = Hits
        fields = ("id", "title", "artist")
