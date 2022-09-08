from qiskit import *
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint

n = 1
s_bits = randint(2, size=n)
s_bases = randint(2, size=n)

# creation of teleportation circuit
def sending_message(bits, bases):
    message = []
    for i in range(n):
        c = QuantumCircuit(3, 3)
        if bases[i] == 0:
            if bits[i] == 0:
                pass
            else:
                c.x(0)
        else:
            if bits[i] == 0:
                    c.h(1)
            else:
                c.cx(1,2)
                c.cx(0,1)
        c.barrier()
        message.append(c)
    return message

print(sending_message(s_bits, s_bases))

