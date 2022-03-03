import pytest
from game import Game

def test_created_with_defaults():
    game = Game()
    assert game.round_type != None
    assert game.match != None
    assert game.board != None
    assert game.board.is_full() == False
    