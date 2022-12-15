import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

#!=================================================================================================
def affCube(cube, Xtab, Ytab, fps, frn, Xlim, Ylim, Zlim_bas, Zlim_haut): #affiche le cube entré en paramètres

    """
    cube : cube à afficher
    Xtab : tableau des abscisses (l'indice i de Xtab correspond à l'abscisse du point "cube[i,:,t]" avec t quelconque)
    Ytab : idem avec l'ordonnée
    fps : nombre d'images par seconde
    frn : nombre de frames (souvent le nombre de valeurs de temps qu'on veut afficher)
    Xlim : limite de graduation de l'axe X
    Ylim : limite de graduation de l'axe Y
    Zlim_bas : limite basse de graduation de l'axe Z
    Zlim_haut : limite haute de graduation de l'axe Z
    """

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    def change_plot(frame_number, cube, plot):
        plot[0].remove()
        plot[0] = ax.plot_surface(Xtab, Ytab, cube[:,:,frame_number], cmap="Blues") #

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') #apparement, ne pas s'occuper du "111"

    plot = [ax.plot_surface(Xtab, Ytab, cube[:, :, 0], color='0.75', rstride=1, cstride=1, cmap='viridis', edgecolor='none')]

    ax.set_xlabel('X-axis')
    ax.set_xlim(0, Xlim)
    ax.set_ylabel('Y-axis')
    ax.set_ylim(0, Ylim)
    ax.set_zlabel('u(x,y,t)')
    ax.set_zlim(Zlim_bas, Zlim_haut)
    ax.set_title('Onde 2D')

    ani = animation.FuncAnimation(fig, change_plot, frn, fargs=(cube, plot), interval=1000 / fps)
    plt.show()
    
def dimQual(nouvNx, nouvNy, cube): #diminue la qualité du cube pour un affichage plus fluide, renvoie un nouveau cube et les coordonnées associées à chaque point (le point cube[x,y,t] a pour coordonnées (Xtab[x],Ytab[y],cube[x,y,t]) dans le repère (O,Ox,Oy,Oz)

    """
    nouvNx : nombre de valeurs en x à afficher
    nouvNy : nombre de valeurs en y à afficher
    cube : cube sur lequel se baser
    """

    Nx = len(cube[:,0,0])
    Ny = len(cube[0,:,0])

    temp = np.zeros((nouvNx,nouvNy,len(cube[0,0,:])))

    Xtab = np.linspace(0,Nx-1,nouvNx,dtype = "int")
    Ytab = np.linspace(0,Ny-1,nouvNy,dtype = "int")
    print(Xtab[0])
    for x in range(nouvNx):
        for y in range(nouvNy):
            temp[x,y,:] = cube[Xtab[x], Ytab[y],:]
    Xtab, Ytab = np.meshgrid(Xtab,Ytab)
    return temp, Xtab, Ytab

def enfiler(e,f):
    f.append(e)

def defiler(f):
    return f.pop(0)

#!=================================================================================================

Nx = 1000
Ny = 1000
Nt = 250

c = 5
f0 = 5e-2
f1 = 5e-2

omega0 = 2 * np.pi * f0
omega1 = 2 * np.pi * f1
A0 = 1
A1 = 1
k0 = omega0 / c
k1 = omega1 / c
lambda0 = c / f0


x0 = 150
y0 = 0
h = 150
epsilon = 0.01

M = np.zeros((Nx, Ny, Nt))

# file = [0 for _ in range(10)] #le temps moyen sera basé sur 10 itération
# temps1 = time.time()

# for t in range(Nt):
#     enfiler(time.time()-temps1,file)
#     defiler(file) #pour garder 10 valeurs dans la file
#     print(np.mean(file)*(Nt-t)/60) #calcul du temps restant à partir des 10 val dans la file
#     temps1 = time.time()
    
#     for x in range(0, Nx):
#         for y in range(h):
#             if x <= c * t:
#                 M[x][y][t] = A1 * np.cos(omega1 * t - k1 * x)
            
#     for x in range(max(0, x0 - c * t), min(Nx, x0 + c * t)):
#         for y in range(min(c * t, int(A0 / epsilon))):
#             r = np.sqrt((x0 - x)**2 + (y0 - y)**2)
#             if r <= c * t and r != 0:
#                 alpha = y // h
#                 if alpha % 2 == 0:
#                     M[x][y - alpha * h][t] += A0 * np.cos(omega0 * t - k0 * r) / r
#                 else:
#                     M[x][(1 + alpha) * h - y][t] += A0 * np.cos(omega0 * t - k0 * r) / r
                


# cubeaff, Xtab, Ytab = dimQual(50,50,M)
# affCube(cubeaff,Xtab,Ytab,250,Nt,Nx,Ny,-0.5,1.5)

#!=================================================================================================
#? Code permettant de déterminer une approximation de l'atténuation

# file = [0 for _ in range(10)] #le temps moyen sera basé sur 10 itération
# temps1 = time.time()
# for t in range(Nt - 1, Nt):
#     enfiler(time.time()-temps1,file)
#     defiler(file) #pour garder 10 valeurs dans la file
#     # print(np.mean(file)*(Nt-t)/60) #calcul du temps restant à partir des 10 val dans la file
#     temps1 = time.time()
    
#     for x in range(Nx - int(lambda0) - 1, Nx):
#         for y in range(h):
#             if x <= c * t:
#                 M[x][y][t] = A1 * np.cos(omega1 * t - k1 * x)
            
#     for x in range(max(0, x0 - c * t), min(Nx, x0 + c * t)):
#         for y in range(min(c * t, int(A0 / epsilon))):
#             r = np.sqrt((x0 - x)**2 + (y0 - y)**2)
#             if r <= c * t and r != 0:
#                 alpha = y // h
#                 if alpha % 2 == 0:
#                     M[x][y - alpha * h][t] += A0 * np.cos(omega0 * t - k0 * r) / r
#                 else:
#                     M[x][(1 + alpha) * h - y][t] += A0 * np.cos(omega0 * t - k0 * r) / r

# t = Nt - 1
# mean = 0
# m = 0

# for y in range(150):
#     for x in range(Nx - int(lambda0) - 1, Nx):
#         if M[x][y][t] > m:
#             m = M[x][y][t]
#     mean += m

# print(mean / 150 / A1)

#!=================================================================================================
#? Code permettant de déterminer le déphasage optimal

I = np.linspace(0, Nx, Nx)
rapports = np.zeros(Nx)

for i in range(100):
    file = [0 for _ in range(10)] #le temps moyen sera basé sur 10 itération
    temps1 = time.time()
    for t in range(Nt - 1, Nt):
        enfiler(time.time()-temps1,file)
        defiler(file) #pour garder 10 valeurs dans la file
        # print(np.mean(file)*(Nt-t)/60) #calcul du temps restant à partir des 10 val dans la file
        temps1 = time.time()
        
        for x in range(Nx - int(lambda0) - 1, Nx):
            for y in range(h):
                if x <= c * t:
                    M[x][y][t] = A1 * np.cos(omega1 * t - k1 * x)
                
        for x in range(Nx - int(lambda0) - 1, Nx):
            for y in range(min(c * t, int(A0 / epsilon))):
                r = np.sqrt((x0 - x)**2 + (y0 - y)**2)
                if r <= c * t and r != 0:
                    alpha = y // h
                    value = A0 * np.cos(omega0 * t - k0 * r + i / 100 * np.pi) / r
                    if alpha % 2 == 0:
                        M[x][y - alpha * h][t] += value
                    else:
                        M[x][(1 + alpha) * h - y][t] += value

    t = Nt - 1
    mean = 0
    m = 0

    for y in range(150):
        for x in range(Nx - int(lambda0) - 1, Nx):
            if M[x][y][t] > m:
                m = M[x][y][t]
        mean += m
        
    rapports[i] = mean / 150 / A1

plt.plot(I, rapports)
plt.show()

#!=================================================================================================