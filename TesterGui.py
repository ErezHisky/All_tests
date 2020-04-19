
#=================
#  imports
#=================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu

win = tk.Tk()

win.title("Tester hiSky GUI")

tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Tab 1")
tabControl.grid(column = 10, row = 10) #, expand=1, fill = "both"
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="Tab 2")

hello_lbl = ttk.Label(win, text="Hello from Tester")
hello_lbl.grid(column=0, row=0)

def clickMe1():
    action.configure(text="** I have been clicked! **")
    hello_lbl.configure(foreground='red')
    hello_lbl.configure(text= 'A red label')

action = ttk.Button(win, text="Start the test !" ,command=clickMe1)
action.grid(column=1, row=0)

ttk.Label(win, text="Please enter a name : ").grid(column=0, row=1)

name = tk.StringVar()
name_entered = ttk.Entry(win, width=12, textvariable=name)
name_entered.grid(column=0, row=2)

def clickMe2():
    action2.configure(text="Hello " + name.get() + ' ' + number_chosen.get())

action2 = ttk.Button(win, text="click !" ,command=clickMe2)
action2.grid(column=2, row=2)

# combobox
ttk.Label(win, text="Chhose a number").grid(column=1,row=1)
number = tk.StringVar()
number_chosen = ttk.Combobox(win, width=12, textvariable=number)
number_chosen['values'] = (1, 2, 3, 42, 100)
number_chosen.grid(column=1, row=2)
number_chosen.current(0)

#checkbutton
chVarDis = tk.IntVar()
check1 = tk.Checkbutton(win, text="Disabled", variable=chVarDis, state='disabled')
check1.select()
check1.grid(column=0, row=4, sticky=tk.W) # tk.W(=west) - aligned to the left

chVarUn = tk.IntVar()
check2 = tk.Checkbutton(win, text="UnChecked", variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=4, sticky=tk.W)

chVarEn = tk.IntVar()
check1 = tk.Checkbutton(win, text="Enabled", variable=chVarEn)
check1.select()
check1.grid(column=2, row=4, sticky=tk.W)

# radiobutton
colors = ["Blue", "Gold", "Red"]

def radCall():
    radSel = radVar.get()
    if radSel == 0: win.configure(background=colors[0])
    if radSel == 1: win.configure(background=colors[1])
    if radSel == 2: win.configure(background=colors[2])

radVar = tk.IntVar()
radVar.set(99) #non - existing index

for col in range(3):
    curRad = tk.Radiobutton(win, text=colors[col], variable=radVar,
                            value=col, command=radCall)
    curRad.grid(column=col, row=5, sticky=tk.W)

# scrolled Text control
scrol_w = 30
scrol_h = 3
scr = scrolledtext.ScrolledText(win, width=scrol_w, height=scrol_h, wrap=tk.WORD) #break lines by words
scr.grid(column=0, columnspan=3)

#Creaet a container to hold labels
buttons_frame = ttk.LabelFrame(win, text=' Labels in a Frame ')
buttons_frame.grid(column=1, row=7, padx=10, pady=10)

#place labels inside the container
ttk.Label(buttons_frame, text='Label1').grid(column=0, row=0, sticky=tk.W)
ttk.Label(buttons_frame, text='Label2').grid(column=1, row=0, sticky=tk.W)
ttk.Label(buttons_frame, text='Label3').grid(column=2, row=0, sticky=tk.W)

for child in buttons_frame.winfo_children():
    child.grid_configure(padx=8, pady=4)


def _quit():
    win.quit()
    win.destroy()
    exit()

#create menu
menu_bar = Menu(win)
win.config(menu=menu_bar)

#create file menu item
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="new")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=_quit)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About")

name_entered.focus() #Place cursor into name Entry

#================
#   Start GUI
#================
win.mainloop()