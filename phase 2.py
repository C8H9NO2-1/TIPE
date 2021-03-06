import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

duree = 3000
N = 400
g = 9.8


t = np.linspace(0,duree,N) #tableau du temps

def Temp(y):
    def aux (y):
        if y < 11e3 : return -6.5*y*1e-3 + 15
        elif y < 20e3 : return -56.5
        elif y < 32e3 : return 1*(y - 20e3)*1e-3 - 56.5
        elif y < 47e3 : return 2.8*(y - 32e3)*1e-3 - 44.5
        elif y < 51e3 : return -2.5
        elif y < 71e3 : return -2.8*(y - 51e3)*1e-3 - 2.5
        else : return -2*(y - 71e3)*1e-3 - 58.5
    return aux(y) + 273.15

def angle_phase1(y):
    def aux(y):
        if y < 10e3: return -5 - 10 * y / 10e3
        elif y < 30e3: return - 15 - 20 * (y - 10e3) / 20e3
        elif y < 60e3: return - 35 - 40 * (y - 30e3) / 30e3
        else: return -75 - 15 * (y - 60e3) / 20e3
    return aux(y) * np.pi / 180

def calc_1 (Y,t) :

    D = 518*9 #Débit massique
    alpha = angle_phase1(Y[4])
    # print(alpha * 180 / np.pi) 
    F = 2000e3*9 #Poussée des moteurs
    
    g = 9.8
    M = 28.956e-3 #kg/mol
    R = 8.314

    #Coefficient de frottements
    r1 = 6.4 / 2
    r2 = 8.6 / 2
    S = np.pi * (r1**2 + r2**2)
    Cx = 0.02
    k = .5 * Y[5] * M / (R * Temp(Y[4])) * Cx * S


    #Y[0] => Vitesse selon x
    #Y[1] => Vitesse selon y
    #Y[2] => masse m
    #Y[3] => x
    #Y[4] => y
    #Y[5] => Pression P

    #dv => acceleration
    #dm => dérivée de la masse
    #dy => vitesse selon y
    #dx => vitesse selon x
    #dP => dérivée de la Pression

    if Y[4] > 76500 : 
    
        dvx = 0
        dvy = 0
        dm = 0
        dy = 0
        dx = 0
        dP = 0

    elif Y[2] > 307240 : #Tant qu'on a du carburant

        dvx = (-F*np.sin(alpha) - k*np.sqrt(Y[0]**2 + Y[1]**2)*Y[0])/Y[2]
        dvy = (F*np.cos(alpha) - k*np.sqrt(Y[0]**2 + Y[1]**2)*Y[1])/Y[2] - g
        dm = -D
        dy = Y[1]
        dx = Y[0]
        dP = (-Y[5] * M * g / (R * Temp(Y[4])))*Y[1]
        

    else : #Il n'y a plus de carburant
    
        dvx = -k*np.sqrt(Y[0]**2 + Y[1]**2)*Y[0]/Y[2]
        dvy = - k*np.sqrt(Y[0]**2 + Y[1]**2)*Y[1]/Y[2] - g
        dm = 0
        dy = Y[1]
        dx = Y[0]
        dP = (-Y[5] * M * g / (R * Temp(Y[4])))*Y[1]

    if Y[4] < 0 : #On touche le sol

        dvx = 0
        dvy = 0
        dm = 0
        dy = 0
        dx = 0
        dP = 0
        

    return np.array([dvx, dvy, dm, dx, dy, dP])


def crop (t,vx,vy,x,y,P) : #On redimensionne les tableaux lorsque les valeurs deviennent constantes
    for i in range (len(t)-1) :
        if int(y[i] * 100)==int(y[i+1] * 100) : return t[:i], vx[:i],vy[:i], x[:i], y[:i], P[:i]
    return t, vx, vy, x, y, P


Y0_1 = np.array([0,0,1807240,0,0,1e5]) #Conditions initiales
sol = odeint(calc_1,Y0_1,t) #résolution de(s) équa. diff.
n_1 = len(sol)

#Extraction des données
vx = np.array([sol[i][0] for i in range (n_1)])
vy = np.array([sol[i][1] for i in range (n_1)])
x = np.array ([sol[i][3] for i in range (n_1)])
y = np.array ([sol[i][4] for i in range (n_1)])
m = np.array ([sol[i][2] for i in range (n_1)])
P = np.array ([sol[i][5] for i in range (n_1)])

t,vx,vy,x,y,P = crop(t,vx,vy,x,y,P)
v = np.sqrt(vx**2+vy**2)

#!=============================================== PHASE II ===============================================

t_2 = np.linspace(t[-1],duree + t[-1],N) #tableau du temps

def angle_phase2(vy):
    def aux(vy):
        if vy > 0: return -70
        else: return -110
    return aux(vy) * np.pi / 180

Y0_2 = np.array([vx[-1],vy[-1],380e3,x[-1],y[-1],P[-1]])

def calc_2 (Y,t) :

    D = 518*2 #Débit massique
    alpha = -90 * np.pi / 180
    # print(alpha * 180 / np.pi) 
    F = 2000e3 * 2 #Poussée des moteurs
    
    g = 9.8
    M = 28.956e-3 #kg/mol
    R = 8.314
    rho_air = Y[5] * M / (R * Temp(Y[4]))
    
    # Norme de la vitesse
    v = np.sqrt(Y[0]**2 + Y[1]**2)
    
    #Coefficient de frottements
    r1 = 6.4 / 2
    r2 = 8.6 / 2
    S = np.pi * (r1**2 + r2**2)
    Cx = 0.02
    k = .5 * rho_air * Cx * S
    
    phi = np.arccos(Y[0] / v) # Angle entre le vecteur vitesse et le repère (Cf feuille d'explication)
    
    #Force de portance 
    A = 461 * np.sin(alpha - phi) #m2
    Cy = 0.1
    Fp = .5 * rho_air * A * Cy * v**2 # Portance
    # Fp = 0

    #Y[0] => Vitesse selon x
    #Y[1] => Vitesse selon y
    #Y[2] => masse m
    #Y[3] => x
    #Y[4] => y
    #Y[5] => Pression P

    #dv => acceleration
    #dm => dérivée de la masse
    #dy => vitesse selon y
    #dx => vitesse selon x
    #dP => dérivée de la Pression
    
    if Y[5] < 0: Y[5] = 0 # Si la pression est négative, on l'annule
    
    if Y[2] > 160e3:

        dvx = (-F * np.sin(alpha) - k * v * Y[0] - np.sin(phi) * Fp) / Y[2]
        dvy = (F * np.cos(alpha) - k * v * Y[1] + np.cos(phi) * Fp) / Y[2] - g
        dm = -D
        dy = Y[1]
        dx = Y[0]
        dP = (-Y[5] * M * g / (R * Temp(Y[4]))) * Y[1]
        
    else:
        
        dvx = (- k * v * Y[0] - np.sin(phi) * Fp) / Y[2]
        dvy = (- k * v * Y[1] + np.cos(phi) * Fp) / Y[2] - g
        dm = 0
        dy = Y[1]
        dx = Y[0]
        dP = (-Y[5] * M * g / (R * Temp(Y[4]))) * Y[1]
        
    if Y[4] < 0 : #On touche le sol
    
        dvx = 0
        dvy = 0
        dm = 0
        dy = 0
        dx = 0
        dP = 0


    return np.array([dvx, dvy, dm, dx, dy, dP])


sol_2 = odeint(calc_2,Y0_2,t_2) #résolution de(s) équa. diff.
n_2 = len(sol_2)

#Extraction des données
vx_2 = np.array([sol_2[i][0] for i in range (n_2)])
vy_2 = np.array([sol_2[i][1] for i in range (n_2)])
x_2 = np.array ([sol_2[i][3] for i in range (n_2)])
y_2 = np.array ([sol_2[i][4] for i in range (n_2)])
m_2 = np.array ([sol_2[i][2] for i in range (n_2)])
P_2 = np.array ([sol_2[i][5] for i in range (n_2)])

t_2,vx_2,vy_2,x_2,y_2,P_2 = crop(t_2,vx_2,vy_2,x_2,y_2,P_2)

#Tracé
plt.figure()
plt.plot(x_2, y_2)
plt.plot(x, y)
plt.ylabel('Altitude en m')
plt.xlabel('Longueur en km')
plt.grid()
plt.show()
