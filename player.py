from oracle import BaseOracle, ColumnClassification


class Player():
    """
    Juega en un tablero después de preguntar a un oráculo
    """

    def __init__(self, name, char, oracle = BaseOracle()) -> None:
        self.name = name
        self.char = char
        self._oracle = oracle

    def play(self, board):
        """
        Elige la mejor columna de aquellas que recomienda el oráculo
        """
        # obtén las recomendaciones
        recommendations = self._oracle.get_recommendation(board, self)

        # selecciona la mejor de todas
        best = self._choose(recommendations)
        # juega en ella
        board.add(self.char, best.index)




    def _choose(self, recommendations):
        # quitamos las no validas
        valid = list(filter(lambda x : x.classification != ColumnClassification.FULL, recommendations))

        # pillamos la primera de las válidas
        return valid[0]
        
        

