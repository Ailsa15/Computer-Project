#def SolveSecondOrderDif(l,E_1, E_2, E_3):
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def system(state, r, l, m_e, E, a):
    u, v = state  
    dudr = v       
    dvdr = l*(l+1)*u/(r**2) - 2*m_e*(E+a/r) * u         
    return [dudr, dvdr]

initial_conditions = [0, 1]
r = np.linspace(0.1, 2000, 10000)
l=0
m_e=0.511

#def CalculateEnergy:
    
    

E=-13.6E-6
a= 1/137
E1 = -8E-6
E2 = -14E-6

solution = odeint(system, initial_conditions, r, args=(l, m_e, E, a))
solution1 = odeint(system, initial_conditions, r, args=(l, m_e, E1, a))
solution2 = odeint(system, initial_conditions, r, args=(l, m_e, E2, a))

u, v = solution.T
u1, v1 = solution1.T    
u2, v2 = solution2.T    

plt.figure(figsize=(10, 5))
plt.plot(r, u, label='x(t)', color='blue')
plt.plot(r, u1, label='x(t)', color='orange')
plt.plot(r, u2, label='x(t)', color='red')
#plt.plot(r, v, label='y(t)', color='orange')
plt.title('Solution of Coupled First-Order Differential Equations')
plt.xlabel('r')
plt.ylabel('Values of x and y')
plt.legend()
plt.grid()
plt.show()

