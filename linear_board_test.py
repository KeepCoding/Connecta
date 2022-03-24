import pytest
from linear_board import LinearBoard
from settings import BOARD_LENGTH, VICTORY_STRIKE

def test_empty_board():
    empty = LinearBoard()
    assert empty.is_full() == False
    assert empty.is_victory('x') == False

def test_add():
    b = LinearBoard()
    for _ in range(BOARD_LENGTH):
        b.add('x')
    assert b.is_full() == True

def test_victory():
    b = LinearBoard()
    for _ in range(VICTORY_STRIKE):
        b.add('x')

    assert b.is_victory('o') == False
    assert b.is_victory('x') == True

def test_tie():
    b = LinearBoard()

    b.add('o')
    b.add('o')
    b.add('x')
    b.add('o')

    assert b.is_tie('x', 'o')


def test_add_to_full():
    full = LinearBoard()
    for _ in range(BOARD_LENGTH):
        full.add('x')
    
    full.add('x')
    assert full.is_full()
    