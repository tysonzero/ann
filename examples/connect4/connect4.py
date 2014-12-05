from multiprocessing import Process
from os import mkdir
from pickle import dump, load
from random import randint


from ann.ann import NeuralNetwork


class Connect4(object):
    def __init__(self, anns=[None, None]):
        self.pieces = [[] for i in xrange(7)]
        self.anns = anns
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
        return [piece for piece_column in self.pieces for piece in piece_column + [1] + (6 - len(piece_column))*[0]]

    def play(self, output=True):
        winner = None
        while winner is None:
            if output:
                print self
            if self.anns[self.turn]:
                winner = self.input(inputs=self.anns[self.turn].calculate(inputs=self.output()))
            else:
                winner = self.move(column=input('{0}\'s turn: '.format(self.turn and 'X' or 'O')))
        if output:
            print self
        if winner == 2:
            if output:
                print "It's a tie!"
        else:
            if output:
                print "{0} wins!".format(winner and 'X' or 'O')
        return winner

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


class Connect4Network:
    def zero_players(self, ann, i, output):
        anns = [NeuralNetwork(inputs=49, outputs=3, hidden=49, rows=5) for _ in xrange(10)]
        for j, ann_opp in enumerate(anns):
            try:
                ann_opp.genome = load(open('examples/connect4/genomes/genome{0:02d}.p'.format(j + 10*(i < 10)), 'rb'))
            except IOError:
                pass
        scores = []
        for j in xrange(100):
            scores.append(0)
            for ann_opp in anns:
                connect4 = Connect4(anns=i < 10 and [ann, ann_opp] or [ann_opp, ann])
                winner = connect4.play(output=output)
                if winner != 2:
                    scores[-1] += 2*winner - 1
        ann.mutate(increment=scores.index(max(scores))/100.0)
        dump(ann.genome, open('examples/connect4/genomes/genome{0:02d}.p'.format(i), 'wb'))

    def start(self):
        try:
            mkdir('examples/connect4/genomes')
        except OSError:
            pass
        players = input('Players: ')
        if players == 0:
            output = input('Output: ')
            anns = [NeuralNetwork(inputs=49, outputs=3, hidden=49, rows=5) for i in xrange(20)]
            for i, ann in enumerate(anns):
                try:
                    ann.genome = load(open('examples/connect4/genomes/genome{0:02d}.p'.format(i), 'rb'))
                except IOError:
                    pass
            for _ in xrange(input('Iterations: ')):
                for i, ann in enumerate(anns):
                    Process(target=self.zero_players, kwargs={'ann': ann, 'i': i, 'output': output}).start()
        if players == 1:
            roll = randint(0, 19)
            ann = NeuralNetwork(inputs=49, outputs=3, hidden=49, rows=5)
            try:
                ann.genome = load(open('examples/connect4/genomes/genome{0:02d}.p'.format(roll), 'rb'))
            except IOError:
                pass
            if roll < 10:
                Connect4([ann, None]).play()
            else:
                Connect4([None, ann]).play()
        if players == 2:
            Connect4().play()
