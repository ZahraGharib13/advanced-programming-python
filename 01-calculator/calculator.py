import tkinter as tk
class calculator:

    def __init__(self):
        self.result_label = None

    def addition(self, event):
        try:
            self.num1 = self.first_num_entry.get()
            self.num2 = self.second_num_entry.get()
            self.result = float(self.num1) + float(self.num2)
            self.result_label.config(text=f'the operation result is: {self.result}')
        except ValueError:
            self.result_label.config(text='enter a number')


    def minus(self, event):
        try:
            self.num1 = self.first_num_entry.get()
            self.num2 = self.second_num_entry.get()
            self.result = float(self.num1) - float(self.num2)
            self.result_label.config(text=f'the operation result is: {self.result}')
        except ValueError:
            self.result_label.config(text='enter a number')


    def multiply(self, event):
        try:
            self.num1 = self.first_num_entry.get()
            self.num2 = self.second_num_entry.get()
            self.result = float(self.num1) * float(self.num2)
            self.result_label.config(text=f'the operation result is: {self.result}')
        except ValueError:
            self.result_label.config(text='enter a number')
        

    def division(self, event):
        try:
            self.num1 = self.first_num_entry.get()
            self.num2 = self.second_num_entry.get()
            self.result = float(self.num1) / float(self.num2)
            self.result_label.config(text=f'the operation resutl is: {self.result}')
        except ZeroDivisionError:
            self.result_label.config(text='cannot be divivded by zero')
        except ValueError:
            self.result_label.config(text='enter a number')

    def reset(self, event):
        self.first_num_entry.delete(0, tk.END)    # clear the contents of a text entry widget-gets the range of chars to delete
        self.second_num_entry.delete(0, tk.END)   # tk.end makes sure all the chars in the entry will be cleared
        self.result_label.config(text='operation result will appear here')


    def create_GUI(self):
        root = tk.Tk()
        root.title('calculator')
        self.first_num_label = tk.Label(root, text='Enter the first number: ')
        self.first_num_label.grid(row=0, column=0, sticky="W")

        self.first_num_entry = tk.Entry(root)
        self.first_num_entry.grid(row=0, column=1, padx=50)

        self.second_num_label = tk.Label(root, text='Enter the second number: ')
        self.second_num_label.grid(row=1, column=0, sticky="W")

        self.second_num_entry = tk.Entry(root)
        self.second_num_entry.grid(row=1, column=1, padx=50)

        frame = tk.Frame(root)
        frame.grid(row=2, columnspan=4, pady= 20)

        add_button = tk.Button(frame, text='+')
        add_button.grid(row=0, column=0, padx=5)
        add_button.bind('<Button>', func=self.addition)

        minus_button = tk.Button(frame, text='-')
        minus_button.grid(row=0, column=1, padx=5)
        minus_button.bind('<Button>', func=self.minus)

        multiply_button = tk.Button(frame, text='*')
        multiply_button.grid(row=0, column=2, padx=5)
        multiply_button.bind('<Button>', func=self.multiply)

        division_button = tk.Button(frame, text='/')
        division_button.grid(row=0, column=3, padx=5)
        division_button.bind('<Button>', func=self.division)

        reset_button = tk.Button(root, text='click to reset')
        reset_button.grid(row=4, columnspan=4, pady=20)
        reset_button.bind('<Button>', func=self.reset)

        self.result_label = tk.Label(root, text='operation result will appear here')
        self.result_label.grid(row=3, columnspan=4, pady=20)
        root.mainloop()

o1 = calculator()
o1.create_GUI()