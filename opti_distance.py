from scipy.integrate import odeint
import numpy as np

a= 1 #coeff de prop tau et I 
R = 34e-2
mu = 0.69
t_min = 0
t_max = 7.5
dt = 0.001
t = np.arange(t_min,t_max,dt)
def induction(I,theta_0):
    tau = a*I
    def dy(theta):
        return [theta[1], tau*theta[1]]
    
    def theta(t):
        res = odeint(dy, theta_0,t)
        return res
    
    return theta()
  
def meca(F,theta_0):
    def dy(theta):
        return [theta[1], -mu*F*R]
    
    def theta(t):
        res = odeint(dy, theta_0,t)
        return res
    
    return theta()

seuil = 130 #rad.s^-1
modele = induction()[0] #On commence par considérer le freinage par induction à hautes vitesse
courbe = [] #comportement final
for i in  t:
    if modele[i] < seuil:
        break
    else:
        courbe.append(modele[i])
#on passe au freinage mécanique
courbe += meca(F,courbe[-1])[0]
    
#On determine la distance parcourue
d = 0
for i in range(len(courbe)):
    d += R*courbe[i]*dt
