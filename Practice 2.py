import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.integrate import simpson

def system(state, r, l, m_e, E, a, n):
    u, v = state  
    dudr = v       
    dvdr = l*(l+1)*u/(r**2) - 2*m_e*(E+a/r) * u   
    return [dudr, dvdr]

def CalculateEnergy(n):
    E1 = -1.36E-5/n**2+2E-7
    E3 = -1.36E-5/n**2-2E-7
    E2 = (E1 + E3)/2
    return E1, E2, E3

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

def NewEnergy(E1, E2, E3, Node1, Node2, Node3, Count1, Count2, Count3):
    if Node1 == Node2 and Count1 == Count2:
        E1 = E2
        E2 = (E1 + E3)/2 
    else:
        E3 = E2
        E2 = (E1 + E3)/2
    return E1, E2, E3

def Solve(initial_conditions, r, l, m_e, E1, E2, E3, a, n):
    solution = odeint(system, initial_conditions, r, args=(l, m_e, E1, a, n))
    solution1 = odeint(system, initial_conditions, r, args=(l, m_e, E2, a, n))
    solution2 = odeint(system, initial_conditions, r, args=(l, m_e, E3, a, n))
    u, v = solution.T
    u1, v1 = solution1.T    
    u2, v2 = solution2.T
    return u, v, u1, v1, u2, v2

def normalisation(u, r):
    normalisation = simpson(u**2, r)
    u_normalised = u/np.sqrt(normalisation)
    u_squared = u_normalised**2
    return u_squared

    
initial_conditions = [0, 1]
r = np.linspace(0.1, 5000, 1000)
l=1
n=2
m_e=0.511  
a= 1/137
E1, E2, E3 = CalculateEnergy(n) 

while abs(E3 - E1) > 1E-15:
    u, v, u1, v1, u2, v2 = Solve(initial_conditions, r, l, m_e, E1, E2, E3, a, n)
    Node1 = (CalculateNodes(u, v))
    Node2 = (CalculateNodes(u1, v1))
    Node3 = (CalculateNodes(u2, v2))
    Count1 = (CalculateTurningPoints(v))
    Count2 = (CalculateTurningPoints(v1))
    Count3 = (CalculateTurningPoints(v2))
    E1, E2, E3 = NewEnergy(E1, E2, E3, Node1, Node2, Node3, Count1, Count2, Count3)
    
print(E2)
u_2 = normalisation(u, r)
u_3 = normalisation(u1, r)
u_4 = normalisation(u2, r)

plt.figure(figsize=(10, 5))
plt.plot(r, u_2, label='x(t)', color='blue')
plt.plot(r, u_3, label='x(t)', color='orange')
plt.plot(r, u_4, label='x(t)', color='red')
plt.xlabel('r')
plt.ylabel('|U_nl(r)|^2')
plt.grid()
plt.show()