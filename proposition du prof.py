import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def enfiler(e,f):
    f.append(e)

def defiler(f):
    return f.pop(0)


# def resolutionEq2d(cube, Nt, delta_x, delta_y, delta_t, c): #modifie le cube passé en paramètres
#
#     """
#     cube : cube avec conditions initiales
#     Nt : nombre de valeurs de temps sur lesquelles résoudre l'eq de propag de l'onde
#     delta_x : distance entre x et x+1
#     delta_y : ditance entre y et y+1
#     delta_t : durée entre t et t+1
#     c : célérité de l'onde
#     """
#
#     file=[0 for _ in range(10)] #le temps moyen sera basé sur 10 itération
#     temps1 = time.time()
#     for t in range(1,Nt-1):
#         enfiler(time.time()-temps1,file)
#         defiler(file) #pour garder 10 valeurs dans la file
#         print(np.mean(file)*(Nt-t)/60) #calcul du temps restant à partir des 10 val dans la file
#         temps1 = time.time()
#         cube[1:-1,1:-1,t+1] = 2*cube[1:-1,1:-1,t]-cube[1:-1,1:-1,t-1]+((delta_t*c)**2)*((cube[2:,1:-1,t]-2*cube[1:-1,1:-1,t]+cube[:-2,1:-1,t])/(delta_x)**2+(cube[1:-1,2:,t]-2*cube[1:-1,1:-1,t]+cube[1:-1,:-2,t])/(delta_y**2))


def resolutionEq2d(cube, Nt, delta_x, delta_y, delta_t, c): #modifie le cube passé en paramètres

    """
    cube : cube avec conditions initiales
    Nt : nombre de valeurs de temps sur lesquelles résoudre l'eq de propag de l'onde
    delta_x : distance entre x et x+1
    delta_y : ditance entre y et y+1
    delta_t : durée entre t et t+1
    c : célérité de l'onde
    """

    file=[0 for _ in range(10)] #le temps moyen sera basé sur 10 itération
    temps1 = time.time()
    for t in range(1,Nt-1):
        enfiler(time.time()-temps1,file)
        defiler(file) #pour garder 10 valeurs dans la file
        print(np.mean(file)*(Nt-t)/60) #calcul du temps restant à partir des 10 val dans la file
        temps1 = time.time()
        cube[1:-1,1:-1,t+1] = 2*cube[1:-1,1:-1,t]-cube[1:-1,1:-1,t-1]
        # laplacien à 9 points
        laplacien=.25*cube[2:,:-2,t]+.25*cube[:-2,2:,t]+.25*cube[2:,2:,t]+.25*cube[:-2,:-2,t]
        laplacien+=.5*cube[:-2,1:-1,t]+.5*cube[2:,1:-1,t]+.5*cube[1:-1,2:,t]+.5*cube[1:-1,:-2,t]
        laplacien-=3*cube[1:-1,1:-1,t]
        cube[1:-1,1:-1,t+1]+=((delta_t*c)**2)/(delta_x)**2*laplacien



def resolutionEq2DNeumann(cube, Nt, delta_x, delta_y, delta_t, c): #modifie le cube passé en paramètres (conditions de Neumann) simule 4murs autour de l'onde

    """
    cube : cube avec conditions initiales
    mur(cube) : fonction qui impose
    Nt : nombre de valeurs de temps sur lesquelles résoudre l'eq de propag de l'onde
    delta_x : distance entre x et x+1
    delta_y : ditance entre y et y+1
    delta_t : durée entre t et t+1
    c : célérité de l'onde
    """
    Nx = len(cube[:,0,0])
    Ny = len(cube[0,:,0])

    file=[0 for _ in range(10)] #le temps moyen sera basé sur 10 itération
    temps1 = time.time()
    for t in range(1,Nt-1):
        enfiler(time.time()-temps1,file)
        defiler(file) #pour garder 10 valeurs dans la file
        if t>10: print(np.mean(file)*(Nt-t)/60) #calcul du temps restant à partir des 10 val dans la file (renvoie le temps restant en minutes)
        temps1 = time.time()
        cube[1:-1,1:-1,t+1] = 2*cube[1:-1,1:-1,t]-cube[1:-1,1:-1,t-1]+((delta_t*c)**2)*((cube[2:,1:-1,t]-2*cube[1:-1,1:-1,t]+cube[:-2,1:-1,t])/(delta_x)**2+(cube[1:-1,2:,t]-2*cube[1:-1,1:-1,t]+cube[1:-1,:-2,t])/(delta_y**2))
        for x in range(1,Nx-1): #conditions aux limites
            cube[x,1,t+1]=cube[x,2,t+1]
            cube[x,0,t+1]=cube[x,1,t+1]
            cube[x,Ny-2,t+1]=cube[x,Ny-3,t+1]
            cube[x,Ny-1,t+1]=cube[x,Ny-2,t+1]
        for y in range(1,Ny-1):
            cube[1,y,t+1]=cube[2,y,t+1]
            cube[0,y,t+1]=cube[1,y,t+1]
            cube[Nx-2,y,t+1]=cube[Nx-3,y,t+1]
            cube[Nx-1,y,t+1]=cube[Nx-2,y,t+1]

# def condIni(Nx, Ny, Nt, r_init, xcenter, ycenter, decalX, decalY): #cos**2 en 2d qui se déplace (problème de stabilité lorsque (decalX,decalY) != (1,0) )
#
#     """
#     Nx : nombre de valeurs d'abscisse
#     Ny : nombre de valeurs d'ordonnée
#     Nt : nombre de valeurs de temps
#     r_init : rayon d'action de la fonction donnant les valeurs initiales
#     xcenter : coord x du centre du cercle d'action de la fonction
#     ycenter : idem en y
#     decalX : décalage de l'onde initiale en x entre t=0 et t=1
#     decalY : idem en y
#     """
#     cube = np.zeros((Nx,Ny,Nt))
#     nb_ang = int(1.5 * 2*np.pi*r_init) # calcul permetant de parcourir tous les indices sur le rayon r_init avec une "marge" de 1.5
#     angles = np.linspace(0,2*np.pi,nb_ang)
#
#     for i in range(nb_ang):
#         theta = angles[i]
#         for r in range(r_init+1):
#             cube[int(np.cos(theta)*r)+xcenter,int(np.sin(theta)*r)+ycenter,0] = np.cos(r/(2*r_init)*np.pi)
#     for x in range(1,Nx):
#         for y in range(Ny):
#             cube[x,y,1] = cube[x-decalX,y-decalY,0] #surement un problème dans les indices
#     return cube

def condIni(Nx, Ny, Nt, r_init, xcenter1,xcenter2, ycenter1,ycenter2, decalX, decalY): #cos**2 en 2d qui se déplace (problème de stabilité lorsque (decalX,decalY) != (1,0) )

    """
    Nx : nombre de valeurs d'abscisse
    Ny : nombre de valeurs d'ordonnée
    Nt : nombre de valeurs de temps
    r_init : rayon d'action de la fonction donnant les valeurs initiales
    xcenter : coord x du centre du cercle d'action de la fonction
    ycenter : idem en y
    decalX : décalage de l'onde initiale en x entre t=0 et t=1
    decalY : idem en y
    """
    cube = np.zeros((Nx,Ny,Nt))
    for x in range(Nx):
        for y in range(Ny):
            cube[x,y,0]=np.exp(-.05*((x-xcenter1)**2+(y-ycenter1)**2))
    for x in range(Nx):
        for y in range(Ny):
            epsilon = 0.001
            if cube[x,y,0] < epsilon :
                cube[x,y,0]=np.exp(-.05*((x-xcenter2)**2+(y-ycenter2)**2))
    for x in range(1,Nx):
        for y in range(Ny):
            cube[x,y,1] = cube[x-decalX,y-decalY,0] #surement un problème dans les indices
    return cube




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

##

Nx=300
Ny=300
Nt = 1000
c = 1000
delta_t = 1
delta_x = c # pour avoir une célérité initiale cohérente (initialement, on décale d'un indice l'onde à t=0, et donc on la décale de c car delta_t = 1)
delta_y = c # ET NON PAS 1


cube = condIni(Nx,Ny,Nt,30,75,10,250,10,0,0)
resolutionEq2d(cube, Nt, delta_x, delta_y, delta_t, c)


##

cubeaff, Xtab, Ytab = dimQual(50,50,cube)
affCube(cubeaff,Xtab,Ytab,250,Nt,Nx,Ny,-0.5,1.5)











