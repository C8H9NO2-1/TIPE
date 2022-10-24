import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


def resolutionEq2d(cube, Nt): #besoin des primitives de files + module time

    """
    cube : cube avec conditions initiales
    Nt : nombre de valeurs de temps sur lesquelles résoudre l'eq de propag de l'onde
    """

    file=[0 for _ in range(10)] #le temps moyen sera basé sur 10 itération
    temps1 = time.time()
    for t in range(1,Nt-1):
        enfiler(time.time()-temps1,file)
        defiler(file) #pour garder 10 valeurs dans la file
        print(np.mean(file)*(Nt-t)/60) #calcul du temps restant à partir des 10 val dans la file
        temps1 = time.time()
        cube[1:-1,1:-1,t+1] = 2*cube[1:-1,1:-1,t]-cube[1:-1,1:-1,t-1]+((delta_t*c)**2)*((cube[2:,1:-1,t]-2*cube[1:-1,1:-1,t]+cube[:-2,1:-1,t])/(delta_x)**2+(cube[1:-1,2:,t]-2*cube[1:-1,1:-1,t]+cube[1:-1,:-2,t])/(delta_y**2))

def condIni(Nx, Ny, r_init, xcenter, ycenter, decalX, decalY):

    """
    Nx : nombre de valeurs d'abscisse
    Ny : nombre de valeurs d'ordonnée
    r_init : rayon d'action de la fonction donnant les valeurs initiales
    xcenter : coord x du centre du cercle d'action de la fonction
    ycenter : idem en y
    decalX : décalage de l'onde initiale en x entre t=0 et t=1
    decalY : idem en y
    """
    nb_ang = int(1.5 * 2*np.pi*r_init) # calcul permetant de parcourir tous les indices sur le rayon r_init avec une "marge" de 1.5
    angles = np.linspace(0,2*np.pi,nb_ang)

    for i in range(nb_ang):
        theta = angles[i]
        for r in range(r_init+1):
            cube[int(np.cos(theta)*r)+xcenter,int(np.sin(theta)*r)+ycenter,0] = np.cos(r/(2*r_init)*np.pi)
    for x in range(1,Nx):
        for y in range(Ny):
            cube[x,y,1] = cube[x-1,y,0]

def dimQual(nouvNx, nouvNy, cube): #diminue la qualité du cube pour un affichage plus fluide

    """
    nouvNx : nombre de valeurs en x à afficher
    nouvNy : nombre de valeurs en y à afficher
    cube : cube sur lequel se baser
    """

    temp = np.zeros(nouvNx,nouvNy,len(cube[0,0,:]))
    pasX = int((Nx-2)/nouvNx) #nombre d'indices qui seront "sautés" pour donner le nouveau cube
    pasY = int((Ny-2)/nouvNy) # on prend en compte un indice tous les "pasY"
    for x in range(nouvNx):
        for y in range(nouvNy):
            temp[x,y,:] = cube[pasX * x, pasY * y,:]
    return temp


def affCube(cube, fps, frn, nbX, nbY, Xlim, Ylim, Zlim_bas, Zlim_haut):

    """
    cube : cube à afficher
    fps : nombre d'images par seconde
    frn : nombre de frames (souvent le nombre de valeurs de temps qu'on veut afficher)
    nbX : nombre de pt d'abscisse à afficher (souvent Nx)
    nbY : nombre de pt d'ordonnée à afficher (souvent Ny)
    Xlim : limite de graduation de l'axe X
    Ylim : limite de graduation de l'axe Y
    Zlim_bas : limite basse de graduation de l'axe Z
    Zlim_haut : limite haute de graduation de l'axe Z
    """

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    Xtab = np.arange(0,nbX,1)
    Xtab, Ytab = np.meshgrid(Xtab, Xtab) #crée un plan pour le plot


    def change_plot(frame_number, cube, plot):
        plot[0].remove()
        plot[0] = ax.plot_surface(Xtab, Ytab, cube[:,:,frame_number], cmap="afmhot_r")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') #apparement, ne pas s'occuper du "111"

    plot = [ax.plot_surface(Xtab, Ytab, cube[:, :, 0], color='0.75', rstride=1, cstride=1)]

    ax.set_xlabel('X-axis')
    ax.set_xlim(0, Xlim)
    ax.set_ylabel('Y-axis')
    ax.set_ylim(0, Ylim)
    ax.set_zlabel('u(x,y,t)')
    ax.set_zlim(Zlim_bas, Zlim_haut)
    ax.set_title('Onde 2D')

    ani = animation.FuncAnimation(fig, change_plot, frn, fargs=(cube, plot), interval=1000 / fps)
    plt.show()

