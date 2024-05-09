from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFont, ImageDraw
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from io import BytesIO
import threading
import numpy as np
import sympy as sp

class Window(Tk):
    def __init__(self):
        super().__init__()

        # vars----------------------------------------------------------------------------------------------------------
        self.eqs_with_img = [] #список функций с их изображениями для оптимизации
        self.prew = ""
        self.len_eqs_prew = 0
        self.font = ImageFont.truetype('arial.ttf', 15)
        self.x, self.pi, self.e = sp.symbols('x, pi, e')
        self.setgendots = [] #eq, xot, xdo, yup\down
        self.dots_in = 0
        self.dots_out = 0
        self.area = 0
        self.flag_del = False
        # vars----------------------------------------------------------------------------------------------------------

        self.title("Вычисление площади плоской фигуры методом Монте-Карло")
        self.geometry("1000x600")
        self.configure(bg="white")
        self.iconbitmap('icon.ico')
        self.resizable(False, False)
        self.after(1000, self.start_eq_loop)

        self.create_buttons()
        self.create_entrys()
        self.create_labels()
        self.create_plot()

        self.x1_entry.insert(0, "-2")
        self.x2_entry.insert(0, "2")
        self.y1_entry.insert(0, "0")
        self.y2_entry.insert(0, "2")
        self.x1_prew = self.x1_entry.get()
        self.x2_prew = self.x2_entry.get()
        self.y1_prew = self.y1_entry.get()
        self.y2_prew = self.y2_entry.get()

        self.protocol("WM_DELETE_WINDOW", self._quit)

    def add_all_plot(self):
        self.ax.cla()
        self.ax.grid(True)
        x1 = float(self.x1_entry.get())
        x2 = float(self.x2_entry.get())
        y1 = float(self.y1_entry.get())
        y2 = float(self.y2_entry.get())
        self.ax.axvline(x=x1, color='b', linestyle='-')
        self.ax.axvline(x=x2, color='b', linestyle='-')
        x_arr = np.arange(x1 - 0.5, x2 + 0.51, 0.01)
        self.ax.plot(x_arr, x_arr*0 + y1)
        self.ax.plot(x_arr, x_arr*0 + y2)
        for ex in self.eqs_with_img:
            y_arr = []
            eq = (sp.sympify(ex[0]))
            for one_x_arr in x_arr:
                if isinstance(eq.evalf(subs={self.x: one_x_arr, self.pi: sp.pi, self.e: sp.E}),
                              sp.core.numbers.Float) or isinstance(
                        eq.evalf(subs={self.x: one_x_arr, self.pi: sp.pi, self.e: sp.E}), sp.core.numbers.Integer):
                    y_arr.append(eq.evalf(subs={self.x: one_x_arr, self.pi: sp.pi, self.e: sp.E}))
            if len(y_arr) != len(x_arr):
                self.ax.plot(x_arr[len(y_arr) + 1:], y_arr)
            else:
                self.ax.plot(x_arr, y_arr)

        self.canvas.draw()

    def recreate_eq_lb(self):
        self.eq_img_lb.config(image=self.tkimg_eq)
        self.eq_img_lb.image = self.tkimg_eq
        self.eq_img_lb.place(x=50, y=440)

    def update_eq(self):
        try:
            eq = (sp.sympify(self.prew))
            f = BytesIO()
            sp.preview(eq, viewer='BytesIO', outputbuffer=f)
            f.seek(0)
            img_eq = Image.open(f)
            self.tkimg_eq = ImageTk.PhotoImage(img_eq)
            self.recreate_eq_lb()
        except:
            ...

    def update_eqs(self):
        eqs_image = Image.new('RGB', (300, len(self.eqs_with_img) * 45), (255, 255, 255))
        drawer = ImageDraw.Draw(eqs_image)
        prew_y = 0
        for i, eqq in enumerate(self.eqs_with_img):
            if eqq[1] == None:
                eq = (sp.sympify(eqq[0]))
                f = BytesIO()
                sp.preview(eq, viewer='BytesIO', outputbuffer=f)
                f.seek(0)
                img_eq = Image.open(f)
                self.eqs_with_img[i][1] = img_eq
                drawer.text((2, prew_y + (img_eq.size[1] // 2) - 8), f'{i + 1})', font=self.font, fill='black')
                eqs_image.paste(img_eq, (25, prew_y))
                prew_y += img_eq.size[1] + 10

            else:
                img_eq = eqq[1]
                drawer.text((2, prew_y + (img_eq.size[1] // 2) - 8), f'{i + 1})', font=self.font, fill='black')
                eqs_image.paste(img_eq, (25, prew_y))
                prew_y += img_eq.size[1] + 10

        eqs_image = ImageTk.PhotoImage(eqs_image)
        self.eqs_img_lb.config(image=eqs_image)
        self.eqs_img_lb.image = eqs_image
        self.eqs_img_lb.place(x=20, y=20)
        print(self.eqs_with_img)

    def start_eq_loop(self):
        if self.prew != self.enter_entry.get():
            self.prew = self.enter_entry.get()
            self.eq_loop = threading.Thread(target=self.update_eq)
            self.eq_loop.start()
        if self.enter_entry.get() == "":
            self.tkimg_eq = None
            self.recreate_eq_lb()
        if self.len_eqs_prew != len(self.eqs_with_img) or self.x1_prew != self.x1_entry.get() or self.x2_prew != self.x2_entry.get() or self.y1_prew != self.y1_entry.get() or self.y2_prew != self.y2_entry.get():
            self.len_eqs_prew = len(self.eqs_with_img)
            self.x1_prew = self.x1_entry.get()
            self.x2_prew = self.x2_entry.get()
            self.y1_prew = self.y1_entry.get()
            self.y2_prew = self.y2_entry.get()
            eqs_loop = threading.Thread(target=self.update_eqs)
            add_plot = threading.Thread(target=self.add_all_plot)
            eqs_loop.start()
            add_plot.start()

        self.after(500, self.start_eq_loop)

    def del_last_eq(self):
        del self.eqs_with_img[-1]

    def del_all_eq(self):
        self.eqs_with_img.clear()

    def add_eq(self):
        self.eqs_with_img.append([self.enter_entry.get(), None])

    def setgen(self):
        if len(self.eqs_with_img) != 0:
            self.settingsgen = WinGenDots(self)
        else:
            messagebox.showerror("Ошибка!", "Функции отсутствуют!")

    def create_buttons(self):
        self.input_button = ttk.Button(text="Ввести формулу", command=self.add_eq)
        self.input_button.place(x=40, y=530)

        self.clear_eq_button = ttk.Button(text="Удалить последнее уравнение", command=self.del_last_eq)
        self.clear_eq_button.place(x=20, y=400)

        self.clear_all_eq_button = ttk.Button(text="Удалить все уравнения", command=self.del_all_eq)
        self.clear_all_eq_button.place(x=215, y=400)

        self.dots_gen = ttk.Button(text="Сгенерировать", command=self.setgen)
        self.dots_gen.place(x=810, y=469)

    def create_entrys(self):
        self.enter_entry = ttk.Entry()
        self.enter_entry.place(x=40, y=500, width=330)

        self.x1_entry = ttk.Entry()
        self.x1_entry.place(x=670, y=410, width=50)

        self.x2_entry = ttk.Entry()
        self.x2_entry.place(x=790, y=410, width=50)

        self.y1_entry = ttk.Entry()
        self.y1_entry.place(x=670, y=440, width=50)

        self.y2_entry = ttk.Entry()
        self.y2_entry.place(x=790, y=440, width=50)

        self.count_dots = ttk.Entry()
        self.count_dots.place(x=700, y=470, width=100)

    def create_labels(self):
        self.y_label = ttk.Label(text="f(x) =")
        self.y_label.configure(background="white")
        self.y_label.place(x=10, y=500)

        self.x1_label = ttk.Label(text="X от")
        self.x1_label.configure(background="white")
        self.x1_label.place(x=640, y=410)

        self.x2_label = ttk.Label(text="X до")
        self.x2_label.configure(background="white")
        self.x2_label.place(x=760, y=410)

        self.y1_label = ttk.Label(text="Y от")
        self.y1_label.configure(background="white")
        self.y1_label.place(x=640, y=440)

        self.y2_label = ttk.Label(text="Y до")
        self.y2_label.configure(background="white")
        self.y2_label.place(x=760, y=440)

        self.dots_count_label = ttk.Label(text="Кол-во точек:")
        self.dots_count_label.configure(background="white")
        self.dots_count_label.place(x=620, y=470)

        self.eq_img_lb = Label()#root)
        self.eq_img_lb.configure(bg="white")
        self.eq_img_lb.place(x=50, y=440)

        self.eqs_img_lb = Label()#root)
        self.eqs_img_lb.configure(bg="white")
        self.eqs_img_lb.place(x=5, y=5)

        self.area_res = Label(text="Площадь плоской фигуры ≈ ...", font="Calibri 16")
        self.area_res.configure(bg="white")
        self.area_res.place(x=620, y=520)

    def create_plot(self):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=500, y=0)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().place(x=500, y=0)

    def _quit(self):
        self.quit()
        self.destroy()

    def generate_dots(self):
        print(self.setgendots)
        rand_dots_x_in = []
        rand_dots_y_in = []
        rand_dots_x_out = []
        rand_dots_y_out = []

        if self.flag_del:
            self.dots_red.remove()
            self.dots_green.remove()

        if self.flag_del == False:
            self.flag_del = not self.flag_del

        rand_dots_x = np.random.uniform(float(self.x1_entry.get()), float(self.x2_entry.get()), int(self.count_dots.get()))
        rand_dots_y = np.random.uniform(float(self.y1_entry.get()), float(self.y2_entry.get()), int(self.count_dots.get()))
        for dot in range(len(rand_dots_x)):
            flg_in = True
            for setgeneq in self.setgendots:
                if rand_dots_x[dot] > setgeneq[1] and rand_dots_x[dot] <= setgeneq[2]:
                    eq = sp.sympify(setgeneq[0])
                    if setgeneq[3] == 0:
                        if not (rand_dots_y[dot] <= eq.evalf(subs={self.x: rand_dots_x[dot], self.pi: sp.pi, self.e: sp.E})):
                            flg_in = False
                    elif setgeneq[3] == 1:
                        if not (rand_dots_y[dot] > eq.evalf(subs={self.x: rand_dots_x[dot], self.pi: sp.pi, self.e: sp.E})):
                            flg_in = False

            if flg_in:
                rand_dots_x_in.append(rand_dots_x[dot])
                rand_dots_y_in.append(rand_dots_y[dot])
            else:
                rand_dots_x_out.append(rand_dots_x[dot])
                rand_dots_y_out.append(rand_dots_y[dot])

        self.dots_in = len(rand_dots_x_in)
        self.dots_out = len(rand_dots_x_out)
        self.area = abs(float(self.x2_entry.get()) - float(self.x1_entry.get())) * abs(float(self.y2_entry.get()) - float(self.y1_entry.get()))

        self.area_res.configure(text=f'Площадь плоской фигуры ≈ {(self.dots_in / (self.dots_in + self.dots_out) * self.area):.6f}')

        self.dots_red = self.ax.scatter(rand_dots_x_out, rand_dots_y_out, color="r", s=0.08)
        self.dots_green = self.ax.scatter(rand_dots_x_in, rand_dots_y_in, color="g", s=0.08)

        self.canvas.draw()

class WinGenDots(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.eqs_with_img = window.eqs_with_img
        self.entrys = []
        self.checks_y = []
        self.labels = []

        self.y_win = len(self.eqs_with_img) * 60 + 20
        self.var_ch = IntVar()
        self.var_ch.set(0)

        self.title("Settings Gen")
        self.geometry(f"500x{self.y_win}")
        self.configure(bg="white")
        self.iconbitmap('icon.ico')
        self.resizable(False, False)

        self.sgen = ttk.Button(self, text="Сгенерировать", command=self.generate)
        self.sgen.place(x=390, y=self.y_win - 35)

        self.eqs_img_label = Label(self)
        self.eqs_img_label.configure(bg="white")
        self.eqs_img_label.place(x=5, y=5)

        eqs_img = Image.new('RGB', (300, len(self.eqs_with_img) * 45), (255, 255, 255))
        drawer = ImageDraw.Draw(eqs_img)
        prew_y = 0

        for i, eqq in enumerate(self.eqs_with_img):
            self.entrys.append([ttk.Entry(self, width=3), ttk.Entry(self, width=3)])
            self.labels.append([Label(self, text="X от", background="white"), Label(self, text="X до", background="white")])
            var_ch = IntVar()
            var_ch.set(0)
            self.checks_y.append([var_ch, ttk.Radiobutton(self, text="Y up", variable=var_ch, value=0), ttk.Radiobutton(self, text="Y down", variable=var_ch, value=1)])
            img_eq = eqq[1]
            drawer.text((2, prew_y + (img_eq.size[1] // 2) - 8), f'{i + 1})', font=window.font, fill='black')
            eqs_img.paste(img_eq, (25, prew_y))

            self.entrys[i][0].place(x=300, y=prew_y + (img_eq.size[1] // 2) + 12)
            self.entrys[i][1].place(x=355, y=prew_y + (img_eq.size[1] // 2) + 12)

            self.checks_y[i][1].place(x=380, y=prew_y + (img_eq.size[1] // 2) + 12)
            self.checks_y[i][2].place(x=430, y=prew_y + (img_eq.size[1] // 2) + 12)

            self.labels[i][0].place(x=270, y=prew_y + (img_eq.size[1] // 2) + 12)
            self.labels[i][1].place(x=325, y=prew_y + (img_eq.size[1] // 2) + 12)

            prew_y += img_eq.size[1] + 20

        eqs_img = ImageTk.PhotoImage(eqs_img)
        self.eqs_img_label.config(image=eqs_img)
        self.eqs_img_label.image = eqs_img
        self.eqs_img_label.place(x=20, y=20)


    def generate(self):
        sgd = []
        try:
            for i in range(len(self.eqs_with_img)):
                sgd.append([self.eqs_with_img[i][0], float(self.entrys[i][0].get()), float(self.entrys[i][1].get()), self.checks_y[i][0].get()])
            window.setgendots = sgd
            start_gen = threading.Thread(target=window.generate_dots)
            start_gen.start()
            if int(window.count_dots.get()) >= 50000:
                messagebox.showinfo("Генерируем", "Ожидайте, происходит генерация!\n\nПредупреждение - чем больше вы указываете кол-во точем, тем дольше ждать!")
            window.settingsgen.destroy()
        except:
            messagebox.showerror("Ошибка!", "Ошибка заполнения полей!")

if __name__ == "__main__":
    window = Window()
    window.mainloop()