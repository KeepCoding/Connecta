
import pyfiglet
from beautifultable import BeautifulTable
from settings import BOARD_LENGTH
from square_board import SquareBoard
from match import Match
from list_utils import reverse_matrix
from player import Player, HumanPlayer
from enum import Enum, auto


class RoundType(Enum):
    COMPUTER_VS_COMPUTER = auto()
    COMPUTER_VS_HUMAN = auto()


class DifficultyLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class Game():

    def __init__(self,
                 round_type=RoundType.COMPUTER_VS_COMPUTER,
                 match=Match(Player('Chip'), Player('Chop'))):

        # tablero vacío sobre el que vamos a jugar
        self.board = SquareBoard()

        # tipo de partida
        self.round_type = round_type

        # match
        self.match = match

    def start(self):
        # Imprimo el nombre del juego
        self.print_logo()
        # Pido al usuario valores deseados para match y tipo de partida
        self._configure_by_user()
        # Arranco el game loop
        self._start_game_loop()

    def _start_game_loop(self):
        # bucle infinito
        while True:
            # obtengo el juagdor de turno
            current_player = self.match.next_player
            # le hago jugar
            current_player.play(self.board)
            # muestro su jugada
            self._display_move(current_player)
            # imprimo el tablero
            self._display_board()
            # si el juego ha terminado,
            if self._is_game_over():
                # muestro el resultado final
                self._display_result()
                # salgo del bucle
                break

    def _display_result(self):
        winner = self.match.get_winner(self.board)
        if winner != None:
            print(f'\n{winner.name} ({winner.char}) wins!!!')
        else:
            print(
                f'\nA tie between {self.match.get_player("x")} (x) and {self.match.get_player("o")} (o)!')

    def _is_game_over(self):
        """
        Game is over if there's a winner or there's a tie
        """
        winner = self.match.get_winner(self.board)
        if winner != None:
            return True  # there is a winner
        elif self.board.is_full():
            return True  # tie
        else:
            return False  # the game is still on

    def _display_move(self, player):
        print(
            f'\n{player.name} ({player.char}) has moved in column #{player.last_move}\n')

    def _display_board(self):
        """
        Print the board in its current state
        """
        # obtener una matriz de caracteres a partir del tablero
        matrix = self.board.as_matrix()
        matrix = reverse_matrix(matrix)
        
        # crear un atabla con beautifultable 
        bt = BeautifulTable()
        for col in matrix:
            bt.columns.append(col)
        bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]

        # imprimirla
        print(bt)

    def _configure_by_user(self):
        """
        Pido al usuario valores deseados para match y tipo de partida
        """

        # determino el tipo de partida (humano vs comp, comp vs comp)
        self.round_type = self._get_round_type()

        # Creamos los dos jugadores
        self.match = self._make_match()

    def _make_match(self):
        """
        Player1 siempre será el ordeñador
        """

        if self.round_type == RoundType.COMPUTER_VS_COMPUTER:
            # ambos jugadores robóticos
            player1 = Player('T-X')
            player2 = Player('T-1000')
        else:
            # humano contro ordenador
            player1 = Player('T-800')
            player2 = HumanPlayer(name=input('Enter your name, puny human: '))

        # creamos la partida
        return Match(player1, player2)

    def _get_round_type(self):
        """
        Ask the user
        """
        print("""
        Select the type of round:

        1) Computer vs Computer
        2) Computer vs Human
        """)

        response = ''
        while response != '1' and response != '2':
            response = input('PLease type either 1 or 2:  ')

        if response == '1':
            return RoundType.COMPUTER_VS_COMPUTER
        else:
            return RoundType.COMPUTER_VS_HUMAN

    def print_logo(self):
        logo = pyfiglet.Figlet(font='stop')
        print(logo.renderText('Connecta'))
