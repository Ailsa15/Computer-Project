import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from decimal import Decimal, getcontext
import sys

def system(state, r, l, m_u, E, a_s, b):
    u, v = state  
    dudr = v       
    dvdr = l*(l+1)*u/(r**2) - 2*m_u*(E+(4*a_s)/(3*r)-b*r) * u   
    return [dudr, dvdr]

def CalculateNodes(x,y):
    cross = 0
    for i in range(1,len(y)):
        if y[i-1]*y[i]<0:
            cross += 1
    return cross

def CalculateTurningPoints(v):
    count = 0
    for i in range(len(v)-1):
        if v[i]*v[i+1]<0:
            count += 1
    return count

def NewEnergy(b1, b2, b3, Node1, Node2, Node3, Count1, Count2, Count3):
    if Node1 == Node2 and Count1 == Count2:
        b1 = b2
        b2 = (b1 + b3)/2 
    elif Node2 == Node3 and Count2 == Count3:
        b3 = b2
        b2 = (b1 + b3)/2
    elif Node1 == Node2 == Node3 and Count1 == Count2 == Count3:
        print('Error in bisection method')
        sys.exit('End')
    return b1, b2, b3

def Solve(initial_conditions, r, l, m_u, E, a_s, b1, b2, b3):
    solution = odeint(system, initial_conditions, r, args=(l, m_u, E, a_s, b1))
    solution1 = odeint(system, initial_conditions, r, args=(l, m_u, E, a_s, b2))
    solution2 = odeint(system, initial_conditions, r, args=(l, m_u, E, a_s, b3))
    u, v = solution.T
    u1, v1 = solution1.T    
    u2, v2 = solution2.T
    return u, v, u1, v1, u2, v2

def normalisation(u, r):
    normalisation = simpson(u**2, r)
    u_normalised = u/np.sqrt(normalisation)
    u_squared = u_normalised**2
    return u_squared

#def round_sig(x, sig=3):
 #   return float(f"{x:.{sig}g}")

def round_sig_fig(x, sig=3):
    from math import log10, floor
    if x == 0:
        return f"{0:.{sig-1}f}"
    dec = sig - 1 - floor(log10(abs(x)))
    return f"{x:.{max(dec,0)}f}"
    
initial_conditions = [0, 1]
l= 0
n= 1
b1 = 0.2
b3 = 0.05
b2 = (b1 + b3)/2
#m_e=0.51099895069 
m_c = 4.70
m_u = m_c/2
#a= 1/137
a_s = 0.28
E = (9.3909+9.4603)/2-m_c-m_c
#a_0 = 1/(m_e*a)
r = np.linspace(1E-7, 15, 10000)

u, v, u1, v1, u2, v2, u_2, u_3, u_4 = np.zeros((9,3,len(r)))
u, v, u1, v1, u2, v2 = Solve(initial_conditions, r, l, m_u, E, a_s, b1, b2, b3)
u_2 = normalisation(u, r)
u_3 = normalisation(u1, r)
u_4 = normalisation(u2, r)
for i in range(100):
#while abs(b3 - b1) > 1E-8:
    u, v, u1, v1, u2, v2 = Solve(initial_conditions, r, l, m_u, E, a_s, b1, b2, b3)
    Node1 = (CalculateNodes(u, v))
    Node2 = (CalculateNodes(u1, v1))
    Node3 = (CalculateNodes(u2, v2))
    Count1 = (CalculateTurningPoints(v))
    Count2 = (CalculateTurningPoints(v1))
    Count3 = (CalculateTurningPoints(v2))
    b1, b2, b3 = NewEnergy(b1, b2, b3, Node1, Node2, Node3, Count1, Count2, Count3)
    u_2 = normalisation(u, r)
    u_3 = normalisation(u1, r)
    u_4 = normalisation(u2, r)
print(b2)   
plt.figure(figsize=(10, 5))
plt.plot(r, u, color='red')
plt.plot(r, u1, color='pink')
plt.plot(r, u2, color='purple')
#plt.plot(r, u_2, color='blue')
#plt.plot(r, u_3, color='orange')
#plt.plot(r, u_4, color='green')

#plt.savefig("Truncation.png", dpi=300, bbox_inches='tight')

plt.show()

# beta to 3.d.p = 0.195
# beta is 0.1951228877648632