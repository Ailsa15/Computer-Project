#import numpy as np

#def SolveSecondOrderDif(l,E_1, E_2, E_3):
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def system(variables, r):
    u, v = variables  
    dudr = v  
    l=0
    m_e=511000
    E=-14
    a= 1/137       
    dvdr = l*(l+1)*u/(r**2) - 2*m_e*(E-a/r) * u         
    return [dudr, dvdr]


initial_conditions = [0, 1]

r = np.linspace(0.0000000000001, 2000, 1000)

solution = odeint(system, initial_conditions, r)

u = solution[:, 0]
v = solution[:, 1]

plt.figure(figsize=(10, 5))
plt.plot(r, u, label='x(t)', color='blue')
#plt.plot(r, v, label='y(t)', color='orange')
plt.title('Solution of Coupled First-Order Differential Equations')
plt.xlabel('Time t')
plt.ylabel('Values of x and y')
#plt.legend()
plt.grid()
plt.show()
