import numpy as np
#import matplotlib.pyplot as plt

def a(det, alpha, delta, t):
    Omega = 7.292115e-5 # Earths Angular Velocity in Rad s^-1
    if det == "H1":
        lam, gam = 0.8107054, 2.998476 # latitude and ccw from East to interferometer arm bisector in radians

    T1 = 1/16 * np.sin(2*gam) * (3 - np.cos(2*lam)) * (3 - np.cos(2*delta)) * np.cos(2 * (alpha - Omega*t))
    T2 = -1/4 * np.cos(2* gam) * np.sin(lam) * (3 - np.cos(2*delta)) * np.sin(2 * (alpha - Omega*t))
    T3 = 1/4 * np.sin(2*gam) * np.sin(2*lam) * np.sin(2*delta) * np.cos(alpha - Omega*t)
    T4 = -1/2 * np.cos(2*gam) * np.cos(lam) * np.sin(2*delta) * np.sin(alpha - Omega*t)
    T5 = 3/4 * np.sin(2*gam) * ((np.cos(lam)) ** 2) * ((np.cos(delta)) ** 2) 

    return T1 + T2 + T3 + T4 + T5



def b(det, alpha, delta, t):
    Omega = 7.292115e-5 # Earths Angular Velocity in Rad s^-1
    if det == "H1":
        lam, gam = 0.8107054, 2.998476 # latitude and ccw from East to interferometer arm bisector in radians

    T1 = np.cos(2*gam) * np.sin(lam) * np.sin(delta) * np.cos(2 * (alpha - Omega*t))
    T2 = 1/4 * np.sin(2*gam) * (3 - np.cos(2*lam)) * np.sin(delta) * np.sin(2 * (alpha - Omega*t))
    T3 = np.cos(2*gam) * np.cos(lam) * np.cos(delta) * np.cos(alpha - Omega*t)
    T4 = 1/2 * np.sin(2*gam) * np.sin(2*lam) * np.cos(delta) * np.sin(alpha - Omega*t)

    return T1 + T2 + T3 + T4


#print(a("H1", 0,0,86164.09054))
#x = np.linspace(0,86400, 1000)
#y = []
#y2 = []
#for i in range(len(x)):
##    y.append((a("H1", 0.6,0.3,x[i])))
 #   y2.append((b("H1", 0.6,0.3,x[i])))
#print(np.mean(y))
#plt.scatter(x,y)
#plt.scatter(x,y2)
#plt.grid()
#plt.show()