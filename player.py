
from oracle import BaseOracle, ColumnClassification, ColumnRecommendation
import random
from list_utils import all_same
from move import Move
from settings import DEBUG, BOARD_LENGTH
from beautifultable import BeautifulTable

class Player():
    """
    Juega en un tablero después de preguntar a un oráculo
    """

    def __init__(self, name,  char = None, opponent = None,   oracle=BaseOracle()) -> None:
        self.name = name
        self.char = char
        self._oracle = oracle
        self.opponent = opponent
        self.last_moves = []

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
        self._play_on(board, best.index, recommendations)

        

        
    def display_recommendations(self, board):
        recs = map(lambda x: str(x.classification).split('.')[
                   1].lower(), self._oracle.get_recommendation(board, self))

        bt = BeautifulTable()
        bt.rows.append(recs)

        bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]

        print(bt)

    def on_win(self):
        pass

    def on_lose(self):
        pass


    def _play_on(self, board, position, recommendations):
        # imprimo recs en caso de debug
        if DEBUG:
            self.display_recommendations(board)
            
        # juega en la pos
        board.add(self.char, position)
        # guarda la última jugada (siempre al principio de la lista)
        self.last_moves.insert(0, Move(position, board.as_code(), recommendations, self))
        
        

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
        # ordenamos por el valor de clasificación 
        valid = sorted(valid, key=lambda x : x.classification.value, reverse=True)
        # si son todas iguales, pillo una al azar
        if all_same(valid):
            return random.choice(valid)
        else:
            # si no lo son, pillo la más deseable (que será la primera)
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


class ReportingPlayer(Player):

    def on_lose(self):
        """
        Le pide al oráculo que revise sus recomendaciones
        """
        self._oracle.backtrack(self.last_moves)
        




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
