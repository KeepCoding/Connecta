import pytest

from list_utils import find_one, find_n, find_streak, first_elements, transpose, displace, all_same, reverse_list, collapse_list, collapse_matrix, replace_all_in_list, replace_all_in_matrix, reverse_matrix
from oracle import ColumnRecommendation, ColumnClassification


def test_find_one():
    needle = 1
    none = [0, 0, 5, 's']
    beginning = [1, None, 9, 6, 0, 0]
    end = ['x', '0', 1]
    several = [0, 0, 3, 4, 1, 3, 2, 1, 3, 4]

    assert find_one(none, needle) == False
    assert find_one(beginning, needle)
    assert find_one(end, needle)
    assert find_one(several, needle)


def test_find_n():
    assert find_n([2, 3, 4, 5, 6], 2, -1) == False
    assert find_n([1, 2, 3, 4, 5], 42, 2) == False
    assert find_n([1, 2, 3, 4, 5], 1, 2) == False
    assert find_n([1, 2, 3, 2, 4, 5], 2, 2)
    assert find_n([1, 2, 3, 4, 5, 4, 6, 4, 7, 4, 6], 4, 2)
    assert find_n([1, 2, 3, 4], 'x', 0) == True


def test_find_streak():
    assert find_streak([1, 2, 3, 4, 5], 4, -1) == False
    assert find_streak([1, 2, 3, 4, 5], 42, 2) == False
    assert find_streak([1, 2, 3, 4], 4, 1)
    assert find_streak([1, 2, 3, 1, 2], 2, 2) == False
    assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 3)
    assert find_streak([5, 5, 5, 1, 2, 3, 4], 5, 3)
    assert find_streak([1, 2, 5, 5, 5, 3, 4], 5, 3)
    assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 4) == False


def test_first_elements():
    original = [[0, 7, 3], [4, 0, 1]]

    assert first_elements(original) == [0, 4]


def test_transpose():
    original = [[0, 7, 3], [4, 0, 1]]
    transposed = [[0, 4], [7, 0], [3, 1]]

    assert transpose(original) == transposed
    assert transpose(transpose(original)) == original


def test_zero_distance_displace():
    l1 = [1, 2, 3, 4, 5, 6]
    l2 = [1]
    l3 = [[4, 5], ['x', 'o', 'c']]

    assert displace([], 0) == []
    assert displace(l1, 0) == l1
    assert displace(l2, 0) == l2
    assert displace(l3, 0) == l3


def test_positive_distance_displace():

    l1 = [1, 2, 3, 4, 5, 6]
    l2 = [1]
    l3 = [[4, 5], ['x', 'o', 'c']]
    l4 = [9, 6, 5]

    assert displace([], 2) == []
    assert displace(l1, 2) == [None, None, 1, 2, 3, 4]
    assert displace(l2, 3, '-') == ['-']
    assert displace(l3, 1, '#') == ['#', [4, 5]]
    assert displace(l4, 3, 0) == [0, 0, 0]


def test_negative_distance_displace():
    l1 = [1, 2, 3, 4, 5, 6]
    l2 = [1]
    l3 = [[4, 5], ['x', 'o', 'c']]
    l4 = [9, 6, 5]

    assert displace([], -2) == []
    assert displace(l1, -2) == [3, 4, 5, 6, None, None]
    assert displace(l2, -3, '-') == ['-']
    assert displace(l3, -1, '#') == [['x', 'o', 'c'], '#']
    assert displace(l4, -3, 0) == [0, 0, 0]


def test_reverse_list():
    assert reverse_list([]) == []
    assert reverse_list([1, 2, 3, 4, 5, 6]) == [6, 5, 4, 3, 2, 1]


def test_reverse_matrix():
    assert reverse_matrix([]) == []
    assert reverse_matrix([[0, 1, 2, 3], [0, 1, 2, 3]]) == [
        [3, 2, 1, 0], [3, 2, 1, 0]]


def test_all_same():
    assert all_same([9, 1, 2, 3, 4]) == False
    assert all_same([[], [], []])
    assert all_same([])

    assert all_same([ColumnRecommendation(0, ColumnClassification.WIN),
                     ColumnRecommendation(2, ColumnClassification.WIN)])

    assert all_same([ColumnRecommendation(0, ColumnClassification.MAYBE),
                     ColumnRecommendation(0, ColumnClassification.WIN)]) == False


def test_collapse_list():
    assert collapse_list([]) == ''
    assert collapse_list(['o', 'x', 'x', 'o']) == 'oxxo'
    assert collapse_list(['x', 'x', None, None, None]) == 'xx...'


def test_collapse_matrix():
    assert collapse_matrix([]) == ''
    assert collapse_matrix([['x', 'x', None],
                           ['o', 'x', 'x'],
                           ['o', None, None]]) == 'xx.|oxx|o..'


def test_replace_all_in_list():
    assert replace_all_in_list([None, 3, '546', 33, None], None, '#') == [
        '#', 3, '546', 33, '#']
    assert replace_all_in_list([1, 2, 3, 4, 5], 'e', 42) == [1, 2, 3, 4, 5]
    assert replace_all_in_list([], 34, 43) == []


def test_replace_all_in_matrix():
    # caso normal: tiene lo viejo
    assert replace_all_in_matrix([[1, 2, 3, 'n', 'n', None],
                                  [4, 5, 'n']], 'n', '#') == [[1, 2, 3, '#', '#', None], [4, 5, '#']]
    # caso raro: no tiene lo viejo
    assert replace_all_in_matrix([[None, None, 2, True], [4, 5, '#']], 'k', 42) == [[
        None, None, 2, True],  [4, 5, '#']]
    # caso más raro: lista de listas vacías
    assert replace_all_in_matrix([], None, 7) == []
    assert replace_all_in_matrix([[], []], None, 7) == [[], []]
