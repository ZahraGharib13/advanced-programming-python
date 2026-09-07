import tkinter as tk
from random import choice

# class ColorGame:        
#     colors = ['green', 'blue', 'brown', 
#                   'pink', 'orange',
#                   'purple', 'black', 'red']

#     def __init__(self):
#         self.score = 0
#         self.timer = 60
#         self.name_color = choice(ColorGame.colors)
#         self.fg_color = choice(ColorGame.colors)
    
#     def start(self, event):
#         if self.timer == 60:
#             self.color_label.config(text=self.name_color, fg=self.fg_color)
#             self.countdodwn()


#     def entered_word(self, event):
#         if self.timer > 0:
#             if self.color_entry.get().lower() == self.fg_color.lower():
#                 self.score += 1
#                 self.score_label.config(text='score: '+str(self.score))
#             self.color_entry.delete(0, tk.END)
#             self.name_color = choice(ColorGame.colors)
#             self.fg_color = choice(ColorGame.colors)
#             self.color_label.config(text=self.name_color, fg=self.fg_color)


#     def reset(self, event):
#         self.color_entry.delete(0, tk.END)
#         self.color_label.config(text='Tap start to see', fg='black')
#         self.score = 0
#         self.score_label.config(text='score: -')
#         self.color_entry.delete(0, tk.END)
#         self.time_label.after_cancel(self.repeat)
#         self.timer = 60
#         self.time_label.config(text='time: -')


#     def countdodwn(self):
#         if self.timer > 0:
#             self.timer -= 1
#             self.time_label.config(text= f'time: {str(self.timer)}')
#             self.repeat = self.time_label.after(1000, self.countdodwn)
#             if self.timer == -1:
#                 self.time_label.config(text='time\'s up!!')


#     def CreateGUI(self):
#         root = tk.Tk()
#         root.title('Color Game')

#         self.time_label = tk.Label(root, text='time: -')
#         self.time_label.grid(row=0, column=1, columnspan=6)

#         self.score_label = tk.Label(root, text='score: -')
#         self.score_label.grid(row=1, column=1, columnspan=6)

#         self.color_label = tk.Label(root, text='Tap start to see')
#         self.color_label.grid(row=2, column=1, columnspan=6)

#         self.color_entry = tk.Entry(root)
#         self.color_entry.grid(row=3, column=1, columnspan=6)
#         self.color_entry.bind('<Return>', self.entered_word)

#         frame = tk.Frame()
#         frame.grid(row=4, column=1, columnspan=6, pady=30, padx=10)

#         reset_button = tk.Button(frame, text='Start', bg='pink')
#         reset_button.grid(row=4, column=1, ipadx=62., ipady=5)
#         reset_button.bind('<Button>', func=self.start)

#         start_button = tk.Button(frame, text='Reset', bg= 'pink')
#         start_button.grid(row=5, column=1, ipadx=60, ipady=5)
#         start_button.bind('<Button>', func=self.reset)

#         tk.mainloop()

        
# a = ColorGame().CreateGUI()




class ColorGame:
    colors = ['green', 'blue', 'brown', 
                  'pink', 'orange',
                  'purple', 'black', 'red']

    def __init__(self):
        self.time = 60
        self.score = 0
    
    def start(self):
        if self.time == 60:        #important cause if you start twice, then the color won't change
            self.fg_color = choice(ColorGame.colors)
            self.color_label.config(text=choice(ColorGame.colors), fg=self.fg_color)
            self.countdown()


    def reset(self):
        self.answer_entry.delete(0, tk.END)
        self.time = 60
        self.time_label.config(text='time: -')
        self.time_label.after_cancel(self.wait)
        self.score = 0
        self.score_label.config(text='score: -')
        self.color_label.config(text='Tap start to see', fg='black')


    def countdown(self):
        if self.time > 0:
            self.time -= 1
            self.time_label.config(text=f'{str(self.time)}')
            self.wait = self.time_label.after(1000, self.countdown)

    def entered_word(self, event):
        if self.time > 0:
            if self.answer_entry.get().lower() == self.fg_color.lower():
                self.score += 1
                self.score_label.config(text=f'score: {(str(self.score))}')
            self.answer_entry.delete(0, tk.END)
            self.fg_color = choice(ColorGame.colors)
            self.color_label.config(text=choice(ColorGame.colors), fg=self.fg_color)


    def Create_GUI(self):
        root = tk.Tk()
        root.title('Color Game')

        self.explain_label = tk.Label(root, text='Enter the color of the word shown below', fg='black')
        self.explain_label.grid(row=0, column=1, columnspan=4)

        self.time_label = tk.Label(root, text='time: -', fg='black')
        self.time_label.grid(row=1, column=2, columnspan=2)

        self.score_label = tk.Label(root, text='score: -', fg='black')
        self.score_label.grid(row=2, column=2, columnspan=2)

        self.color_label = tk.Label(root, text='Tap start to see', fg='black')
        self.color_label.grid(row=3, column=2, columnspan=2)     

        self.answer_entry = tk.Entry(root)
        self.answer_entry.grid(row=4, column=2, columnspan=2)
        self.answer_entry.bind('<Return>', self.entered_word)

        frame = tk.Frame()
        frame.grid(row=6, column=2, rowspan=2, columnspan=2, pady=5)

        self.start_btn = tk.Button(frame, text='Start', command=self.start, bg='light green')
        self.start_btn.grid(row=0, column=2, columnspan=2, ipadx=32, ipady=5)

        self.reset_btn = tk.Button(frame, text='Reset', command=self.reset, bg='light blue')
        self.reset_btn.grid(row=1, column=2, columnspan=2, ipadx=30, ipady=5)

        tk.mainloop()

a = ColorGame().Create_GUI()