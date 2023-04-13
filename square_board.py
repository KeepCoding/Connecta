from linear_board import LinearBoard
from list_utils import collapse_matrix, displace_matrix, replace_all_in_matrix, reverse_matrix, transpose
from string_utils import explode_list_of_strings
from settings import BOARD_LENGTH

class SquareBoard():
    """
    Representa un tablero cuadrado
    """

    @classmethod
    def fromList(cls, list_of_lists):
        """
        Transforma una lista de listas en una list de LinearBoard
        """
        board = cls()
        board._columns = list(map(lambda element: LinearBoard.fromList(element), list_of_lists) )
        return board

    @classmethod
    def fromBoardCode(cls, board_code):
        return cls.fromBoardRawCode(board_code.raw_code)

    @classmethod
    def fromBoardRawCode(cls, board_raw_code):
        """
        Transforma una cadena en formato de BoardCode en una 
        lista de LinearBoards y luego lo transfroma en un tablero cuadrado
        """
        # 1. Convertir la cadena del código en una lista de cadenas
        list_of_strings = board_raw_code.split("|")

        # 2. Transformar cada cadena en una lista de caracteres
        matrix = explode_list_of_strings(list_of_strings)

        # 3. Cambiamos todas las ocurrencias de . por None
        matrix = replace_all_in_matrix(matrix, '.', None)

        # 4. Transformamos esa lista en un SquareBoard 
        return cls.fromList(matrix)


    def __init__(self):
        self._columns = [LinearBoard() for _ in range(BOARD_LENGTH)]

    def __repr__(self):
        return f'{self.__class__}: {self._columns}'

    def __len__(self):
        return len(self._columns)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns

    def __hash__(self):
        return hash(self._columns)
    
    def is_full(self):
        """
        True si todos los LinearBoards están llenos
        """
        result = True
        for lb in self._columns:
            result = result and lb.is_full()
        return result

    def as_code(self):
        return BoardCode(self)

    
    def as_matrix(self):
        """
        Devuelve una representación en fromato de matriz, es decir,
        lista de listas.
        """
        return list(map(lambda x: x._column, self._columns))

    # Juega una ficha en una columna
    def add(self, char, column):
        self._columns[column].add(char)

    # Detectra victorias
    def is_victory(self, char):
        return self._any_vertical_victory(char) or self._any_horizontal_victory(char) or self._any_rising_victory(char) or self._any_sinking_victory(char)

    def _any_vertical_victory(self, char):
        result = False
        for lb in self._columns:
            result = result or lb.is_victory(char)
        return result

    def _any_horizontal_victory(self, char):
        # Transponemos _columns
        transp = transpose(self.as_matrix())
        # Creamos un tablero temporal con esa matriz transpuesta
        tmp = SquareBoard.fromList(transp)

        # comprobamos si tiene una victoria temporal
        return tmp._any_vertical_victory(char)


    def _any_rising_victory(self, char):
        # obtener las columnas
        m = self.as_matrix()
        # las invertimos
        rm = reverse_matrix(m)
        # creamos tablero temporal con esa matriz
        tmp = SquareBoard.fromList(rm)
        # devolvemos si tiene una victoria descendente
        return tmp._any_sinking_victory(char)



    def _any_sinking_victory(self, char):
        # Obtenemos las columnas como una matriz
        m = self.as_matrix()
        # la desplazamos
        d = displace_matrix(m)
        # creamos un tablero temporal con esa matriz
        tmp = SquareBoard.fromList(d)
        # averiguamos si tiene una vitroia horizontal
        return tmp._any_horizontal_victory(char)


    # dunders
    def __repr__(self):
        return f'{self.__class__}:{self._columns}'



class BoardCode:

    def __init__(self, board):
        self._raw_code = collapse_matrix(board.as_matrix())

    @property
    def raw_code(self):
        return self._raw_code

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            # solo importa el raw code
            return self.raw_code == other.raw_code

    def __hash__(self):
        return hash(self.raw_code)

    def __repr__(self):
        return f'{self.__class__}: {self.raw_code}'