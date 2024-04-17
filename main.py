from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from io import BytesIO
import numpy as np
import sympy as sp
import threading

#-----------------------------------------------------------------------------------------
x = np.arange(-2.5, 2.51, 0.01)
root = None
prew = ""
#-----------------------------------------------------------------------------------------

def recreate_eq_lb(imag):
    eq_img_lb.config(image=imag)
    eq_img_lb.image = imag
    eq_img_lb.place(x=50, y=440)
def addeq():
    yr = enter_entry.get()
    eq = (sp.sympify(yr))
    f = BytesIO()
    sp.preview(eq, viewer='BytesIO', outputbuffer=f)
    sp.preview(eq, viewer='file', filename='1.png')
    f.seek(0)
    img_eq = Image.open(f)
    tkimg_eq = ImageTk.PhotoImage(img_eq)
    recreate_eq_lb(tkimg_eq)

def update_eq(prew):
    try:
        eq = (sp.sympify(prew))
        f = BytesIO()
        sp.preview(eq, viewer='BytesIO', outputbuffer=f)
        sp.preview(eq, viewer='file', filename='1.png')
        f.seek(0)
        img_eq = Image.open(f)
        tkimg_eq = ImageTk.PhotoImage(img_eq)
        recreate_eq_lb(tkimg_eq)
    except:
        ...

def start_eq_loop():
    global prew
    if prew != enter_entry.get():
        prew = enter_entry.get()
        eq_loop = threading.Thread(target=update_eq, args=(prew,))
        eq_loop.start()
    root.after(500, start_eq_loop)

def del_last_eq():
    ...

def del_all_eq():
    ...

def createRootWindow(title: str = "Title", icon: str = "", size_window: set = (1000, 600), resize_window: set = (False, False)):
    root = Tk()
    root.title(title)
    root.configure(bg="white")
    if icon != "": root.iconbitmap(icon)
    root.geometry(f'{size_window[0]}x{size_window[1]}')
    root.resizable(resize_window[0], resize_window[1])
    return root

def _quit():
    root.quit()
    root.destroy()

def crateplot():
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x, np.sin(x*2) + 4, color='g')
    ax.plot(x, x * 0)
    ax.axvline(x=-2, color='b', linestyle='-')  # Вертикальная линия
    ax.axvline(x=2, color='g', linestyle='-')  # Вертикальная линия
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=500, y=0)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().place(x=500, y=0)

def result():
    ...

def create_buttons():
    input_button = ttk.Button(text="Ввести формулу", command=addeq)
    input_button.place(x=20, y=530)

    clear_eq_button = ttk.Button(text="Удалить последнее уравнение", command=del_last_eq)
    clear_eq_button.place(x=20, y=400)

    clear_all_eq_button = ttk.Button(text="Удалить все уравнения", command=del_all_eq)
    clear_all_eq_button.place(x=215, y=400)

    result_button = ttk.Button(text="Вычислить площадь", command=result)
    result_button.place(x=860, y=530)

def create_entrys():
    global enter_entry, x1_entry, x2_entry
    enter_entry = ttk.Entry()
    enter_entry.place(x=20, y=500, width=330)

    x1_entry = ttk.Entry()
    x1_entry.place(x=670, y=410, width=50)

    x2_entry = ttk.Entry()
    x2_entry.place(x=790, y=410, width=50)

def create_labels():
    global  eq_img_lb
    x1_label = ttk.Label(text="X от")
    x1_label.configure(background="white")
    x1_label.place(x=640, y=410)

    x2_label = ttk.Label(text="X до")
    x2_label.configure(background="white")
    x2_label.place(x=760, y=410)

    eq_img_lb = Label(root)
    eq_img_lb.place(x=20, y=20)
#Добавить ввод кол-ва точек и кнопку их генерации
if __name__ == "__main__":
    root = createRootWindow()
    root.protocol("WM_DELETE_WINDOW", _quit)
    create_buttons()
    create_entrys()
    create_labels()
    crateplot()
    root.after(1000, start_eq_loop)
    root.mainloop()
