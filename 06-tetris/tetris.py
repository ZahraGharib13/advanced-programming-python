"""
created on: March 19 2025

author: Zahra Gharib
"""

import random
import tkinter as tk

class Tetris:
    block_list = ['L', 'I', 'T', 'Z','J', 'S','O']
    color_list = ['purple', 'pink', 'blue', 
                  'green', 'yellow', 'red',
                  'aqua', 'brown']
    
    SHAPES = {
        'I': [[1], [1], [1], [1]],
        'O': [[1, 1], [1, 1]],
        'T': [[0, 1, 0], [1, 1, 1]],
        'L': [[1, 0], [1, 0], [1, 1]],
        'J': [[0, 1], [0, 1], [1, 1]],
        'S': [[0, 1, 1], [1, 1, 0]],
        'Z': [[1, 1, 0], [0, 1, 1]]
    }

    def __init__(self, root):
        self.root = root
        self.direction = 'Down'
        self.width = 20 
        self.height = 20  
        self.cell = 20        
        self.is_fast_speed = False
        self.normal_speed = 400
        self.fast_speed = 100
        self.increase = 10
        self.level = 1
        self.root.bind('<KeyPress>', self.change_dir)
        self.root.bind('<KeyRelease>', self.reset_speed)
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.current_shape = []
        self.current_color = ''
        self.x = self.width // 2
        self.y = 0
        self.game_on = True
        self.score = 0
        self.time = 120
        self.GUI()
        self.countdown()
        self.new_block()
        self.game_loop()

    def countdown(self):
        if self.time > 0 and self.game_on:
            self.time -= 1
            self.time_label.config(text=f'time: {self.time}')
            self.second = self.root.after(1000, self.countdown)
        elif self.time <= 0:
            self.time = 0
            self.draw()
    
    def increase_time(self):
        """
        after every row deletion(one score), blocks fall with faster speed
        """
        if self.normal_speed > 200:
            self.normal_speed = max(self.normal_speed - self.increase, 200)
            self.increase = min(self.increase + 10, 50)
        else:
            self.increase = 10
        


    def new_block(self):
        """
        creates another block falling on top of the remaining ones
        """
        self.current_block = random.choice(self.block_list)
        self.current_shape = self.SHAPES[self.current_block]  #list of lists
        self.current_color = random.choice(self.color_list)
        self.x = (self.width - len(self.current_shape[0])) // 2
        self.y = 0

        if self.hit(self.x, self.y):
            self.game_over()

    def hit(self, new_x, new_y, shape=None):
        """checks if the block get out of the box-shape=None for rotation"""
        shape = shape or self.current_shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = new_x + x
                    grid_y = new_y + y
                    if grid_x < 0 or grid_x >= self.width:
                        return True
                    if grid_y >= self.height:
                        return True
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return True
        return False

    def reset_speed(self, event):
        """increases the speed of falling down when pressing down"""
        if event.keysym == 'Down':
            self.is_fast_speed = False

    def rotate(self):
        if not self.game_on or self.time <= 0:
            return
        rotated = list(zip(*reversed(self.current_shape)))
        if not self.hit(self.x, self.y, rotated) and self.time > 0:
            self.current_shape = rotated
            self.draw()


    def GUI(self):
        self.frame = tk.Frame(self.root, width=self.width*self.cell)
        self.frame.grid(row=0, column=0, columnspan=self.width//self.cell)

        self.canvas = tk.Canvas(self.root, width=self.width*self.cell, height=self.height*self.cell, bg='black')
        self.canvas.grid(row=1, column=0)

        self.time_label = tk.Label(self.frame, text='time: -')
        self.time_label.grid(row=0, column=0, padx=(10, self.width//2))

        self.score_label = tk.Label(self.frame, text='score: 0')
        self.score_label.grid(row=0, column=1, padx=(self.width//2, 10))

        self.level_label = tk.Label(self.frame, text=f'level: {self.level}')
        self.level_label.grid(row=0, column=2)


    def move(self, dx):
        if not self.game_on or self.time <= 0:
            return
        if not self.hit(self.x + dx, self.y) and self.time > 0:
            self.x += dx
        self.draw()

    def check_continue(self):
        """constant moving down"""
        if not self.game_on or self.time <=0:
            return
        if not self.hit(self.x, self.y + 1) and self.time > 0:
            self.y += 1        #constant moving down
        else:
            self.occupied_cells()
            self.new_block()
        self.draw()

    def occupied_cells(self):
        """paints the grid. replaces the 0 and 1 with the color of the remaning blocks"""
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.y + y][self.x + x] = self.current_color
        self.keep_score()

    def change_dir(self, event):
        if not self.game_on:
            return
        if event.keysym == 'Left':
            self.move(-1)
        elif event.keysym == 'Right':
            self.move(1)
        elif event.keysym == 'Down':
            self.is_fast_speed = True
        elif event.keysym == 'Up':
            self.rotate()

    def game_over(self):
        self.game_on = False
        self.time_label.config(text='time: -')


    def game_loop(self):
        if self.game_on and self.time > 0:
            self.check_continue()
            if self.is_fast_speed:
                self.root.after(self.fast_speed, self.game_loop)
            else:
                self.root.after(self.normal_speed, self.game_loop)

    def draw(self):
        self.canvas.delete('all')
        # whole peices
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    self.paint(x, y, self.grid[y][x])
        #current peice
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.paint(self.x + x, self.y + y, self.current_color)
        if not self.game_on:
            self.canvas.create_text((self.width * self.cell) // 2, (self.width * self.cell) // 2, 
                                    fill='white', text='Game Over', font=('Arial', 24, 'bold'))  
        if self.time == 0:
            self.canvas.create_text((self.width * self.cell) // 2, (self.width * self.cell) // 2, 
                                    fill='white', text='Time\'s Up', font=('Arial', 24, 'bold'))           


    def paint(self, x, y, color):
        self.canvas.create_rectangle(x * self.cell, y * self.cell,(x+1) * self.cell,(y+1) * self.cell, fill=color, outline='white')

    def keep_score(self):
        """removes a completely occupied row and increases the score"""
        for row in self.grid:
            if 0 not in row:
                self.grid.remove(row)
                self.grid.insert(0, [0] * self.width)
                self.score += 1
                self.score_label.config(text=f'score: {self.score}')
                self.level += 1
                self.level_label.config(text=f'level: {self.level}')
                # self.time = 60
                self.increase_time()


root = tk.Tk()
tetris = Tetris(root)
tk.mainloop()