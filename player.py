from oracle import BaseOracle, ColumnClassification, ColumnRecommendation


class Player():
    """
    Juega en un tablero después de preguntar a un oráculo
    """

    def __init__(self, name,  char = None, opponent = None,   oracle=BaseOracle()) -> None:
        self.name = name
        self.char = char
        self._oracle = oracle
        self.opponent = opponent

    @property
    def opponent(self):
        return self._opponent

    @opponent.setter
    def opponent(self, other):
        self._opponent = other
        if other != None:
            assert other.char != self.char
            other._opponent = self


    def play(self, board):
        """
        Elige la mejor columna de aquellas que recomienda el oráculo
        """
        # Pregunto al oráculo
        (best, recommendations) = self._ask_oracle(board)

        # juego en la mejor
        self._play_on(board, best.index)

    def _play_on(self, board, position):
        # juega en la pos
        board.add(self.char, position)

    def _ask_oracle(self, board):
        """
        Pregunta al oráculo y devuielve la mejor opción
        """
        # obtenemos las recommendaciones
        recommendations = self._oracle.get_recommendation(board, self)

        # seleccionamos la mejro
        best = self._choose(recommendations)

        return (best, recommendations)

    def _choose(self, recommendations):
        # quitamos las no validas
        valid = list(filter(lambda x: x.classification !=
                     ColumnClassification.FULL, recommendations))

        # pillamos la primera de las válidas
        return valid[0]


class HumanPlayer(Player):

    def __init__(self, name, char = None):
        super().__init__(name, char)

    def _ask_oracle(self, board):
        """
        Le pido al humano que es mi oráculo
        """
        while True:
            # pedimos columna al humano
            raw = input('Select a column, puny human: ')
            # verificamos que su respuesta no sea una idiotez
            if _is_int(raw) and _is_within_column_range(board, int(raw)) and _is_non_full_column(board, int(raw)):

                # si no lo es, jugamos donde ha dicho y salimos del bucle
                pos = int(raw)
                return (ColumnRecommendation(pos, None), None)


# funciones de validación de índice de columna
def _is_non_full_column(board, num):
    return not board._columns[num].is_full()


def _is_within_column_range(board, num):
    return num >= 0 and num < len(board)


def _is_int(aString):
    try:
        num = int(aString)
        return True
    except:
        return False
