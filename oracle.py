
from enum import Enum, auto
from copy import deepcopy
from syslog import LOG_USER
from settings import BOARD_LENGTH
from square_board import SquareBoard


class ColumnClassification(Enum):
    FULL = -1        # imposible
    LOSE =  1        # imminent defeat
    BAD = 5         # Muy indeseable
    MAYBE = 10      # indeseable
    WIN = 100       # La mejor opción: gano por narices


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

    def __repr__(self):
        return f'{self.__class__}:{self.classification}'


class BaseOracle():

    def get_recommendation(self, board, player):
        """
        Returns a list of ColumnRecommendations
        """
        recommendations = []
        for i in range(len(board)):
            recommendations.append(
                self._get_column_recommendation(board, i, player))
        return recommendations

    def _get_column_recommendation(self, board, index, player):
        """
        Classifies a column as either FULL or MAYBE and returns an ColumnRecommendation
        """
        classification = ColumnClassification.MAYBE
        if board._columns[index].is_full():
            classification = ColumnClassification.FULL

        return ColumnRecommendation(index, classification)

    def no_good_options(self, board, player):
        """
        Detecta que todas las clasificaciones sean BAD o FULL
        """
        # obtener las clasificaciuones
        columnRecommendations = self.get_recommendation(board, player)

        # comprobamos que todas sean del tipo correcto
        result = True
        for rec in columnRecommendations:
            if (rec.classification == ColumnClassification.WIN) or (rec.classification == ColumnClassification.MAYBE):
                result = False
                break
        return result

    # métodos que han de ser sobre-escritos por mis subclases
    def update_to_bad(self, move):
        pass

    def backtrack(self, list_of_moves):
        pass


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
        tmp = self._play_on_tmp_board(board,index,player)

        will_lose = False
        for i in range(0, BOARD_LENGTH):
            if self._is_winning_move(tmp, i, player.opponent):
                will_lose = True
                break
        return will_lose

    def _is_winning_move(self, board, index, player):
        """
        Determina si al jugar en una posición, nos llevaría a ganar de inmediato
        """
        # hago una copia del tablero
        # juego en ella
        tmp = self._play_on_tmp_board(board, index, player)

        # determino si hay una victoria para player o no
        return tmp.is_victory(player.char)

    def _play_on_tmp_board(self, board, index, player):
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

    def _make_key(self, board_code, player):
        """
        La clave debe de combinar el board y el player, de la forma más sencilla posible
        """
        return f'{board_code.raw_code}@{player.char}'

    def get_recommendation(self, board, player):
        # Creamos la clave
        key = self._make_key(board.as_code(), player)

        # Miramos en el cache: si no está, calculo y guardo en cache
        if key not in self._past_recommendations:
            self._past_recommendations[key] = super(
            ).get_recommendation(board, player)

        # Devuelvo lo que está en el caché
        return self._past_recommendations[key]


class LearningOracle(MemoizingOracle):

    def update_to_bad(self, move):
        # crear clave
        key = self._make_key(move.board_code, move.player)
        # obtener la clasificación erronea
        recommendation = self.get_recommendation(
            SquareBoard.fromBoardCode(move.board_code), move.player)
        # corregirla
        recommendation[move.position] = ColumnRecommendation(
            move.position, ColumnClassification.BAD)
        # sustituirla
        self._past_recommendations[key] = recommendation

    def backtrack(self, list_of_moves):
        """
        Repasa todos las jugadas y si encuentra una en la cual todo 
        estaba perdido, quiere decir que la anterior tiene que ser 
        actualizada a BAD
        """
        # los moves están en orden inverso (el primero será el último)
        print('Learning...')

        # por cada move...
        for move in list_of_moves:
            # lo reclasifico a bad
            self.update_to_bad(move)

            # evaluo si todo estaba perdido tras esta clasificación
            board = SquareBoard.fromBoardCode(move.board_code)
            if not self.no_good_options(board, move.player):
                # si no todo estaba perdido, salgo. Sino, sigo
                break

        print(f'Size of knowledgebase: {len(self._past_recommendations)}')
