import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N = 1000
N2 = 4000
delta_t = 1
delta_x = 1

c = 1

m = np.zeros((N, N2))

for i in range(10, 111):
    delta = np.pi / 100
    t = i - 10
    m[0][i] = (np.sin(t * delta)) ** 2
    
for i in range(11, 112):
    delta = np.pi / 100
    t = i - 11
    m[1][i] = (np.sin(t * delta)) ** 2

for  j in range(1, N2 - 1):
    for i in range(2, N - 1):
        m[i][j + 1] = 2 * m[i][j] - m[i][j - 1] + (c * delta_t / delta_x) ** 2 * (m[i + 1][j] - 2 * m[i][j] + m[i - 1][j])

a = np.arange(0, 1000, 1)

def colonne(matrice, k):
    l = []
    for i in range(0, len(matrice)):
        l.append(matrice[i][k])
    return l

# plt.plot(a, colonne(m, 100))

fig, ax = plt.subplots()

line, = ax.plot(a, colonne(m, 0))

def animate(i):
    line.set_ydata(colonne(m, i))  # update the data.
    return line,

ani = animation.FuncAnimation(
    fig, animate, interval=5, blit=False, save_count=50)

plt.ylim(top=1.1, bottom=-1.1)
plt.show()