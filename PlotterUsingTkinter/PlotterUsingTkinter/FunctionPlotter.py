from decimal import DivisionByZero
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning
import numpy as np
import matplotlib.pyplot as plt
import re
import math

# intiating the settings of the program
plt.rcParams["figure.autolayout"] = True
root = Tk()
root.geometry("600x300+500+160")
root.title("FunctionPlotter")
root.config(bg='grey')
root.resizable(0, 0)

for i in range(7):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=2)
style = ttk.Style()
style.theme_use('vista')
# confinguration
style.configure("TButton", width=20)


# defining the elements
# entries
eqTaker = Entry(root, border=4, state='disabled')
min = Entry(root, border=4)
max = Entry(root, border=4)

# labels
MinLabel = Label(root, text="minVal", bg='grey')
MaxLabel = Label(root, text="MaxVal", bg='grey', pady=10)
eqLabel = Label(root, text="Equation", bg='grey')

# buttons
but0 = ttk.Button(root, text='0', command=lambda: but_click(0))
but1 = ttk.Button(root, text='1', command=lambda: but_click(1))
but2 = ttk.Button(root, text='2', command=lambda: but_click(2))
but3 = ttk.Button(root, text='3', command=lambda: but_click(3))
but4 = ttk.Button(root, text='4', command=lambda: but_click(4))
but5 = ttk.Button(root, text='5', command=lambda: but_click(5))
but6 = ttk.Button(root, text='6', command=lambda: but_click(6))
but7 = ttk.Button(root, text='7', command=lambda: but_click(7))
but8 = ttk.Button(root, text='8', command=lambda: but_click(8))
but9 = ttk.Button(root, text='9', command=lambda: but_click(9))

# operators
butplus = ttk.Button(root, text='+', command=lambda: but_click('+'))
butdiv = ttk.Button(root, text='/', command=lambda: but_click('/'))
butminus = ttk.Button(root, text='-', command=lambda: but_click('-'))
butmul = ttk.Button(root, text='*', command=lambda: but_click('*'))
butpow = ttk.Button(root, text='^', command=lambda: but_click('^'))

# functions
butexp = ttk.Button(root, text='e', command=lambda: but_click('exp('))
butX = ttk.Button(root, text='X', command=lambda: but_click('x'))
butopenbrac = ttk.Button(root, text='(', command=lambda: but_click('('))
butcloesdbrac = ttk.Button(root, text=')', command=lambda: but_click(')'))
butdel = ttk.Button(root, text='del', command=lambda: but_del())
butclr = ttk.Button(root, text='CLR', command=lambda: but_clr())
butdrw = ttk.Button(root, text='Draw', command=lambda: Draw())

# Showing the objects
# labels
eqLabel.grid(row=0, column=0)
MinLabel.grid(row=1, column=0)
MaxLabel.grid(row=1, column=3)

# entries
eqTaker.grid(row=0, column=1, padx=(0, 10),
             columnspan=6, sticky='snew', pady=10)
min.grid(row=1, column=1, columnspan=2, sticky='ew')
max.grid(row=1, column=4, padx=10, columnspan=3, sticky='ew')

# buttons
but0.grid(row=5, column=0, padx=0, columnspan=3,
          ipady=14, ipadx=10, sticky='snew')
but1.grid(row=2, column=0, padx=0, ipady=14,  ipadx=10)
but2.grid(row=2, column=1, padx=0, ipady=14, ipadx=10)
but3.grid(row=2, column=2, padx=0, ipady=14, ipadx=10)

but4.grid(row=3, column=0, padx=0, ipady=14, ipadx=10)
but5.grid(row=3, column=1, padx=0, ipady=14, ipadx=10)
but6.grid(row=3, column=2, padx=0, ipady=14, ipadx=10)

but7.grid(row=4, column=0, padx=0, ipady=14, ipadx=10)
but8.grid(row=4, column=1, padx=0, ipady=14, ipadx=10)
but9.grid(row=4, column=2, padx=0, ipady=14, ipadx=10)

# operations
butplus.grid(row=2, column=3,  ipady=14, ipadx=5, padx=(5, 0))
butdiv.grid(row=2, column=4, ipady=14, ipadx=5)
butminus.grid(row=2, column=5, ipadx=5, ipady=14, padx=(0, 0))
butmul.grid(row=3, column=3, ipady=14, ipadx=5, padx=(5, 0))
butpow.grid(row=3, column=4, ipady=14, ipadx=5)
butexp.grid(row=3, column=5, ipady=14, ipadx=5)

#braces and x
butopenbrac.grid(row=4, column=3, ipady=14, ipadx=5, padx=(5, 0))
butcloesdbrac.grid(row=4, column=4, ipady=14, ipadx=5)
butX.grid(row=4, column=5, ipady=14, ipadx=5)

# clr del and draw
butdel.grid(row=2, column=6, ipady=14, ipadx=5, rowspan=3, sticky='sn')
butclr.grid(row=5, column=5, columnspan=2, sticky='ew',
            ipady=14, ipadx=5)
butdrw.grid(row=5, column=3, columnspan=2, sticky='ew',
            ipady=14, ipadx=5, padx=(5, 0))

# functions
# delete last character


def but_del():
    eqTaker.config(state='normal')
    size = eqTaker.get()
    eqTaker.delete(size.__len__() - 1, END)
    eqTaker.config(state='disabled')


# to clear the text
def but_clr():
    eqTaker.config(state='normal')
    eqTaker.delete(0, END)
    eqTaker.config(state='disabled')


def but_click(number):
    eqTaker.config(state='normal')
    current = eqTaker.get()
    eqTaker.delete(0, END)
    eqTaker.insert(0, str(current) + str(number))
    eqTaker.config(state='disabled')


replacements = {
    'exp': 'np.exp',
    '^': '**',
}

allowed_words = [
    'x',
    'exp',
]


def string2func(string):
    ''' evaluates the string and returns a function of x '''
    # replace the user input into python expression
    for old, new in replacements.items():
        string = string.replace(old, new)

    def func(x):
        l = eval(string)
        # check for infinity if divide by zero
        idx = np.argwhere(l == math.inf)
        if(l[idx] == math.inf):
            showwarning("Division by Zero",
                        "Your Equation contains a Division by zero over the specified range!")
        return l

    return func


def Draw():
    if min.get() != '' and max.get() != '' and eqTaker != '':  # entries must be not empty
        try:
            func = string2func(eqTaker.get())
            mn = int(min.get())
            mx = int(max.get())
            if mn >= mx:
                showerror("min and  max", "min should be less than max")
                return
            x = np.arange(mn, mx, .5)

            plt.plot(x, func(x))
            plt.xlim(mn, mx)

            plt.show()
        except:
            showerror(
                "Wrong Format", "Please check the equation formate because it is not correct!\n tips:\n 2x is not correct it should be 2*x \n check brackets \n equation must contain x")
    else:
        showerror("empty entry", "please put equation and values!")

# close the window if the user pressed escape


def Exit(event):
    root.destroy()


root.bind('<Escape>', Exit)


root.mainloop()
