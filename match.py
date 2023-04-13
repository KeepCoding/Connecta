

class Match:
    def __init__(self, player1, player2):
        player1.char = 'x'
        player2.char = 'o'
        player1.opponent = player2
        self._players = {'x' : player1, 'o' : player2}
        self._round_robbin = [player1, player2]
        assert (player1.opponent is not None) and (player2.opponent is not None), "Players are required to have an opponent for recommendations"

    @property 
    def next_player(self):
        next_one = self._round_robbin[0]
        self._round_robbin.reverse()
        return next_one
    
    def get_player(self, char):
        return self._players[char]

    
    def get_winner(self, board):
        """
        Returns the winning player. If there's no winner, return None.
        This doesn't mean it's a tie, the game might not be finished yet.
        """
        if board.is_victory('x') :
            return self.get_player('x')
        elif board.is_victory('o') :
            return self.get_player('o')
        else:
            return None

            
    def is_match_over(self):
        """
        pregunta al usuario si hay huevos para otra partida
        """
        result = True
        while True:
            answer = input('Would you like to play another match? (Y/N) ').upper()
            if answer == 'Y':
                result = False
                break
            elif answer == 'N':
                result = True
                break

        return result


    
