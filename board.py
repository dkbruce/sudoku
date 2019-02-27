import unittest

class Board(object):
    def __init__(self, path):
        try:
            with open(path, 'r') as fileread:
                newboard = fileread.read().split('\n')

            header = newboard[0].split(' ')
            boxrows = int(header[0])
            boxcols = int(header[1])
            boardrows = int(header[2])
            boardcols = int(header[3])
            numrows = boxrows * boardrows
            numcols = boxcols * boardcols

            self.boxrows = boxrows
            self.boxcols = boxcols
            self.boardrows = boardrows
            self.boardcols = boardcols
            self.numrows = numrows
            self.numcols = numcols
            
            rows = [list(map(int, row.split())) for row in newboard[1:]]
            cols = list(map(list, zip(*rows)))
            boxes = []
            for i in range(0, numrows, boxrows):
                for j in range(0, numcols, boxcols):
                    these_rows = rows[i : i+boxrows]
                    temp = []
                    for row in these_rows:
                        for num in row[j : j+boxcols]:
                            temp.append(num)
                    boxes.append(temp)
            
            self.rows = rows
            self.cols = cols
            self.boxes = boxes
            self.startrows = [list(map(int, row.split())) for row in newboard[1:]]
        except FileNotFoundError:
            print('Invalid filepath')
        
    def rows_valid(self):
        for row in self.rows:
            filtered = [x for x in row if x != 0]
            if len(filtered) != len(set(filtered)):
                return False
        return True

    def cols_valid(self):
        for col in self.cols:
            filtered = [x for x in col if x != 0]
            if len(filtered) != len(set(filtered)):
                return False
        return True

    def boxes_valid(self):
        for box in self.boxes:
            filtered = [x for x in box if x != 0]
            if len(filtered) != len(set(filtered)):
                return False
        return True

    def entries_valid(self):
        num_range = range(self.boxrows * self.boxcols + 1)
        for row in self.rows:
            if any(num not in num_range for num in row):
                return False
        return True

    def no_blanks(self):
        for row in self.rows:
            if any([x == 0 for x in row]):
                return False
        return True

    def completed(self):
        if(self.rows_valid() and self.cols_valid and self.boxes_valid()
           and self.entries_valid() and self.no_blanks()):
            return True
        return False

    def get_box(self, row, col):
        box_row = row // self.boxrows
        box_col = col // self.boxcols
        box_num = box_row * self.boardcols + box_col
        box_index = ((row % self.boxrows) * self.boxcols 
                    + (col % self.boxcols))
        return (box_num, box_index)


    def update(self, row, col, num):
        self.rows[row][col] = num
        self.cols[col][row] = num
        box_num, box_col = self.get_box(row, col)
        self.boxes[box_num][box_col] = num

    def insert(self, row, col, num):
        if self.writable(row, col):
            self.update(row, col, num)

    def writable(self, row, col):
        if self.startrows[row][col] == 0:
            return True
        return False
            

class TestBoard(unittest.TestCase):
    def test_valid(self):
        new_board = Board('tests/success.test')
        self.assertEqual(new_board.rows_valid(), True)
        self.assertEqual(new_board.cols_valid(), True)
        self.assertEqual(new_board.boxes_valid(), True)
        self.assertEqual(new_board.entries_valid(), True)
        self.assertEqual(new_board.no_blanks(), True)
        self.assertEqual(new_board.completed(), True)

    def test_invalid(self):
        new_board = Board('tests/fail.test')
        self.assertEqual(new_board.rows_valid(), False)
        self.assertEqual(new_board.cols_valid(), False)
        self.assertEqual(new_board.boxes_valid(), False)
        self.assertEqual(new_board.entries_valid(), False)
        self.assertEqual(new_board.no_blanks(), True)
        self.assertEqual(new_board.completed(), False)

    def test_oblong(self):
        new_board = Board('tests/oblong.test')
        self.assertEqual(new_board.rows_valid(), True)
        self.assertEqual(new_board.cols_valid(), True)
        self.assertEqual(new_board.boxes_valid(), True)
        self.assertEqual(new_board.entries_valid(), True)
        self.assertEqual(new_board.no_blanks(), True)
        self.assertEqual(new_board.completed(), True)

    def test_starter(self):
        new_board = Board('tests/start.test')
        self.assertEqual(new_board.rows_valid(), True)
        self.assertEqual(new_board.cols_valid(), True)
        self.assertEqual(new_board.boxes_valid(), True)
        self.assertEqual(new_board.entries_valid(), True)
        self.assertEqual(new_board.no_blanks(), False)
        self.assertEqual(new_board.completed(), False)

    def test_insert(self):
        new_board = Board('tests/start.test')
        self.assertEqual(new_board.rows, [[1, 0, 3, 0], [0, 4, 1, 2],
                                          [2, 1, 0, 0], [0, 0, 2, 0]])
        self.assertEqual(new_board.cols, [[1, 0, 2, 0], [0, 4, 1, 0],
                                          [3, 1, 0, 2], [0, 2, 0, 0]])
        self.assertEqual(new_board.boxes, [[1, 0, 0, 4], [3, 0, 1, 2],
                                           [2, 1, 0, 0], [0, 0, 2, 0]])
        new_board.insert(0, 1, 2)
        self.assertEqual(new_board.rows, [[1, 2, 3, 0], [0, 4, 1, 2],
                                          [2, 1, 0, 0], [0, 0, 2, 0]])
        self.assertEqual(new_board.cols, [[1, 0, 2, 0], [2, 4, 1, 0],
                                          [3, 1, 0, 2], [0, 2, 0, 0]])
        self.assertEqual(new_board.boxes, [[1, 2, 0, 4], [3, 0, 1, 2],
                                           [2, 1, 0, 0], [0, 0, 2, 0]])
        new_board.insert(0, 2, 2)
        self.assertEqual(new_board.rows, [[1, 2, 3, 0], [0, 4, 1, 2],
                                          [2, 1, 0, 0], [0, 0, 2, 0]])
        self.assertEqual(new_board.cols, [[1, 0, 2, 0], [2, 4, 1, 0],
                                          [3, 1, 0, 2], [0, 2, 0, 0]])
        self.assertEqual(new_board.boxes, [[1, 2, 0, 4], [3, 0, 1, 2],
                                           [2, 1, 0, 0], [0, 0, 2, 0]])

    def test_big(self):
        new_board = Board('tests/big.test')
        self.assertEqual(new_board.rows_valid(), True)
        self.assertEqual(new_board.cols_valid(), True)
        self.assertEqual(new_board.boxes_valid(), True)
        self.assertEqual(new_board.entries_valid(), True)
        self.assertEqual(new_board.boxes, [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],])


if __name__ == '__main__':
    unittest.main()