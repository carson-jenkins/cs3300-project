# golf_app/tests.py

from django.test import TestCase
from .models import Player, Game, PlayerGameScore
from datetime import date

class PlayerModelTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        Player.objects.create(name="John Doe", handicap=15)

    def test_player_creation(self):
        player = Player.objects.get(name="John Doe")
        self.assertEqual(player.name, "John Doe")
        self.assertEqual(player.handicap, 15)

class GameModelTest(TestCase):
    def setUp(self):
        # Creating a player for the game
        self.player = Player.objects.create(name="Jane Doe", handicap=12)
        # Creating a game instance
        self.game = Game.objects.create(course_name="Sunset Golf Course", date=date.today())

    def test_game_creation(self):
        self.assertEqual(self.game.course_name, "Sunset Golf Course")
        self.assertEqual(self.game.date, date.today())

class PlayerGameScoreTest(TestCase):
    def setUp(self):
        # Create a player and a game for testing scores
        self.player = Player.objects.create(name="Alice Smith", handicap=10)
        self.game = Game.objects.create(course_name="Lakeside", date=date.today())
        self.score = PlayerGameScore.objects.create(player=self.player, game=self.game, scores='5,4,3,4,5,4,3,4,5')

    def test_score_retrieval(self):
        score = PlayerGameScore.objects.get(player=self.player, game=self.game)
        self.assertEqual(score.scores, '5,4,3,4,5,4,3,4,5')

    # Additional tests can be written to test specific functionalities, like score calculations or updates.