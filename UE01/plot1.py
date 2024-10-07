import matplotlib.pyplot as plt
import math

PI = math.pi
CNT = 1024
# CNT Werte von -pi bis pi
X = [2*PI*i/CNT - PI for i in range(CNT)]
C = [math.cos(x) for x in X]
S = [math.sin(x) for x in X]

plt.plot(X, C, label='cos(x)')
plt.plot(X, S, label='sin(x)')

plt.savefig("plot1_waldecker.png",dpi=72)
plt.show()
