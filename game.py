
import pyfiglet

from square_board import SquareBoard
from match import Match
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
            # obtengo el juagdor de turno
            # le hago jugar
            # muestro su jugada
            # imprimo el tablero
            # si el juego ha terminado,
                # muestro resultado final
                # salgo del bucle
        pass


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
