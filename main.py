from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np

#-----------------------------------------------------------------------------------------
x = np.arange(-2.5, 2.51, 0.01)
root = None
#-----------------------------------------------------------------------------------------

def createRootWindow(title: str = "Title", icon: str = "", size_window: set = (1000, 600), resize_window: set = (False, False)):
    root = Tk()
    root.title(title)
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

if __name__ == "__main__":
    root = createRootWindow()
    root.protocol("WM_DELETE_WINDOW", _quit)
    crateplot()
    root.mainloop()