import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from movie_options import movies, actors
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt):
    options = Movie.query.all()
    movies = [movie.format() for movie in options]

    return jsonify({
        'success': True,
        'movies': movies
    })


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movies(jwt):
    body = request.get_json()
    new_title = body.get('title', None)
    new_release_year = body.get('release_year', None)
    actors = body.get('actors', None)

    try:
        new_movie = Movie(title=new_title, release_year=new_release_year)

        if actors:
            for id in actors:
                actor = Actor.query.filter(Actor.id == id).one_or_none()
                if actor:
                    new_movie.actors.append(actor)
                else:
                    abort(404)

        new_movie.insert()

        return jsonify(
            {
                'success': True,
                'posted': new_movie.id,
                'movie': new_movie.format()
            }
        )
    except:
        abort(400)


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(jwt):
    options = Actor.query.all()
    actors = [actor.format() for actor in options]

    return jsonify(
        {
            'success': True,
            'actors': actors
        }
    )


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(jwt):
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)
    movies = body.get('movies', None)

    try:
        new_actor = Actor(name=new_name, age=new_age, gender=new_gender)

        if movies:
            for id in movies:
                movie = Movie.query.filter(Movie.id == id).one_or_none()
                if movie:
                    new_actor.movies.append(movie)
                else:
                    abort(404)

        new_actor.insert()

        return jsonify(
            {
                'success': True,
                'created': new_actor.id,
                'actor': new_actor.format()
            }
        )
    except:
        abort(400)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, movie_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(400)

        movie.delete()

        return jsonify(
            {
                'success': True,
                'deleted': movie_id
            }
        )

    except:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(400)

        actor.delete()

        return jsonify(
            {
                'success': True,
                'deleted': actor_id
            }
        )
    except:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def edit_movie(jwt, movie_id):

    body = request.get_json()
    new_title = body.get('title', None)
    new_release_year = body.get('release_year', None)
    actors = body.get('actors', None)

    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        if new_title:
            movie.title = new_title

        if new_release_year:
            movie.release_year = new_release_year

        if actors:
            movie.actors = []
            for id in actors:
                actor = Actor.query.filter(Actor.id == id).one_or_none()
                if actor:
                    movie.actors.append(actor)
                else:
                    abort(404)

        movie.update()

        return jsonify(
            {
                'success': True,
                'movie': movie.format()
            }
        )

    except Exception as e:
        print(e)
        abort(400)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def edit_actor(jwt, actor_id):

    body = request.get_json()
    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)
    movies = body.get('movies', None)

    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        if new_name:
            actor.name = new_name

        if new_age:
            actor.age = new_age

        if new_gender:
            actor.gender = new_gender

        if movies:
            actor.movies = []
            for id in movies:
                movie = Movie.query.filter(Movie.id == id).one_or_none()
                if movie:
                    actor.movies.append(movie)
                else:
                    abort(404)

        actor.update()

        return jsonify(
            {
                'success': True,
                'actor': actor.format()
            }
        )

    except:
        abort(400)


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 400,
        'message': 'BAD REQUEST',
        'success': 'false'
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 404,
        'message': 'NOT FOUND',
        'success': 'false'
    })


@app.errorhandler(422)
def unprocessable_content(error):
    return jsonify({
        'error': 422,
        'message': 'UNPROCESSABLE CONTENT',
        'success': 'false'
    })


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'error': 500,
        'message': 'INTERNAL SERVER ERROR',
        'success': 'false'
    })


@app.errorhandler(AuthError)
def auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code

    return response
