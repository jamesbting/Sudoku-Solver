import random


class SudokuBoard:
    # data structure to represent the board
    # constructor
    def __init__(self):
        self.clear()

    # returns a row of the board
    def get_row(self, row):
        return self.grid[row]

    # returns a column in the grid
    def get_cols(self, col):
        return [y[col] for y in self.grid]

    def get_nearest_region(self, col, row):
        # Regions are the 3 x 3 sub boxes
        return [y[self.make_index(col):self.make_index(col) + 3]
                for y in self.grid[self.make_index(row):self.make_index(row) + 3]]

    # helper function that returns the indices of the 3 x 3 square it is located in
    def make_index(self, v):
        if v <= 2:
            return 0
        elif v <= 5:
            return 3
        else:
            return 6

    # function that takes as input a 2D array, and prints it out with some lines to denote the different squares
    def print_board(self):
        for i in range(len(self.grid)):
            if i % 3 == 0 and i != 0:
                print("-------------------")
            for j in range(len(self.grid[0])):
                if j % 3 == 0 and j != 0:
                    print("|", end="")

                print(self.grid[i][j]) if j == 8 else print(self.grid[i][j], end=" ")

        return

    # function that finds a zero entry in the sudoku board, which represents an empty square
    def find_empty(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 0:
                    return i, j  # returns in the form of row,column

        # if no blank squares, return None
        return None

    # check if the current board is valid
    def is_valid(self, number, position):
        # check row
        for i in range(len(self.grid[0])):
            if (self.grid[position[0]][i]) == number and position[1] != i:
                return False
        # check column
        for i in range(len(self.grid)):
            if (self.grid[i][position[1]]) == number and position[0] != i:
                return False
        # check the 3x3 box
        # determine which box we are in
        box_x = position[1] // 3
        box_y = position[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.grid[i][j] == number and (i, j) != position:
                    return False
        # its a valid position
        return True

    def put(self, value, position):
        self.grid[position[0]][position[1]] = value

    # recursive solution to solve the board
    def solve(self):
        # base case: our board is full - there are no zeros and we have reached the end of the board
        find = self.find_empty()
        if not find:
            return True

        else:
            row, col = find

        # test numbers from 1 to 9
        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.grid[row][col] = i
                # see if it gives a valid solution
                if self.solve():  # recursive step
                    return True
                # set it to zero and start over
                self.grid[row][col] = 0
        return False

    def clear(self):
        # Empty the board
        self.grid = [[0 for x in range(9)] for y in range(9)]
        self.locked = []

    def generate_new_board(self):
        # Algorithm: Add a random number between 1-9 to each sub square in the board,
        # do not add duplicate random numbers.
        self.clear()
        r_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Generate all values from 1 to 9
        random.shuffle(r_vals)  # Shuffle those values, so they will appear in random order
        for y in range(0, 9, 3):
            for x in range(0, 9, 3):
                if not r_vals:
                    return
                i = r_vals.pop()  # Gets (and removes) one value from list
                try:
                    self.set(random.randint(x, x + 2), random.randint(y, y + 2), i, lock=True)
                except ValueError:
                    print("Board rule violation, this shouldn't happen!")

    # method to place numbers into the board
    def set(self, col, row, v, lock=False, delete=False):
        # check if a number is to be deleted
        if delete and not ((col, row) in self.locked):
            self.grid[row][col] = 0
            return
        # check if the number already exists in the slot that is selected
        elif v == self.grid[row][col] or (col, row) in self.locked:
            return
        # check if that digit exsists in the row already
        for v2 in self.get_row(row):
            if v == v2 and v != 0:
                raise ValueError()
        # check if that digit exists in the column alread
        for v2 in self.get_cols(col):
            if v == v2 and v != 0:
                raise ValueError()
        # check if that digit exists in the region(the 3 x 3 square) already
        for y in self.get_nearest_region(col, row):
            for x in y:
                if v == x and v != 0:
                    raise ValueError()

        # entry is valid! so place it into the grid
        self.grid[row][col] = v
        if lock:
            self.locked.append((col, row))
