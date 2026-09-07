import tkinter as tk
from random import randint

class Snake:
    def __init__(self, root):
        self.root = root
        self.GUI()

    def GUI(self):
        self.canvas = tk.Canvas(self.root, bg='black', width=500, height=500)
        self.canvas.pack()
        self.root.bind('<KeyPress>', self.change_dir)
        self.direction = 'Up'
        self.cell = 20
        self.snake = [(200, 200), (200, 250+self.cell)]
        self.game_on = True
        self.food = self.place_food()
        self.move()

    def change_dir(self, event):
        if event.keysym in ['Up', 'Down', 'Right', 'Left']:
            self.direction = event.keysym


    def move(self):
        if self.game_on:
            head_x, head_y = self.snake[0]
            if self.direction == 'Up':
                new_head = (head_x, head_y-self.cell)
            elif self.direction == 'Down':
                new_head = (head_x, head_y+self.cell)
            elif self.direction == 'Right':
                new_head = (head_x+self.cell, head_y)
            elif self.direction == 'Left':
                new_head = (head_x-self.cell, head_y)
            
            if not self.game_over(new_head):
                self.snake.insert(0, new_head)
                if new_head[0] == self.food[0] and new_head[1] == self.food[1]:
                    self.food = self.place_food()
                else:
                    self.snake.pop()
                self.draw()
                self.root.after(300, self.move)
            else:
                self.canvas.create_text(250, 250, fill='white', text='Game Over')
                self.game_on = False

    def game_over(self, new_head):
        if new_head[0] >= 500 or new_head[1] >= 500 or new_head[0]<0 or new_head[1] < 0:
            return True
        if new_head in self.snake:
            return True
        return False

    def place_food(self):
        self.food_x = randint(0, 500//self.cell-1)*self.cell
        self.food_y = randint(0, 500//self.cell-1)*self.cell
        if (self.food_x, self.food_y) in self.snake:
            self.place_food()
        return (self.food_x, self.food_y)
            


    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.snake[0][0], self.snake[0][1], self.snake[0][0]+self.cell, self.snake[0][1]+self.cell, fill='purple')
        for crdnt in self.snake[1:]:
            self.canvas.create_rectangle(crdnt[0], crdnt[1], crdnt[0]+self.cell, crdnt[1]+self.cell, fill='green')
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0]+self.cell, self.food[1]+self.cell, fill='red')

root = tk.Tk()
snake = Snake(root)
root.mainloop()