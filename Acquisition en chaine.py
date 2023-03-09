import pycanum.main as pyc
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.optimize

sys = pyc.Sysam("SP5")

delta_i = 400

f = 400
Te = 1/(f * delta_i)

t = np.linspace(0, 1/f, delta_i + 1)
Amp1 = 5
Amp2 = 5
signal1 = np.array([Amp1 * np.sin(i / delta_i * 2 * np.pi) for i in range(delta_i + 1)])

Te_entree = 1 / (1000 * f) # periode d'echantillonage des entrees
nb_points = 50000

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    # tt = np.array(tt)
    # yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

def valeur_signal_primaire():
    pyc.Sysam.config_sortie(sys, 1, Te * 10**6, signal1, -1)
    
    pyc.Sysam.config_entrees(sys, [0], [0.4])
    pyc.Sysam.config_echantillon(sys, Te_entree * 10**6, nb_points)
    
    amplitudes = []
    frequences = []
    
    for _ in range(10):
        pyc.Sysam.declencher_sorties(sys, 1, 0)
        
        time.sleep(2/340) # Le temps que le signal atteigne le bout du tuyau
        
        pyc.Sysam.acquerir(sys)
        temps = pyc.Sysam.temps(sys)
        tensions = pyc.Sysam.entrees(sys)
        
        temp = temps[0]
        tension = tensions[0]
        temp = temp[:nb_points - int(0.02 / Te_entree)]
        tension = tension[int(0.02 / Te_entree):]
        
        regression = fit_sin(temp, tension)
        
        amplitudes.append(abs(regression["amp"]))
        frequences.append(regression["freq"])
        
        pyc.Sysam.stopper_sorties(sys, 1, 1)

    amplitudes = np.array(amplitudes)
    frequences = np.array(frequences)
    amp_mean = np.mean(amplitudes)
    freq_mean = np.mean(frequences)
    amp_std = np.std(amplitudes)
    freq_std = np.std(frequences)
    
    print("amp_mean: ", amp_mean, "\n", "freq_mean: ", freq_mean, "\n", "amp_std: ", amp_std, "\n", "freq_std: ", freq_std, "\n")
    
    array = np.array([amp_mean, freq_mean, amp_std, freq_std])
    np.save("signal primaire.npy", array)
    
# valeur_signal_primaire()
signal_primaire = np.load("signal primaire.npy")

def test_phases(tab_phases):
    tab_amp = []
    
    pyc.Sysam.config_sortie(sys, 1, Te * 10**6, signal1, -1)
    
    pyc.Sysam.config_entrees(sys, [0], [1])
    pyc.Sysam.config_echantillon(sys, Te_entree * 10**6, nb_points)
    
    for phase in tab_phases:
        phase *= np.pi/180
        signal2 = np.array([Amp2 * np.sin(i / delta_i * 2 * np.pi + phase) for i in range(delta_i + 1)])
        pyc.Sysam.config_sortie(sys, 2, Te * 10**6, signal2, -1)
        
        pyc.Sysam.declencher_sorties(sys, 1, 1)

        time.sleep(2/340) # Le temps que le signal atteigne le bout du tuyau
        
        pyc.Sysam.acquerir(sys)

        temps = pyc.Sysam.temps(sys)
        tensions = pyc.Sysam.entrees(sys)

        temp2 = temps[0]
        tension2 = tensions[0]
        
        pyc.Sysam.stopper_sorties(sys, 1, 1)
        
        regression = fit_sin(temp2, tension2)
        amp = abs(regression["amp"])
        tab_amp.append(amp)
        
    return tab_amp

def test_amplitudes(phi, tab_amp):
    tab_theo = []
    tab_pratique = []
    
    phi *= np.pi / 180
    
    pyc.Sysam.config_entrees(sys, [0], [1])
    pyc.Sysam.config_echantillon(sys, Te_entree * 10**6, nb_points)

    amp1 = signal_primaire[0]
        
    for a2 in tab_amp:
        
        tab_theo.append(a2)
        
        phi *= np.pi/180
        signal2 = np.array([a2 * np.sin(i / delta_i * 2 * np.pi + phi) for i in range(delta_i + 1)])
        pyc.Sysam.config_sortie(sys, 1, Te * 10**6, signal2, -1)
        
        pyc.Sysam.declencher_sorties(sys, 1, 0)

        time.sleep(2/340) # Le temps que le signal atteigne le bout du tuyau
    
        pyc.Sysam.acquerir(sys)
    
        temps = pyc.Sysam.temps(sys)
        tensions = pyc.Sysam.entrees(sys)

        temp2 = temps[0]
        tension2 = tensions[0]
        
        pyc.Sysam.stopper_sorties(sys, 1, 1)
    
        regression = fit_sin(temp2, tension2)
        amp2 = abs(regression["amp"])
        
        tab_pratique.append(amp2 / amp1)
    
    return tab_theo, tab_pratique
            
            
            








# phases = [i/10 for i in range(200, 410)]
# amps = test_phases(phases)
# amps /= signal_primaire[0]
x, y = test_amplitudes(30, [])

plt.figure()
plt.plot(x, y, marker  = "x", ls = 'none')
plt.show()
