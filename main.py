from tkinter import Frame, Button, Tk, Canvas, messagebox
from tkinter.filedialog import askopenfilename
from board import Board
import os

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Sudoku')
        self.pack()
        self.margin = 25
        self.filename = ''
        self.row, self.col = -1, -1
        self.w = Canvas(master, width = 875, height = 875)
        self.create_widgets()
        self.w.bind('<Button-1>', self.click)
        self.w.bind('<Key>', self.key)

    def create_widgets(self):
        self.button_create = Button(self)
        self.button_create["text"] = "Create game"
        self.button_create["command"] = self.create_game
        self.button_create.pack(side="top")

    def create_game(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.join(dir_path, 'boards')
        self.filename = askopenfilename(initialdir = dir_path, 
                                        title = 'Select game')
        self.game = Board(self.filename)
        self.gameUI()
        self.button_create.destroy()
        self.populate_game()

    def gameUI(self):
        self.w.pack(side = 'top')
        self.side = 800 / self.game.numcols
        for i in range(self.game.numcols + 1):
            color = "blue" if i % self.game.boxcols == 0 else "black"
            x0 = self.margin + i*self.side
            y0 = self.margin
            x1 = self.margin + i*self.side
            y1 = 825
            if i % self.game.boxcols == 0:
                self.w.create_line(x0, y0, x1, y1, fill = color, width = 3)
            else:
                self.w.create_line(x0, y0, x1, y1, fill = color)

        for i in range(self.game.numrows + 1):
            color = "blue" if i % self.game.boxrows == 0 else "black"
            y0 = self.margin + i*self.side
            x0 = self.margin
            y1 = self.margin + i*self.side
            x1 = 825
            if i % self.game.boxrows == 0:
                self.w.create_line(x0, y0, x1, y1, fill = color, width = 3)
            else:
                self.w.create_line(x0, y0, x1, y1, fill = color)

    def populate_game(self):
        self.w.delete("numbers")
        for i in range(self.game.numrows):
            for j in range(self.game.numcols):
                answer = self.game.rows[i][j]
                if answer != 0:
                    x = self.margin + j * self.side + self.side / 2
                    y = self.margin + i * self.side + self.side / 2
                    original = self.game.startrows[i][j]
                    color = "black" if answer == original else "sea green"
                    self.w.create_text(x, y, text=answer, tags="numbers",
                                       fill=color, font = ('Montserrat', 18))

    def click(self, event):
        x, y = event.x, event.y
        if (self.margin < x < 875 - self.margin) and (self.margin < y < 875 - self.margin):
            self.w.focus_set()
            row, col = int((y - self.margin) / self.side), int((x - self.margin) / self.side)
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            else:
                self.row, self.col = row, col
        self.box()

    def box(self):
        self.w.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = self.margin + self.col * self.side + 1
            y0 = self.margin + self.row * self.side + 1
            x1 = self.margin + (self.col + 1) * self.side - 1
            y1 = self.margin + (self.row + 1) * self.side - 1
            self.w.create_rectangle(
                x0, y0, x1, y1,
                outline='red', tags='cursor'
            )

    def key(self, event):
        if ((self.row, self.col) != (-1, -1) and event.char in '1234567890' and
                self.game.writable(self.row, self.col)):
            self.game.insert(self.row, self.col, int(event.char))
            self.populate_game()
            self.box()
            if self.game.completed():
                messagebox.showinfo('Congrats!', 'You win!')



root = Tk()
root.geometry('875x875')
app = Application(master = root)
app.mainloop()