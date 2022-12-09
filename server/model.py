from . import db
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Images_Db(Base):
    __tableName__ = "images_dicts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    dictionary = db.Column(db.JSON)
