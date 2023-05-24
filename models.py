import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

"""complete"""

db = SQLAlchemy()

database_path = os.environ['DATABASE_URL']

# database_path = 'postgres://hollywood_casting_agency_m681_user:bbPt1ZB3oGcimsjjPOMPl3UeqEaa2fTK@dpg-chn0oum7avj3o34gjel0-a.oregon-postgres.render.com/hollywood_casting_agency_m681'


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


actors_in_movie = db.Table('actors_in_movie',
                           db.Column('movie_id', db.Integer, db.ForeignKey(
                               'movies.id', ondelete='CASCADE'), primary_key=True),
                           db.Column('actor_id', db.Integer, db.ForeignKey(
                               'actors.id', ondelete='CASCADE'), primary_key=True)
                           )


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_year = Column(String)
    actors = db.relationship(
        'Actor', secondary=actors_in_movie, backref=db.backref('movies', lazy=True))

    def __init__(self, title, release_year):
        self.title = title
        self.release_year = release_year

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year,
            'actors': [
                {
                    'id': actor.id,
                    'name': actor.name
                }
                for actor in self.actors]
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'movies': [
                {
                    'id': Movie.id,
                    'name': Movie.title
                }
                for movie in self.movies]
        }
