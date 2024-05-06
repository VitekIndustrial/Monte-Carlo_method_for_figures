from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

class Window(Tk):
    def __init__(self):
        super().__init__()

        self.title("Window")
        self.geometry("1000x600")
        self.configure(bg="white")
        self.resizable(False, False)

        self.create_buttons()
        self.create_entrys()
        self.create_labels()
        self.create_plot()

        self.protocol("WM_DELETE_WINDOW", self._quit)

    def create_buttons(self):
        self.input_button = ttk.Button(text="Ввести формулу")#, command=add_eq)
        self.input_button.place(x=40, y=530)

        self.clear_eq_button = ttk.Button(text="Удалить последнее уравнение")#, command=del_last_eq)
        self.clear_eq_button.place(x=20, y=400)

        self.clear_all_eq_button = ttk.Button(text="Удалить все уравнения")#, command=del_all_eq)
        self.clear_all_eq_button.place(x=215, y=400)

        self.result_button = ttk.Button(text="Вычислить площадь")#, command=result)
        self.result_button.place(x=860, y=530)

        self.dots_gen = ttk.Button(text="Сгенерировать")#, command=start_gen)
        self.dots_gen.place(x=810, y=439)

    def create_entrys(self):
        #global enter_entry, x1_entry, x2_entry, count_dots
        self.enter_entry = ttk.Entry()
        self.enter_entry.place(x=40, y=500, width=330)

        self.x1_entry = ttk.Entry()
        self.x1_entry.place(x=670, y=410, width=50)

        self.x2_entry = ttk.Entry()
        self.x2_entry.place(x=790, y=410, width=50)

        self.count_dots = ttk.Entry()
        self.count_dots.place(x=700, y=440, width=100)

    def create_labels(self):
        #global eq_img_lb, eqs_img_lb

        self.y_label = ttk.Label(text="f(x) =")
        self.y_label.configure(background="white")
        self.y_label.place(x=10, y=500)

        self.x1_label = ttk.Label(text="X от")
        self.x1_label.configure(background="white")
        self.x1_label.place(x=640, y=410)

        self.x2_label = ttk.Label(text="X до")
        self.x2_label.configure(background="white")
        self.x2_label.place(x=760, y=410)

        self.dots_count_label = ttk.Label(text="Кол-во точек:")
        self.dots_count_label.configure(background="white")
        self.dots_count_label.place(x=620, y=440)

        self.eq_img_lb = Label()#root)
        self.eq_img_lb.configure(bg="black") #white
        self.eq_img_lb.place(x=50, y=440)

        self.eqs_img_lb = Label()#root)
        self.eqs_img_lb.configure(bg="black") #white
        # eqs_img_lb.place(x=5, y=5)

    def create_plot(self):
        #global ax, toolbar, canvas
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True)
        # ax.plot(x, np.sin(x*2) + 4, color='g')
        # ax.plot(x, x * 0)
        # ax.axvline(x=-2, color='b', linestyle='-')  # Вертикальная линия
        # ax.axvline(x=2, color='g', linestyle='-')  # Вертикальная линия
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=500, y=0)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().place(x=500, y=0)

    def _quit(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    window = Window()
    window.mainloop()