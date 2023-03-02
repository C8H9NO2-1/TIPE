import numpy as np
import matplotlib.pyplot as plt

delta_i = 1000 # The number of points in our table
f = 300 # The frequency of the signal
Te = 1/(f*delta_i) # The sampling period

dephasage = 180 # The phase shift of the secondary signal
dephasage *= (np.pi / 180)

signal1 = np.array([np.sin(2 * np.pi * i / delta_i) for i in range(delta_i + 1)]) # The primary signal to be sent
signal2 = np.array([np.sin(2 * np.pi * i / delta_i + dephasage) for i in range(delta_i + 1)]) # The secondary signal to be sent

t = np.arange(256)
test = np.sin(t)
# test = abs(np.fft.fft(signal1)) # The FFT of the primary signal
# test2 = np.fft.fft(signal2, 1000) # The FFT of the secondary signal



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





plt.figure()
plt.plot(fit_sin(t, test)["fitfunc"])
plt.show()