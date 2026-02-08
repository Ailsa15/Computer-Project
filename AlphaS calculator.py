import numpy as np

n_f = 4
Lambda_QCD = 0.16  # GeV
mQ = 1.321  # GeV
mu = 2*mQ*mQ/(mQ + mQ)
a_S = 4*np.pi/((11-2/3*n_f)*np.log(mu**2/Lambda_QCD**2))
print("Alpha_s =", a_S)