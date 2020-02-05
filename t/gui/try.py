from tkinter import *
from tkinter import ttk

def changed():
    print(var1.get())
    if var1.get() == '1':
        rb.configure(state = NORMAL)
    elif var1.get() == 'F':
        rb.configure(state = DISABLED)
    
f = Tk()
var1 = StringVar()
cb = ttk.Checkbutton(f, text='Checkbox', variable=var1, onvalue=True, offvalue='F', command = changed)
cb.pack()

var2 = StringVar()
rb = ttk.Radiobutton(f, text='Radiobutton', variable = var2)
rb.pack()

rb.configure(state = DISABLED)
rb.configure(state = NORMAL)
