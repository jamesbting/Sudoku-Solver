# import statements
import tkinter as tk
from SudokuSolver import SudokuBoard
from StopWatch import StopWatch
import copy


class GUI:

    # constructor
    def __init__(self, master):

        # dictionary to store the cells
        self.cells = {}

        # set the window settings
        self.window = master
        self.window.title("Sudoku")
        self.window.resizable(0, 0)

        # the unsolved game the player will be presented with
        self.board = SudokuBoard()
        self.board.generate_new_board()
        self.grid = self.board.grid

        # create a solution
        self.solution = copy.deepcopy(self.board)
        self.solution.solve()

        # calls a helper method to display the board
        self.make_grid(master)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Key>", self.canvas_key)
        self.current = None

        # calls a helper method to initialize all the attributes and display the buttons on the side
        self.button_frame = tk.Frame(master)
        self.new_button = tk.Button(self.button_frame, height=2, width=10, text='New Game', command=self.new_game)
        self.label = tk.Label(self.button_frame, text="Options", font=("helvetica", 30))
        self.solveButton = tk.Button(self.button_frame, height=2, width=10, text="Solve",
                                     command=self.make_solution)
        self.quitButton = tk.Button(self.button_frame, height=2, width=10, text='Quit', command=self.window.destroy)
        self.display_buttons()

        # calls a helper method to initialize the stopwatch and all it's features
        self.sudoku_stopwatch = StopWatch(self.button_frame)
        self.stopwatch_frame = tk.Frame(master)
        self.display_stopwatch()

    # function that creates a new game
    def new_game(self):
        self.board.clear()
        self.board = SudokuBoard()
        self.board.generate_new_board()
        self.solution = copy.deepcopy(self.board)
        self.solution.solve()
        self.sync_board_and_canvas()

    # function that makes a new window for the game, and returns the window
    def make_window(self, title):
        window = tk.Toplevel()
        window.title(title)
        window.attributes('-topmost', True)
        window.grab_set()
        window.focus_force()
        return window

    # function that creates a grid for the game and a canvas to display the grid
    def make_grid(self, master):
        self.c = tk.Canvas(master, width='512', height='512')
        self.c.grid(row=0, column=0)

        self.rects = [[None for x in range(9)] for y in range(9)]
        self.handles = [[None for x in range(9)] for y in range(9)]
        rsize = 512 / 9
        guidesize = 512 / 3

        for y in range(9):
            for x in range(9):
                (xr, yr) = (x * guidesize, y * guidesize)
                self.rects[y][x] = self.c.create_rectangle(xr, yr, xr + guidesize,
                                                           yr + guidesize, width=3)
                (xr, yr) = (x * rsize, y * rsize)
                r = self.c.create_rectangle(xr, yr, xr + rsize, yr + rsize)
                t = self.c.create_text(xr + rsize / 2, yr + rsize / 2, text="SUDO",
                                       font="System 15 bold")
                self.handles[y][x] = (r, t)

        self.canvas = self.c
        self.sync_board_and_canvas()

    # function that updates the canvas when something is input into the grid
    def sync_board_and_canvas(self):
        g = self.board.grid
        for y in range(9):
            for x in range(9):
                if g[y][x] != 0:
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text=str(g[y][x]))
                else:
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text='')

    #function that updates the board and displays the solution
    def sync_solution_board_and_canvas(self):
        g = self.solution.grid # this is the only line that differs from the previous one
        for y in range(9):
            for x in range(9):
                if g[y][x] != 0:
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text=str(g[y][x]))
                else:
                    self.canvas.itemconfig(self.handles[y][x][1],
                                           text='')

    #function that, when the canvas is clicked, determines where the click occured
    def canvas_click(self, event):
        print("Click! (%d,%d)" % (event.x, event.y))
        self.canvas.focus_set()
        rsize = 512 / 9
        (x, y) = (0, 0)
        if event.x > rsize:
            x = int(event.x / rsize)
        if event.y > rsize:
            y = int(event.y / rsize)
        print(x, y)
        if self.current:
            (tx, ty) = self.current
        self.current = (x, y)

    # function that determines what to do based on which key is pressed on the keyboard and calls methods to determine
    # if that input is valid
    def canvas_key(self, event):
        print("Clack! (%s)" % event.char)

        (x, y) = self.current
        if event.keysym_num == 65288:
            self.board.set(x, y, 0,delete=True)
            self.sync_board_and_canvas()
        elif event.char.isdigit() and int(event.char) > 0 and self.current:
            self.sudoku_stopwatch.start()
            try:
                self.board.set(x, y, int(event.char))
                self.sync_board_and_canvas()
            except ValueError:
                self.board.set(x, y, 0)
                self.sync_board_and_canvas()


    # function that places the buttons into their location on the side
    def display_buttons(self):
        # place everything into their appropriate positions
        self.label.grid(row=5, column=0)
        self.new_button.grid(row=6, column=0)
        self.solveButton.grid(row=7, column=0)
        self.quitButton.grid(row=8, column=0)
        self.button_frame.grid(row=0, column=1, sticky='n')

    # function that places the stop watch on the side of the board
    def display_stopwatch(self):
        self.stopwatch_frame.grid(row=1, column=0)

    # function that recreates the canvas and then displays the solution
    def make_solution(self):
        self.c = tk.Canvas(self.window, width='512', height='512')
        self.c.grid(row=0, column=0)

        self.rects = [[None for x in range(9)] for y in range(9)]
        self.handles = [[None for x in range(9)] for y in range(9)]
        rsize = 512 / 9
        guidesize = 512 / 3

        for y in range(9):
            for x in range(9):
                (xr, yr) = (x * guidesize, y * guidesize)
                self.rects[y][x] = self.c.create_rectangle(xr, yr, xr + guidesize,
                                                           yr + guidesize, width=3)
                (xr, yr) = (x * rsize, y * rsize)
                r = self.c.create_rectangle(xr, yr, xr + rsize, yr + rsize)
                t = self.c.create_text(xr + rsize / 2, yr + rsize / 2, text="SUDO",
                                       font="System 15 bold")
                self.handles[y][x] = (r, t)

        self.canvas = self.c
        self.sync_solution_board_and_canvas()

    # adds some colors to the board
    def rgb(self, red, green, blue):
        # Make a tkinter compatible RGB color.
        return "#%02x%02x%02x" % (red, green, blue)


def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()


main()
