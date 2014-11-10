class Connect4(object):
    def __init__(self):
        self.pieces = [[] for i in xrange(7)]
        self.turn = 0

    def move(self, column):
        for i in xrange(column, column + 7):
            if len(self.pieces[i % 7]) < 6:
                self.pieces[i % 7].append(self.turn)
                self.turn = 1 - self.turn
                return

    def __str__(self):
        output = ''
        for i in xrange(6):
            output += i and '\n ' or ' '
            for piece_column in self.pieces:
                try:
                    output += str(piece_column[5 - i]) + ' '
                except IndexError:
                    output += '  '
        return output


def start():
    pass
