import pytest
from player import Player
from match import Match
from square_board import SquareBoard

xavier = Player('Dr Xavier')
otto = Player('Dr Octopus')


def test_different_players_have_different_chars():
    t = Match(xavier, otto)
    assert xavier.char != otto.char


def test_no_player_with_none_char():
    t = Match(otto, xavier)
    assert otto.char != None
    assert xavier.char != None


def test_next_player_is_round_robbin():
    t = Match(otto, xavier)
    p1 = t.next_player
    p2 = t.next_player
    assert p1 != p2


def test_get_winner():
    t = Match(xavier, otto)
    win_x = SquareBoard.fromList([['x', 'o', None, None, ],
                                  ['o', 'x', None, None, ],
                                  ['x', 'o', 'x', 'o', ],
                                  ['x', 'o', None, None, ],
                                  ])
    assert t.get_winner(win_x) != None
    assert t.get_winner(win_x) == xavier
    
