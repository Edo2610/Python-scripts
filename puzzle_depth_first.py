import random
import itertools
import collections

class Node:
    """
    Classe nodo
    - 'puzzle' = Puzzle iniziale
    - 'parent' = nodo precedente generato dal Solver, se esiste
    - 'action' = azione fatta per arrivare allo stato corrente
    """
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action

    @property
    def state(self):
        """
        Ritorna rappresentazione lineare del puzzle
        """
        return str(self)

    @property
    def path(self):
        """
        Ricostruisce il percorso al nodo radice
        """
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def solved(self):
        """ Verifica se il puzzle è verificato """
        return self.puzzle.solved

    @property
    def actions(self):
        """ Accede alle azione per arrivare alla posizione corrente """
        return self.puzzle.actions

    def __str__(self):
        return str(self.puzzle)

class Solver:
    """
    Un N-puzzle solver
    - 'start' è l'istanza iniziale'
    """
    def __init__(self, start):
        self.start = start

    def solve(self):
        """
        Performa la depth first search e ritorna il
        percorso alla soluzione, se esiste
        """
        queue = collections.deque([Node(self.start)])
        seen  = set()
        seen.add(queue[0].state)
        while queue:
            node = queue.pop()
            """
            Anzichè usare il comando queue.appendleft(child) [vedi sotto] potremmo
            usare il comando node = queue.pop(0) così che prenda sempre
            il primo della lista open che è l'ultimo entrato dato che vengono
            inseriti a sinistra. L'algoritmo diverrebbe lo stesso LIFO.
            """
            if node.solved:
                return node.path
            for move, action in node.actions:
                child = Node(move(), node, action)

                if child.state not in seen:
                    #queue.appendleft(child)
                    queue.append(child)
                    seen.add(child.state)
                    """
                    Ogni volta che viene aggiugnto un child viene messo a destra e non a sinstra
                    così il comando node = queue.pop() prende l'ultimo elemento messo nella lista
                    open facendo diventare l'algoritmo da FIFO a LIFO.
                    """
class Puzzle:
    """
    Classe per l'N-puzzle'
    - board deve essere una lista 2D quadrata con elementi da 0 a N-1
    """
    def __init__(self, board):
        self.width = len(board[0])
        self.board = board

    @property
    def solved(self):
        """
        Il puzzle è risolto se la rappresentazione lineare dei suoi
        elementi è in ordine crescente da sinistra a destra e lo '0'
        è in ultima posizione
        """
        N = self.width * self.width
        return str(self) == ''.join(map(str, range(1,N))) + '0'

    @property
    def actions(self):
        """
        ritorna la lista di coppi 'move' e 'action'
        'move' può essere chiamata per ritornare un nuovo puzzle in cui
        lo '0' viene spostato nella direzione di 'action
        """
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            direcs = {'R':(i, j-1),
                      'L':(i, j+1),
                      'D':(i-1, j),
                      'U':(i+1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and self.board[r][c] == 0:
                    move = create_move((i,j), (r,c)), action
                    moves.append(move)
        return moves

    def shuffle(self):
        """
        Ritorna un nuovo puzzle con 1000 mosse random
        """
        puzzle = self
        for _ in range(1000):
            puzzle = random.choice(puzzle.actions)[0]()
        return puzzle

    def copy(self):
        """
        Ritorna un nuovo puzzle uguale a 'self'
        """
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def _move(self, at, to):
        """
        Ritorna un nuovo puzzle dove 'at' e 'to' vengonos cambiati di posto
        """
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def pprint(self):
        for row in self.board:
            print(row)
        print()

    def __str__(self):
        return ''.join(map(str, self))
    
    def __iter__(self):
        for row in self.board:
            yield from row

if __name__ == '__main__':
    # example of use
    n = int(input("Please enter dimension of puzzle: "))
    
    board = [[j*n+i for i in range(n)] for j in range(n)]
    n = 0
    
    puzzle = Puzzle(board)
    print("Your puzzle dimension\n")
    puzzle.pprint()
    puzzle = puzzle.shuffle()
    print("Your puzzle start point\n")
    puzzle.pprint()
    
    s = Solver(puzzle)
    p = s.solve()   
    
    for node in p:
        n += 1
        print(node.action, end = " - "),
    print("\nSolved in {:d} moves\n".format(n))
    node.puzzle.pprint()
