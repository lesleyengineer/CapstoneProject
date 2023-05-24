import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from app import create_app
from movie_options import movies, actors, new_movie, new_actor, new_movie_no_actor_id, new_actor_no_movie_id, update_movie, update_actor


class HollywoodCastingTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        def tearDown(self):
            """Executed after reach test"""
            pass

    # home page test

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        '''TESTS FOR EXECUTIVE PRODUCER'''

    # test for get movies

    def test_get__movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movie_fail(self):
        res = self.client().put('/movies',
                                json={'id': 8, 'title': 'Harry Potter and The Final Battle', 'release_year': '2023'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['message'], 'bad request')
        self.assertEqual(data['success'], False)

    # test for get actors

    def test_get__actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_fail(self):
        res = self.client().put(
            '/actors', json={'id': 10, 'name': 'Brendan Gleeson', 'age': '70'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['message'], 'bad request')
        self.assertEqual(data['success'], False)

    # create a new movie

    def test_post_movie(self):
        res = self.client().post('/movies', json=new_movie.format())
        data = json.loads(res.data)

        movie = Movie.query.order_by(Movie.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], movie.id)

    def test_post_movie_fail(self):
        res = self.client().post('/movies', json=new_movie_no_actor_id.format())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # create a new actor

    def test_post_actor(self):
        res = self.client().post('/actors', json=new_actor.format())
        data = json.loads(res.data)

        actor = Actor.query.order_by(Actor.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], actor.id)

    def test_post_actor_fail(self):
        res = self.client().post('/actors', json=new_actor_no_movie_id.format())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # update a movie

    def test_patch_movie(self):
        res = self.client().patch('/movies/2', json=update_movie)
        data = json.loads(res.data)

        movie_id = 2

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['actors'][0]['id'], 1)
        self.assertEqual(data['movie']['actors'][1]['id'], 2)
        self.assertEqual(data['movie']['id'], movie_id)
        self.assertEqual(data['movie']['release_year'], '2003')
        self.assertEqual(data['movie']['title'],
                         'Harry Potter and the Chamber of Fun')

    def test_patch_movies_fail(self):
        res = self.client().put("/movies/2", json=update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

    # update an actor

    def test_patch_actor(self):
        res = self.client().patch('/actors/2', json=update_actor)
        data = json.loads(res.data)

        actor_id = 2

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['movies'][0]['id'], 1)
        self.assertEqual(data['actor']['movies'][1]['name'], 'Emma Watson')
        self.assertEqual(data['actor']['id'], actor_id)
        self.assertEqual(data['actor']['age'], '33')
        self.assertEqual(data['actor']['gender'], 'female')

    def test_patch_actors_fail(self):
        res = self.client().put("/actors/6", json=update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

    # delete movie

    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)

    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # delete actor

    def test_delete_actor(self):
        res = self.client().delete('/actor/1')
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/26')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
