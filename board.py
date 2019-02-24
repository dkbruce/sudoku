import unittest

class Board:
    def __init__(self, path):
        with open(path, 'r') as fileread:
            newboard = fileread.read().split('\n')
        
        header = newboard[0].split(' ')
        boxrows = int(header[0])
        boxcols = int(header[1])
        boardrows = int(header[2])
        boardcols = int(header[3])
        self.boxrows = boxrows
        self.boxcols = boxcols
        self.boardrows = boardrows
        self.boardcols = boardcols
        
        rows = [list(map(int, row.split())) for row in newboard[1:]]
        cols = list(map(list, zip(*rows)))
        
        self.rows = rows
        self.cols = cols
    
    def rows_valid(self):
        for row in self.rows:
            if len(row) != len(set(row)):
                return False
        return True

    def cols_valid(self):
        for col in self.cols:
            if len(col) != len(set(col)):
                return False
        return True

    def entries_valid(self):
        num_range = range(1, self.boxrows * self.boxcols + 1)
        for row in self.rows:
            if any(num not in num_range for num in row):
                return False
        return True
            

class TestBoard(unittest.TestCase):
    def test_valid(self):
        new_board = Board('tests/success.test')
        self.assertEqual(new_board.rows_valid(), True)
        self.assertEqual(new_board.cols_valid(), True)
        self.assertEqual(new_board.entries_valid(), True)


if __name__ == '__main__':
    unittest.main()