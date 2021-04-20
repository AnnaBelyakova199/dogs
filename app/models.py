import enum
import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class DogColors(str, enum.Enum):
    brown = 'brown'
    black = 'black'
    white = 'white'


class Dogs(db.Model):
    __tablename__ = 'dogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    breed = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    color = db.Column(db.Enum(DogColors))

    father_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable=True)
    father = db.relationship("Dogs", remote_side=[id], foreign_keys=[father_id])

    mother_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable=True)
    mother = db.relationship("Dogs", remote_side=[id], foreign_keys=[mother_id])
