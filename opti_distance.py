from scipy.integrate import odeint
import numpy as np

a= 1 #coeff de prop tau et I 
R = 34e-2
mu = 0.69
t_min = 0
t_max = 7.5
dt = 0.001

t_i = 0 #instant (indice dans la liste) à partir duquel le freinage mécanique débute

t = np.arange(t_min,t_max,dt)
def induction(I,theta_0):
    tau = a*I
    def dy(theta):
        return [theta[1], 1/tau*theta[1]]
    
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

courbe = [] #comportement final
def distance(I,F):
    global t_i, courbe
    seuil = 130 #rad.s^-1
    modele = induction(I, [300, -1/(a*I)])[0] #On commence par considérer le freinage par induction à hautes vitesse
    
    for i in  t:
        if modele[i] < seuil:
            t_i = i
            break
            
        else:
            courbe.append(modele[i])
    #on passe au freinage mécanique
    courbe += meca(F,courbe[-1])[0]
    
    #On determine la distance parcourue
    d = 0
    for i in range(len(courbe)):
        d += R*courbe[i]*dt

    return d

H = 1 #dureté du matériau
K = 1 #constante d'Archard adimensionée
def usure(t_i, F):
    """On va utiliser la loi d'Archard qui donne le volume perdu au cours du freinage
        On va sommer des petits élement de volume, correspondant au volume perdu pendant dt
        """
    global courbe
    V = 0
    for i in range(courbe[t_i:]):
        V += K*F*R*courbe[i]*dt/H

    return V

#Tracé des courbes de la distance et de l'usure en fonction de l'intensité, de la force et du seuil
