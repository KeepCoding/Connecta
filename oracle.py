
from enum import Enum, auto
from copy import deepcopy
from settings import BOARD_LENGTH

class ColumnClassification(Enum):
    FULL    = -1        # imposible
    LOSE    = 1         # Muy indeseable
    MAYBE   = 10        # indeseable
    WIN     = 100       # La mejor opción: gano por narices

class ColumnRecommendation():
    def __init__(self, index, classification):
        self.index = index
        self.classification = classification

    def __eq__(self, other):
        # si son de clases distintas, pues distintos
        if not isinstance(other, self.__class__):
            return False
        # sólo importa la clasificación
        else:
            return self.classification == other.classification

    def __hash__(self) -> int:
        return hash((self.index, self.classification))

class BaseOracle():

    def get_recommendation(self, board, player):
        """
        Returns a list of ColumnRecommendations
        """
        recommendations = []
        for i in range(len(board)):
            recommendations.append(self._get_column_recommendation(board, i, player))
        return recommendations

    def _get_column_recommendation(self, board, index, player):
        """
        Classifies a column as either FULL or MAYBE and returns an ColumnRecommendation
        """
        classification = ColumnClassification.MAYBE
        if board._columns[index].is_full():
            classification = ColumnClassification.FULL

        return ColumnRecommendation(index, classification)

class SmartOracle(BaseOracle):
    def _get_column_recommendation(self, board, index, player):
        """
        Afina la clasificacion de super e intenta encontrar columnas WIN
        """
        recommendation = super()._get_column_recommendation(board, index, player)
        if recommendation.classification == ColumnClassification.MAYBE:
            # se puede mejorar
            if self._is_winning_move(board, index, player):
                recommendation.classification = ColumnClassification.WIN
            elif self._is_losing_move(board, index, player):
                recommendation.classification = ColumnClassification.LOSE

        return recommendation

    def _is_losing_move(self, board, index, player):
        """
        Si player juega en index, ¿genera una jugada vencedora para el 
        oponente el alguna de las demás columnas?
        """
        will_lose = False
        for i in range(0, BOARD_LENGTH):
            if self._is_winning_move(board, i, player.opponent):
                will_lose = True
                break
        return will_lose

    def _is_winning_move(self,board, index, player):
        """
        Determina si al jugar en una posición, nos llevaría a ganar de inmediato
        """
        # hago una copia del tablero
        # juego en ella
        tmp = self._play_on_tmp_board(board, index, player )

        # determino si hay una victoria para player o no
        return tmp.is_victory(player.char)

    def _play_on_tmp_board(self, board, index, player ):
        """
        Crea una copia del board y juega en él
        """
        tmp = deepcopy(board)

        tmp.add(player.char, index)

        # devuelvo la copia alterada
        return tmp


class MemoizingOracle(SmartOracle):
    """
    El método get_recommendation está ahora memoizado
    """
    def __init__(self) -> None:
        super().__init__()
        self._past_recommendations = {}

    def _make_key(board, player):
        """
        La clave debe de combinar el board y el player, de la forma más sencilla posible
        """
        return f'{board.as_code().raw_code}@{player.char}'

    def get_recommendation(self, board, player):
        # Creamos la clave
        key = self._make_key(board, player)

        # Miramos en el cache: si no está, calculo y guardo en cache
        if key not in self._past_recommendations:
            self._past_recommendations[key] = super().get_recommendation(board, player)

        # Devuelvo lo que está en el caché
        return self._past_recommendations[key]
    
    
