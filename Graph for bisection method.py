import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def system(state, r, l, m_e, E, a):
    u, v = state  
    dudr = v       
    dvdr = l*(l+1)*u/(r**2) - 2*m_e*(E+a/r) * u         
    return [dudr, dvdr]

#colours = [
 #   "#1E780C",  # deep royal purple
 #   "#77269A",  # vibrant violet
 #   "#B7A3C2",  # light lavender purple
 #   "#AB6DC6"   # pale lilac highlight




initial_conditions = [0, 1]
r = np.linspace(0.1, 2000, 10000)
r1 = np.linspace(0.1, 1550, 10000)
r2 = np.linspace(0.1, 1600, 10000)
l=0
m_e=0.511
  
E=-11E-6
a= 1/137
E1 = -8E-6
E2 = -14E-6
E3 = -13.6E-6

solution = odeint(system, initial_conditions, r2, args=(l, m_e, E, a))
solution1 = odeint(system, initial_conditions, r1, args=(l, m_e, E1, a))
solution2 = odeint(system, initial_conditions, r, args=(l, m_e, E2, a))
solution3 = odeint(system, initial_conditions, r, args=(l, m_e, E3, a))

u, v = solution.T
u1, v1 = solution1.T    
u2, v2 = solution2.T 
u3, v3 = solution3.T   

plt.figure(figsize=(10, 5))
plt.plot(r, u3, label=f"E = E$_{0}$", color='purple')
plt.plot(r, u2, label=f"E = E$_{1}$", color='orange')
plt.plot(r2, u, label=f"E = E$_{2}$", color='red')
plt.plot(r1, u1, label=f"E = E$_{3}$", color='blue')

plt.xlabel('r')
plt.ylabel('U(r)')
plt.legend()
#plt.xlim(0, 2000)
#plt.ylim(-300,300)
plt.xticks(np.arange(0, 2001, 200))

#plt.axhline(0, color='black', linewidth=1)  # horizontal axis line
#plt.axvline(0, color='black', linewidth=1)  
ax = plt.gca()
ax.spines['bottom'].set_position('zero')
ax.spines['bottom_line'] = ax.spines['bottom']  # keep bottom spine reference
ax.axhline(y=ax.get_ylim()[0], color='black', linewidth=2)
# Move x-axis ticks/spine to y=0
#ax.spines['bottom'].set_position(('data', 0))
#ax.spines['top'].set_visible(True)
#ax.spines['bottom'].set_visible(True)

# Optional: make y-axis look clean
#ax.spines['right'].set_visible(True)

plt.savefig("Bisection.png", dpi=300, bbox_inches='tight')

plt.show()
