import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

filename = './data/ws50cm-history.csv'

f = open(filename,'r')

t = []
mx = []
mn = []
anisotropyRatio = []

for line in f:
    items = line.split(',')
    t.append(float(items[0]))
    mx.append(float(items[1]))
    mn.append(float(items[2]))
    anisotropyRatio.append(mx[-1]/mn[-1])


f.close()



plt.rc('grid', c='0.5', ls='-', lw=0.25)
plt.rc('lines', lw=2, color='g')

plt.fill([0.0]+t+[24.], [0.0]+anisotropyRatio+[0.0], 'r', alpha=0.25)
plt.plot(t, anisotropyRatio, '-.r')
plt.plot(t, mx, '-b')
plt.plot(t, mn, '--g')
ax = list(plt.axis())
ax[0] = 0.0
ax[1] = 24.0
ax[2] = 0.0
plt.axis(ax)
#plt.xticks(range(25), ['00:00', '', '', '', '', '', '06:00', '', '', '', '', '', '12:00', '', '', '', '', '', '18:00', '', '', '', '', '', '24:00'])
plt.xticks([0,6,12,18,24], ['00:00', '06:00', '12:00', '18:00', '24:00'])
plt.minorticks_on()
ax = plt.gca()
ax.xaxis.set_minor_locator(MultipleLocator(1))
plt.legend(('anisotropy ratio [1]', 'max driving stress [MPa]', 'min driving stress [MPa]'))
plt.grid(True, which='major', axis='x')
plt.grid(True, which='minor', axis='x')
plt.grid(True, which='major', axis='y')

plt.savefig(filename[:-3]+'png', dpi=300)
