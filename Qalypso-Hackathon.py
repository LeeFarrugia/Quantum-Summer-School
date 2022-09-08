from qiskit import *
import matplotlib.pyplot as plt

# creation of teleportation circuit
c = QuantumCircuit(3, 3)
c.x(0)
c.barrier()
c.h(1)
c.cx(1,2)
c.cx(0,1)
c.h(0)
c.barrier()
c.measure([0,1], [0,1])
c.barrier()
c.cx(1,2)
c.cz(0,2)
c.draw('mpl')
plt.show()
