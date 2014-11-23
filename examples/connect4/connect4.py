from ANN.ANN import NeuralNetwork


class Connect4(object):
    def __init__(self):
        self.pieces = [[] for i in xrange(7)]
        self.turn = 0

    def check(self, column):
        vectors = ((1, 0), (1, 1), (0, 1), (-1, 1))
        for i in xrange(4):
            row = []
            for j in xrange(-3, 4):
                try:
                    if column + j*vectors[i][0] >= 0 and len(self.pieces[column]) - 1 + j*vectors[i][1] >= 0:
                        row.append(self.pieces[column + j*vectors[i][0]][len(self.pieces[column]) - 1 + j*vectors[i][1]])
                    else:
                        row.append(None)
                except IndexError:
                    row.append(None)
            for j in xrange(4):
                if row[j] == row[j + 1] == row[j + 2] == row[j + 3] is not None:
                    return row[j]
        if sum(len(piece_column) for piece_column in self.pieces) == 42:
            return 2

    def move(self, column):
        for i in xrange(column, column + 7):
            if len(self.pieces[i % 7]) < 6:
                self.pieces[i % 7].append(self.turn)
                self.turn = 1 - self.turn
                return self.check(i % 7)

    def input(self, inputs):
        return self.move(sum(j*2**i for i, j in enumerate(inputs)))

    def output(self):
        return [piece for piece_column in self.pieces for piece in piece_column + [1] + [0] * (6 - len(piece_column))]

    def __str__(self):
        output = ''
        for i in xrange(6):
            output += i and '\n|' or '|'
            for piece_column in self.pieces:
                try:
                    output += piece_column[5 - i] and 'X|' or 'O|'
                except IndexError:
                    output += ' |'
        output += '\n 0 1 2 3 4 5 6 '
        return output


def start():
    players = input('Players: ')
    if players == 0:
        ANNs = [NeuralNetwork(49, 3, 49, 2) for i in xrange(20)]
        for ANN0 in ANNs[0:10]:
            scores = []
            for i in xrange(100):
                scores.append(0)
                for ANN1 in ANNs[10:20]:
                    connect4 = Connect4()
                    winner = None
                    while winner is None:
                        if connect4.turn == 0:
                            winner = connect4.input(inputs=ANN0.calculate(inputs=connect4.output(), increment=i/100.0))
                        else:
                            winner = connect4.input(inputs=ANN1.calculate(inputs=connect4.output()))
                    print connect4
                    if winner == 2:
                        print "It's a tie!"
                    else:
                        scores[-1] += 1 - 2*winner
                        print "{0} wins!".format(winner and 'X' or 'O')
            for i, score in enumerate(scores):
                if score == max(scores):
                    ANN0.mutate(increment=i/100.0)
                    break
        for ANN1 in ANNs[10:20]:
            scores = []
            for i in xrange(100):
                scores.append(0)
                for ANN0 in ANNs[0:10]:
                    connect4 = Connect4()
                    winner = None
                    while winner is None:
                        if connect4.turn == 0:
                            winner = connect4.input(inputs=ANN0.calculate(inputs=connect4.output()))
                        else:
                            winner = connect4.input(inputs=ANN1.calculate(inputs=connect4.output(), increment=i/100.0))
                    print connect4
                    if winner == 2:
                        print "It's a tie!"
                    else:
                        scores[-1] += 2*winner - 1
                        print "{0} wins!".format(winner and 'X' or 'O')
            for i, score in enumerate(scores):
                if score == max(scores):
                    ANN1.mutate(increment=i/100.0)
                    break
    if players == 1:
        connect4 = Connect4()
        ANN = NeuralNetwork(inputs=49, outputs=3, hidden=49, rows=5)
        winner = None
        while winner is None:
            print connect4
            if connect4.turn == 0:
                winner = connect4.move(column=input('{0}\'s turn: '.format(connect4.turn and 'X' or 'O')))
            else:
                winner = connect4.input(inputs=ANN.calculate(inputs=connect4.output()))
        print connect4
        if winner == 2:
            print "It's a tie!"
        else:
            print "{0} wins!".format(winner and 'X' or 'O')
    if players == 2:
        connect4 = Connect4()
        winner = None
        while winner is None:
            print connect4
            winner = connect4.move(column=input('{0}\'s turn: '.format(connect4.turn and 'X' or 'O')))
        print connect4
        if winner == 2:
            print "It's a tie!"
        else:
            print "{0} wins!".format(winner and 'X' or 'O')
