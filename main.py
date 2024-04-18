from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from io import BytesIO
import numpy as np
import sympy as sp
import threading
import math

#-----------------------------------------------------------------------------------------
x = np.arange(-2.5, 2.51, 0.01)
root = None
prew = ""
ax = None
rand_dots_x = []
rand_dots_y = []
rand_dots_x_in = []
rand_dots_y_in = []
rand_dots_x_out = []
rand_dots_y_out = []
#-----------------------------------------------------------------------------------------

def recreate_eq_lb(imag):
    eq_img_lb.config(image=imag)
    eq_img_lb.image = imag
    eq_img_lb.place(x=50, y=440)

def update_eq(prew):
    try:
        eq = (sp.sympify(prew))
        f = BytesIO()
        sp.preview(eq, viewer='BytesIO', outputbuffer=f)
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
    if enter_entry.get() == "":
        recreate_eq_lb(None)
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
    global ax, fig, toolbar, canvas
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x, np.sin(x*2) + 4, color='g')
    ax.plot(x, x * 0)
    ax.axvline(x=-2, color='b', linestyle='-')  # Вертикальная линия
    ax.axvline(x=2, color='g', linestyle='-')  # Вертикальная линия
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=500, y=0)
    #toolbar = NavigationToolbar2Tk(canvas, root)
    #toolbar.update()
    #canvas.get_tk_widget().place(x=500, y=0)

def gen_dots_plot():
    global rand_dots_x, rand_dots_y, rand_dots_x_in, rand_dots_y_in, rand_dots_x_out, rand_dots_y_out, ax, canvas
    rand_dots_x = np.random.uniform(float(x1_entry.get()), float(x2_entry.get()), int(count_dots.get()))
    rand_dots_y = np.random.uniform(0, 5, int(count_dots.get()))
    for dot in range(len(rand_dots_x)):
        if rand_dots_y[dot] >= 0 and rand_dots_y[dot] <= (math.sin(rand_dots_x[dot] * 2) + 4):
            rand_dots_x_in.append(rand_dots_x[dot])
            rand_dots_y_in.append(rand_dots_y[dot])
        else:
            rand_dots_x_out.append(rand_dots_x[dot])
            rand_dots_y_out.append(rand_dots_y[dot])
    ax.scatter(rand_dots_x_out, rand_dots_y_out, color="r", s=0.08)
    ax.scatter(rand_dots_x_in, rand_dots_y_in, color="g", s=0.08)
    canvas.draw()

def start_gen():
    generate = threading.Thread(target=gen_dots_plot)
    generate.start()

def result():
    ...

def create_buttons():
    input_button = ttk.Button(text="Ввести формулу", command=...)
    input_button.place(x=40, y=530)

    clear_eq_button = ttk.Button(text="Удалить последнее уравнение", command=del_last_eq)
    clear_eq_button.place(x=20, y=400)

    clear_all_eq_button = ttk.Button(text="Удалить все уравнения", command=del_all_eq)
    clear_all_eq_button.place(x=215, y=400)

    result_button = ttk.Button(text="Вычислить площадь", command=result)
    result_button.place(x=860, y=530)

    dots_gen = ttk.Button(text="Сгенерировать", command=start_gen)
    dots_gen.place(x=810, y=439)

def create_entrys():
    global enter_entry, x1_entry, x2_entry, count_dots
    enter_entry = ttk.Entry()
    enter_entry.place(x=40, y=500, width=330)

    x1_entry = ttk.Entry()
    x1_entry.place(x=670, y=410, width=50)

    x2_entry = ttk.Entry()
    x2_entry.place(x=790, y=410, width=50)

    count_dots = ttk.Entry()
    count_dots.place(x=700, y=440, width=100)

def create_labels():
    global  eq_img_lb

    y_label = ttk.Label(text="f(x) =")
    y_label.configure(background="white")
    y_label.place(x=10, y=500)

    x1_label = ttk.Label(text="X от")
    x1_label.configure(background="white")
    x1_label.place(x=640, y=410)

    x2_label = ttk.Label(text="X до")
    x2_label.configure(background="white")
    x2_label.place(x=760, y=410)

    dots_count_label = ttk.Label(text="Кол-во точек:")
    dots_count_label.configure(background="white")
    dots_count_label.place(x=620, y=440)

    eq_img_lb = Label(root)
    eq_img_lb.configure(bg="white")
    eq_img_lb.place(x=50, y=440)

if __name__ == "__main__":
    root = createRootWindow()
    root.protocol("WM_DELETE_WINDOW", _quit)
    create_buttons()
    create_entrys()
    create_labels()
    crateplot()
    root.after(1000, start_eq_loop)
    root.mainloop()
