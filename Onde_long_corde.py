import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Nx = 200
Nt = 4000
delta_t = 1
delta_x = 1

c = 1


def initOnde4fronts(m):
    for i in range(10, 210):
        delta = 2*np.pi / 100
        t = i - 10
        m[0][i] = (np.sin(t * delta)) ** 2

    for i in range(11, 211):
        delta = 2*np.pi / 100
        t = i - 11
        m[1][i] = (np.sin(t * delta)) ** 2

def initRes(m):
    for i in range(0, 399):
        delta = 2*np.pi / 100
        m[0][i] = (np.sin(i * delta)) ** 2

    for i in range(1, 400):
        delta = 2*np.pi / 100
        m[1][i] = (np.sin(i * delta)) ** 2

def initDeuxRes(m):
    for i in range(0, 399):
        delta = 2*np.pi / 400
        m[0][i] = (np.sin(i * delta)) ** 2

    for i in range(1, 400):
        delta = 2*np.pi / 400
        m[1][i] = (np.sin(i * delta)) ** 2

def initUneRes(m):
    for i in range(0, 399):
        delta = 2*np.pi / 800
        m[0][i] = (np.sin(i * delta)) ** 2

    for i in range(1, 400):
        delta = 2*np.pi / 800
        m[1][i] = (np.sin(i * delta)) ** 2

def animate(i,l):
    m = l[0]
    line.set_ydata(m[:,i])  # update the data.
    return line,

#initDeuxRais()
#initRais()
#initUneRais()
#initOnde4fronts()
#initUneRais()

def resolutionEq(f):
    m = np.zeros((Nx,Nt))
    f(m)
    for  j in range(1, Nt - 1):
        for i in range(2, Nx - 1):
            m[i][j + 1] = 2 * m[i][j] - m[i][j - 1] + (c * delta_t / delta_x) ** 2 * (m[i + 1][j] - 2 * m[i][j] + m[i - 1][j])
    return m



a = np.arange(0, 200, 1)

#penser à essayer de ne pas faire avancer l'onde initiale le long de la corde mais de la multiplier par un facteur <1 pour l'amortir entre t=0 et t=1, peut être intéressant


fig, ax = plt.subplots()





#m1 = resolutionEq(initDeuxRes)
#m1 = resolutionEq(initOnde4fronts)
#m1 = resolutionEq(initUneRes)
#m1 = resolutionEq(initRes)

"""
line, = ax.flat.plot(a, m1[:,0])

ani1 = animation.FuncAnimation(
    fig, animate, interval=1, blit=False, save_count=50,fargs=(m1))

#ani2 = animation.FuncAnimation(
  #  fig, animate, interval=1, blit=False, save_count=50,fargs=(m2))

#ani3 = animation.FuncAnimation(
  #  fig, animate, interval=1, blit=False, save_count=50,fargs=(m3))

#ani4 = animation.FuncAnimation(
   # fig, animate, interval=1, blit=False, save_count=50,fargs=(m4))

"""

line, = ax.plot(a, m1[:,0])

def animate(i):
    line.set_ydata(m1[:,i])  # update the data.
    return line,

ani = animation.FuncAnimation(
    fig, animate, interval=5, blit=False, save_count=50)

plt.ylim(top=1.1, bottom=-1.1)
plt.show()

plt.ylim(top=2.1, bottom=-2.1)
plt.show()