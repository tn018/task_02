import numpy as np
import matplotlib.pyplot as plt
import os
import requests
import re
import scipy.special as sc
import matplotlib.ticker as mt

def a(n, x):
    return sc.spherical_jn(n, x) / h(n, x) 

def b(n, x):
    return ((x * sc.spherical_jn(n - 1, x) - n * sc.spherical_jn(n, x))
            / (x * h(n - 1, x) - n * h(n, x)))
    
def h(n, x):
    return sc.spherical_jn(n, x) + 1j * sc.spherical_yn(n, x)

def RCS(D, fmin, fmax):
    c = 3e8
    r = D/2
    f = np.arange(fmin, fmax+1e6, 1e6)
    sigma, F = [], []
    for i in f:
        lambda_ = c / i
        k = 2 * np.pi / lambda_
        summa = []
        for n in range(1,110):
            summa.append((-1) ** n * (n + 0.5) * (b(n, k * r) - a(n, k * r)))
        sigma.append((lambda_ ** 2 / np.pi) * abs(sum(summa)) ** 2)
        F.append(i)
    w = open('results/task_02_4О-506C_Tyrkalov_07.txt', 'w')
    print ('f, [МГц]\tsigma, [м^2]\n', file = w)
    d = dict(zip(F, sigma))
    for key, value in d.items():
        print('{0}\t\t{1}\n'.format(key * 1e-6, value), file = w)
    w.close()
    
    plt.plot(f, sigma)
    plt.grid()
    plt.ylabel(r'$\sigma$, [$м^2$]', fontsize = 18)
    plt.xlabel('$f$, [Гц]')
    plt.show()
           
if __name__ == '__main__':
    try: os.mkdir('results')
    except OSError: pass
    r = requests.get('https://jenyay.net/uploads/Student/Modelling/task_02.txt')
    z = re.search(r'^7\..+', r.text, flags=re.M)
    z1 = (z.group().split(';'))
    D = float(z1[0].split('=')[1])
    fmin = float(z1[1].split('=')[1])
    fmax = float(z1[2].split('=')[1])
    RCS(D, fmin, fmax)
