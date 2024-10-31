"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "3.0"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "Ready to Review"
"""
import matplotlib.pyplot as plt
import math

PI = math.pi
CNT = 1024
# CNT Werte von -pi bis pi
X = [2 * PI * i / CNT - PI for i in range(CNT)]
C = [math.cos(x) for x in X]
S = [math.sin(x) for x in X]

plt.figure(figsize=(10, 6), dpi=80)
# Ändere die Linienfarbe und den Linienstil
plt.plot(X, C, color="green", linewidth=2.5, linestyle="--", label="Cosinus")
plt.plot(X, S, color="orange", linewidth=2.5, linestyle="-.", label="Sinus")

plt.legend(loc='upper left', frameon=False)

plt.xticks([-PI, -PI / 2, 0, PI / 2, PI], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
plt.yticks([-1, 0, 1], [r'$-1$', r'$0$', r'$+1$'])

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_bounds(min(X), max(X))
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))
ax.spines['left'].set_bounds(-1, 1)

ax.annotate('', xy=(1.20*max(X), 0), xytext=(1.20*min(X), 0),
                arrowprops=dict(arrowstyle='-|>,head_width=0.4,head_length=0.8', color='black', lw=4))
ax.annotate('', xy=(0, 1.2), xytext=(0, -1.2),
                arrowprops=dict(arrowstyle='-|>,head_width=0.4,head_length=0.8', color='black', lw=4))

t = 2 * PI / 3
plt.plot([t, t], [0, math.sin(t)], color='orange', linewidth=2.5, linestyle="--")
plt.scatter([t], [math.sin(t)], 50, color='orange')
plt.annotate(r'$\sin\left(\frac{2\pi}{3}\right)=\frac{\sqrt{3}}{2}$',
             xy=(t, math.sin(t)), xycoords='data', xytext=(+10, +30), textcoords='offset points',
             fontsize=16, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

plt.plot([t, t], [0, math.cos(t)], color='green', linewidth=2.5, linestyle="--")
plt.scatter([t], [math.cos(t)], 50, color='green')
plt.annotate(r'$\cos\left(\frac{2\pi}{3}\right) = -\frac{1}{2}$',
             xy=(t, math.cos(t)), xycoords='data', xytext=(-90, -50), textcoords='offset points',
             fontsize=16, arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

plt.title('Plot von Paul Waldecker', fontsize=20)

#plt.annotate('', xy=(PI, 0), xytext=(-PI, 0), arrowprops=dict(arrowstyle='->', color='black'))
#plt.annotate('', xy=(0, 1), xytext=(0, -1), arrowprops=dict(arrowstyle='->', color='black'))

plt.xlim(min(X) * 1.2, max(X) * 1.2)
plt.ylim(-1.2, 1.2)

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(16)
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65))

ax.set_axisbelow(True)

plt.savefig("plot1_waldecker.png", dpi=72)
plt.show()