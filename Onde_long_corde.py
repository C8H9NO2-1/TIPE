import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N = 200
N2 = 4000
delta_t = 1
delta_x = 1

c = 1

m = np.zeros((N, N2))

def initOnde4fronts():
    for i in range(10, 210):
        delta = 2*np.pi / 100
        t = i - 10
        m[0][i] = (np.sin(t * delta)) ** 2

    for i in range(11, 211):
        delta = 2*np.pi / 100
        t = i - 11
        m[1][i] = (np.sin(t * delta)) ** 2

def initRais():
    for i in range(0, 399):
        delta = 2*np.pi / 100
        m[0][i] = (np.sin(i * delta)) ** 2

    for i in range(1, 400):
        delta = 2*np.pi / 100
        m[1][i] = (np.sin(i * delta)) ** 2

def initDeuxRais():
    for i in range(0, 399):
        delta = 2*np.pi / 400
        m[0][i] = (np.sin(i * delta)) ** 2

    for i in range(1, 400):
        delta = 2*np.pi / 400
        m[1][i] = (np.sin(i * delta)) ** 2

def initUneRais():
    for i in range(0, 399):
        delta = 2*np.pi / 800
        m[0][i] = (np.sin(i * delta)) ** 2

    for i in range(1, 400):
        delta = 2*np.pi / 800
        m[1][i] = (np.sin(i * delta)) ** 2

#initDeuxRais()
#initRais()
initUneRais()
#initOnde4fronts()
#initUneRais()

for  j in range(1, N2 - 1):
    for i in range(2, N - 1):
        m[i][j + 1] = 2 * m[i][j] - m[i][j - 1] + (c * delta_t / delta_x) ** 2 * (m[i + 1][j] - 2 * m[i][j] + m[i - 1][j])

a = np.arange(0, 200, 1)


# plt.plot(a, colonne(m, 100))

fig, ax = plt.subplots()

line, = ax.plot(a, m[:,0])

def animate(i):
    line.set_ydata(m[:,i])  # update the data.
    return line,

ani = animation.FuncAnimation(
    fig, animate, interval=1, blit=False, save_count=50)

plt.ylim(top=2.1, bottom=-2.1)
plt.show()