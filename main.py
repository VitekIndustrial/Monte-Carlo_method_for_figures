import numpy as np
import matplotlib.pyplot as plt
import math

dots_count = 10_000_000

rand_dots_x = np.random.uniform(-2, 2, dots_count)
rand_dots_y = np.random.uniform(0, 5, dots_count)

rand_dots_x_in = []
rand_dots_x_out = []
rand_dots_y_in = []
rand_dots_y_out = []

for dot in range(len(rand_dots_x)):
    if rand_dots_y[dot] >= 0 and rand_dots_y[dot] <= (math.sin(rand_dots_x[dot]*2) + 4):
        rand_dots_x_in.append(rand_dots_x[dot])
        rand_dots_y_in.append(rand_dots_y[dot])
    else:
        rand_dots_x_out.append(rand_dots_x[dot])
        rand_dots_y_out.append(rand_dots_y[dot])


plt.scatter(rand_dots_x_out, rand_dots_y_out, color="r", s=0.08)
plt.scatter(rand_dots_x_in, rand_dots_y_in, color="g", s=0.08)

np.set_printoptions(threshold=np.inf)
plt.title(f'Всего точек: {len(rand_dots_x)}, Входящих точек: {len(rand_dots_x_in)}, Не входящих точек: {len(rand_dots_x_out)}')

x = np.arange(-2.5, 2.51, 0.01)
plt.plot(x, np.sin(x*2) + 4)
plt.plot(x, x*0)
plt.axvline(x=-2, color='b', linestyle='-') #Вертикальная линия
plt.axvline(x=2, color='g', linestyle='-') #Вертикальная линия
plt.show()
print(f'Всего точек: {len(rand_dots_x)}, Входящих точек: {len(rand_dots_x_in)}, Не входящих точек: {len(rand_dots_x_out)}')