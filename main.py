import sys
from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

import solver

MARGIN = 20  # Pixels around the board
SIDE = 30  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board
MAX_SIZE = 15

class NonoUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent , size_matrix = 5):

        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1
        self.row_temp, self.col_temp = -1, -1
        self.size_matrix = size_matrix
        self.border_top_size = 3
        self.border_left_size = 3

        self.border_top = [[0 for i in range(self.border_top_size)] for _ in range(self.size_matrix)]

        self.border_left = [[0 for i in range(self.border_left_size)] for _ in range(self.size_matrix)]

        self.obj2 = solver.Solver()

        self.__initUI()

        self.insert_pos = -1

    def __initUI(self):

        self.parent.title("Nonogram GUI Solver - Ferran Celades")
        self.grid(row=1, column=1, sticky='nsew')
        self.grid_propagate(1)

        self.canvas = Canvas(self,
        width=self.size_matrix*SIDE+self.border_left_size*SIDE, height=self.size_matrix*SIDE+self.border_top_size*SIDE, bg='white', highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='nsew',padx=20, pady=20)
        self.canvas.grid_propagate(1)

        clear_button = Button(self,
                              text="RESET MAP",
                              command=self.__reset_map)
        clear_button.grid(row=2, column=1, sticky='nsew')
        clear_button.grid_propagate(1)

        add_row = Button(self,
                              text="ADD ROW",
                              command=self.__add_row)
        add_row.grid(row=0, column=1, sticky='n')
        add_row.grid_propagate(1)

        add_col = Button(self,
                              text="ADD COL",
                              command=self.__add_col)
        add_col.grid(row=1, column=0, sticky='w')
        add_col.grid_propagate(1)

        solve = Button(self,
                              text="SOLVE",
                              command=self.__solve)
        solve.grid(row=2, column=0, sticky='we')
        solve.grid_propagate(1)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)
        self.canvas.bind('<Left>', self.__leftKey)
        self.canvas.bind('<Right>', self.__rightKey)
        self.canvas.bind('<Up>', self.__upKey)
        self.canvas.bind('<Down>', self.__downKey)


    def __update_canvas(self):
        self.canvas.delete("all")
        self.canvas.config(width=self.size_matrix*SIDE+self.border_left_size*SIDE, height=self.size_matrix*SIDE+self.border_top_size*SIDE)
        self.__draw_grid()
        self.__draw_puzzle()
        self.__draw_cursor()

    def __update_numbers(self):
        self.canvas.delete("number")
        self.__draw_puzzle()

    def __add_row(self):
        self.border_top_size += 1
        for r in range(self.size_matrix):
            self.border_top[r].append(0)
        self.__update_canvas()

    def __add_col(self):
        self.border_left_size += 1
        for c in range(self.size_matrix):
            self.border_left[c].append(0)
        self.__update_canvas()

    def __draw_grid(self):

        """
        Draws grid
        """

        for i in range(self.size_matrix + 1):
            actual_x = i * SIDE + self.border_left_size * SIDE
            actual_y = i * SIDE + self.border_top_size * SIDE

            width_line = 5.0 if i == 0 or i == self.size_matrix else 2.0
            self.canvas.create_line(
            0, actual_y, self.size_matrix*SIDE+self.border_left_size * SIDE, actual_y, width=width_line, tags="cleanmap")
            self.canvas.create_line(
            actual_x, 0, actual_x, self.size_matrix*SIDE+self.border_top_size * SIDE , width=width_line, tags="cleanmap")

        for i in range(self.border_top_size):
            x0 = self.border_left_size * SIDE
            y0 = i*SIDE
            x1 = self.size_matrix * SIDE + self.border_left_size * SIDE
            y1 = i*SIDE
            width_line = 5.0 if i is 0 else 2.0
            self.canvas.create_line(x0,y0,x1,y1, width=width_line, tags="cleanmap")

        for i in range(self.border_left_size):
            x0 = i*SIDE
            y0 = self.border_top_size * SIDE
            x1 = i*SIDE
            y1 = self.size_matrix * SIDE + self.border_top_size * SIDE

            width_line = 5.0 if i is 0 else 2.0
            self.canvas.create_line(x0,y0,x1,y1, width=width_line, tags="cleanmap")

    def __draw_puzzle(self):

        text_font = ("Times",SIDE-4,"bold")

        x0 = (SIDE // 2)
        y0 = SIDE // 2
        self.canvas.create_text(x0,y0, fill="black", font = text_font, text=str(self.size_matrix))

        for top in range(self.size_matrix):
            for number in range(len(self.border_top[top])):
                x0 = self.border_left_size * SIDE + SIDE // 2 + SIDE * top
                y0 = self.border_top_size * SIDE - SIDE // 2 - SIDE * number
                text = self.border_top[top][number]
                if text is not 0:
                    self.canvas.create_text(x0,y0, fill="black", font = text_font, text=text, tags="number")

        for left in range(self.size_matrix):
            for number in range(len(self.border_left[left])):
                x0 = self.border_left_size * SIDE - SIDE // 2 - SIDE * number
                y0 = self.border_top_size * SIDE + SIDE // 2 + SIDE * left
                text = self.border_left[left][number]
                if text is not 0:
                    self.canvas.create_text(x0,y0, fill="black", font = text_font, text=text, tags="number")

    def __reset_map(self):

        self.border_top_size = 3
        self.border_left_size = 3
        self.border_top = [[0 for i in range(self.border_top_size)] for _ in range(self.size_matrix)]
        self.border_left = [[0 for i in range(self.border_left_size)] for _ in range(self.size_matrix)]
        self.__update_canvas()

    def __cell_clicked(self,event):

        x, y = event.x, event.y
        col = x // SIDE
        row = y // SIDE
        if col in range(self.border_left_size,self.size_matrix+self.border_left_size) and row in range(self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col in range(self.border_left_size) and row in range(self.border_top_size,self.size_matrix+self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col is 0 and row is 0:
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()

        self.row_temp = -1
        self.col_temp = -1

    def __draw_cursor(self):

        self.canvas.delete("cursor")
        x0 = SIDE * self.col + 1
        y0 = SIDE * self.row + 1
        x1 = SIDE * self.col + SIDE - 1
        y1 = SIDE * self.row + SIDE - 1
        self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor", width=2
            )

    def __leftKey(self,event):

        col = self.col-1
        row = self.row
        if col in range(self.border_left_size,self.size_matrix+self.border_left_size) and row in range(self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col in range(self.border_left_size) and row in range(self.border_top_size,self.size_matrix+self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col is 0 and row is 0:
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()

        self.row_temp = -1
        self.col_temp = -1

    def __rightKey(self,event):

        col = self.col+1
        row = self.row
        if col in range(self.border_left_size,self.size_matrix+self.border_left_size) and row in range(self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col in range(self.border_left_size) and row in range(self.border_top_size,self.size_matrix+self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col is 0 and row is 0:
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()

        self.row_temp = -1
        self.col_temp = -1

    def __upKey(self,event):

        col = self.col
        row = self.row-1
        if col in range(self.border_left_size,self.size_matrix+self.border_left_size) and row in range(self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col in range(self.border_left_size) and row in range(self.border_top_size,self.size_matrix+self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col is 0 and row is 0:
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()

        self.row_temp = -1
        self.col_temp = -1

    def __downKey(self,event):

        col = self.col
        row = self.row+1
        if col in range(self.border_left_size,self.size_matrix+self.border_left_size) and row in range(self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col in range(self.border_left_size) and row in range(self.border_top_size,self.size_matrix+self.border_top_size):
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()
        if col is 0 and row is 0:
            self.canvas.focus_set()
            self.row = row
            self.col = col
            self.__draw_cursor()

        self.row_temp = -1
        self.col_temp = -1

    def __key_pressed(self,event):

        if event.char in "1234567890":
            self.__safe_number(int(event.char))


    def __change_mat_size(self,number):

        if self.row_temp != self.row or self.col_temp != self.col:
            self.size_matrix = number
            self.__reset_map()
            self.row_temp = self.row
            self.col_temp = self.col
        else:
            tot_number = int(str(self.size_matrix) + str(number))
            if tot_number <= MAX_SIZE:
                self.size_matrix = tot_number
                self.__reset_map()


    def __insert_top(self,number):

        text_font = ("Times",SIDE-4,"bold")

        row = self.row * SIDE + SIDE // 2
        col = self.col * SIDE + SIDE // 2

        list_x = self.col - self.border_left_size
        list_y = self.border_top_size - self.row - 1

        if self.row_temp != self.row or self.col_temp != self.col:
            if self.border_top[list_x][list_y] is not 0:
                self.border_top[list_x][list_y] = number
                self.__update_numbers()
            else:
                self.border_top[list_x][list_y] = number
                self.canvas.create_text(col, row, font = text_font, text=number, tags="number")
            self.row_temp = self.row
            self.col_temp = self.col
        else:
            tot_number = int(str(self.border_top[list_x][list_y]) + str(number))
            if tot_number <= self.size_matrix:
                self.border_top[list_x][list_y] = tot_number
                self.__update_numbers()


    def __insert_left(self,number):

        text_font = ("Times",SIDE-4,"bold")

        row = self.row * SIDE + SIDE // 2
        col = self.col * SIDE + SIDE // 2

        list_x = self.border_left_size - self.col - 1
        list_y = self.row  - self.border_top_size

        if self.row_temp != self.row or self.col_temp != self.col:
            if self.border_left[list_y][list_x] is not 0:
                self.border_left[list_y][list_x] = number
                self.__update_numbers()
            else:
                self.border_left[list_y][list_x] = number
                self.canvas.create_text(col, row, font = text_font, text=number, tags="number")
            self.row_temp = self.row
            self.col_temp = self.col
        else:
            tot_number = int(str(self.border_left[list_y][list_x]) + str(number))
            if tot_number <= self.size_matrix:
                self.border_left[list_y][list_x] = tot_number
                self.__update_numbers()


    def __safe_number(self,number):

        if self.col is 0 and self.row is 0:

            self.__change_mat_size(number)

        elif number <= self.size_matrix:
            if self.col in range(self.border_left_size,self.size_matrix+self.border_left_size) and self.row in range(self.border_top_size):

                self.__insert_top(number)

            else:

                self.__insert_left(number)

    def __solve(self):

        top_border = zip(*self.border_top)
        top_border = top_border[::-1]

        left_border = []
        for left_line in self.border_left:
            left_border.append(left_line[::-1])

        self.__draw_solution(self.obj2.solve(top_border,left_border))

    def __draw_solution(self,mat):

        for line in range(self.size_matrix):
            for char in range(self.size_matrix):
                if mat[line][char] is 'x':
                    x0 = self.border_left_size * SIDE + char * SIDE
                    y0 = self.border_top_size * SIDE + line * SIDE
                    x1 = self.border_left_size * SIDE + char * SIDE + SIDE
                    y1 = self.border_top_size * SIDE + line * SIDE + SIDE
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill="black")


if __name__ == '__main__':
    root = Tk()
    NonoUI(root)
    root.mainloop()
