import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from sympy import symbols, diff, solve

def system(state, r, l, m_e, E, a, n):
    u, v = state  
    dudr = v       
    dvdr = l*(l+1)*u/(r**2) - 2*m_e*(E+a/r) * u   
    #dvdr = l*(l+1)*u/(r**2) - 2*m_e*(E-(2*270*n**2*E)/r) * u        
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

def normalisation:
    
    
initial_conditions = [0, 1]
r = np.linspace(0.1, 5000, 1000)
l=0
n=2
m_e=0.511  

#Need to calculate energy for different n values and then imput limits based on that.

E1= -3.6E-6
a= 1/137
E3 = -3.2E-6
E2 = (E1+E3)/2

for i in range(100):
    u, v, u1, v1, u2, v2 = Solve(initial_conditions, r, l, m_e, E1, E2, E3, a, n)
    Node1 = (CalculateNodes(u, v))
    Node2 = (CalculateNodes(u1, v1))
    Node3 = (CalculateNodes(u2, v2))
    Count1 = (CalculateTurningPoints(v))
    Count2 = (CalculateTurningPoints(v1))
    Count3 = (CalculateTurningPoints(v2))
    E1, E2, E3 = NewEnergy(E1, E2, E3, Node1, Node2, Node3, Count1, Count2, Count3)
    
print(E2)
print(Count1, Count2, Count3)

plt.figure(figsize=(10, 5))
plt.plot(r, u, label='x(t)', color='blue')
plt.plot(r, u1, label='x(t)', color='orange')
plt.plot(r, u2, label='x(t)', color='red')
#plt.plot(r, v, label='y(t)', color='orange')
plt.title('Solution of Coupled First-Order Differential Equations')
plt.xlabel('r')
plt.ylabel('Values of x and y')
#plt.legend()
plt.grid()
plt.show()

#Need to add number of nodes. For l=0 the number of nodes and turning points should be n-1 and n respectively. 