import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def resolutionEq2d(cube, Nt, delta_x, delta_y, delta_t, c, cube2): #modifie le cube passé en paramètres

    """
    cube : cube avec conditions initiales
    Nt : nombre de valeurs de temps sur lesquelles résoudre l'eq de propag de l'onde
    delta_x : distance entre x et x+1
    delta_y : ditance entre y et y+1
    delta_t : durée entre t et t+1
    c : célérité de l'onde
    """
    
    for t in range(1,Nt-1):
        cube[1:-1,1:-1,(t+1) % 3] = 2*cube[1:-1,1:-1,t % 3]-cube[1:-1,1:-1,(t-1) % 3]
        # laplacien à 5 points
        laplacien += cube[:-2,1:-1,t % 3]+cube[2:,1:-1,t % 3]+cube[1:-1,2:,t % 3]+cube[1:-1,:-2,t % 3]
        laplacien -= 4*cube[1:-1,1:-1,t % 3]
        
        cube[1:-1,1:-1,(t+1) % 3]+=((delta_t*c)**2)/(delta_x)**2*laplacien
        
        if t % 20 == 0:
            cubeaff, _, _ = dimQual(100, 100,cube)
            cube2[:, :, t // 20] = cubeaff[:, :, t % 3]

def condIni(Nx, Ny, Nt, r_init, xcenter1,xcenter2, ycenter1,ycenter2, decalX, decalY):

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
    delta_x = 1000
    delta_y = 1000
    k = 1e-4 / 3
    for x in range(Nx):
        for y in range(Ny):
            cube[x, y, 0] = np.cos(- k * np.sqrt(((x - xcenter1) * delta_x)**2 + ((y - ycenter1) * delta_y)**2)) * np.exp(-.00005*((x-xcenter1)**2+(y-ycenter1)**2))
    for x in range(Nx):
        for y in range(Ny):
            phase = 0 * np.pi / 180
            cube[x, y, 0] += np.cos(- k * np.sqrt(((x - xcenter2) * delta_x)**2 + ((y - ycenter2) * delta_y)**2) + phase) * np.exp(-.00005*((x-xcenter2)**2+(y-ycenter2)**2))
    for x in range(1,Nx):
        for y in range(Ny):
            cube[x,y,1] = cube[x-decalX,y-decalY,0]
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

##

Nx = 2000
Ny = 2000
Nt = 500
c = 1000
delta_t = 1
delta_x = c # pour avoir une célérité initiale cohérente (initialement, on décale d'un indice l'onde à t=0, et donc on la décale de c car delta_t = 1)
delta_y = c # ET NON PAS 1


cube = condIni(Nx,Ny,Nt,30,Nx//2,Ny//2,Nx//2 - 200,Ny//2 + 200,0,0)

n = 500 // 20
qual = 100
cube2 = np.zeros((qual, qual, n))

cubeaff, Xtab, Ytab = dimQual(qual, qual,cube)

cube2[:, :, 0] = cubeaff[:, :, 0]

resolutionEq2d(cube, Nt, delta_x, delta_y, delta_t, c, cube2)

#! Curseur
fig = plt.figure()
plt.subplots_adjust(bottom=0.25)                

Z = cube2       

ax2 = fig.add_subplot(projection='3d')

l=ax2.plot_surface(Xtab,Ytab,Z[:, :, 0],cmap='viridis',rstride=2, cstride=2)
ax2.set_zlim(-1,1)

axtemps = fig.add_axes([0.2, 0.1, 0.65, 0.03])
stemps = Slider(axtemps, "Time [s]", 0, Nt - 1, valinit = 0, valstep=20)

def update(val): 
    t = int(val) 
    ax2.clear()
    l=ax2.plot_surface(Xtab,Ytab,Z[:, :, t // 20], cmap='viridis', rstride=2, cstride=2)
    ax2.set_zlim(-1,1)
    fig.canvas.draw_idle() 

stemps.on_changed(update)
ax2.set_zlim(0,10)

plt.show()












