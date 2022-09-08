from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute, assemble
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint
import regex as re

circuits = []
sendResults = []
receiveResults = []
results = []
sendkey = []
receivekey= []
backend = Aer.get_backend('aer_simulator')
sr_patterns = [re.compile("'..00"), re.compile("'..01"), re.compile("'..10"), re.compile("'..11")]

N = 10

# create registers
qr = QuantumRegister(2)
cr = ClassicalRegister(4)

# singlet production
singlet_state = QuantumCircuit(qr, cr, name='singlet')
singlet_state.x(qr[0])
singlet_state.x(qr[1])
singlet_state.h(qr[0])
singlet_state.cx(qr[0], qr[1])
singlet_state.barrier()

# sending measurements
s1 = QuantumCircuit(qr, cr, name='send1')
s1.h(qr[0])
s1.measure(qr[0], cr[0])
s1.barrier()

s2 = QuantumCircuit(qr, cr, name='send2')
s2.s(qr[0])
s2.h(qr[0])
s2.t(qr[0])
s2.h(qr[0])
s2.measure(qr[0], cr[0])
s2.barrier()

s3 = QuantumCircuit(qr, cr, name='send3')
s3.measure(qr[0], cr[0])
s3.barrier()

# receiver measurements
r1 = QuantumCircuit(qr, cr, name='recv1')
r1.s(qr[1])
r1.h(qr[1])
r1.t(qr[1])
r1.h(qr[1])
r1.measure(qr[1], cr[1])

r2 = QuantumCircuit(qr, cr, name='recv2')
r2.measure(qr[1], cr[1])

r3 = QuantumCircuit(qr, cr, name='recv3')
r3.s(qr[1])
r3.h(qr[1])
r3.tdg(qr[1])
r3.h(qr[1])
r3.measure(qr[1], cr[1])

sender_measurements = [s1, s2, s3]
receiver_measurements = [r1, r2, r3]

sender_choices = [np.random.randint(1, 3) for i in range(N)]
receiver_choices = [np.random.randint(1, 3) for i in range(N)]


for i in range(N):
    cN = str(i) + ':S' + str(sender_choices[i]) + '_R'
    sub_circ = singlet_state.compose(sender_measurements[sender_choices[i]-1]).compose(receiver_measurements[receiver_choices[i]-1])
    circuits.append(cN)
    result = execute(sub_circ, backend=backend, shots=1, memory=True).result()
    results.append(result.get_counts())

for i in range(N):
    rescheck = results[i]
    if sr_patterns[0].search(str(rescheck)):
        sendResults.append(-1)
        receiveResults.append(-1)
    if sr_patterns[1].search(str(rescheck)):
        sendResults.append(1)
        receiveResults.append(-1)
    if sr_patterns[2].search(str(rescheck)):
        sendResults.append(-1)
        receiveResults.append(1)
    if sr_patterns[3].search(str(rescheck)):
        sendResults.append(-1)
        receiveResults.append(-1)

for i in range(N):
    if (sender_choices[i] == 2 and receiver_choices[i] == 1) or (sender_choices[i] == 3 and receiver_choices[i] == 2):
        sendkey.append(sendResults[i])
        receivekey.append(- receiveResults[i])

keylength = len(sendkey)

srkeymiss = 0
for j in range(keylength):
    if sendkey[j] != receivekey[j]:
        srkeymiss += 1

def chsh_corr_value(x):
    countA1B1 = [0, 0, 0, 0] 
    countA1B3 = [0, 0, 0, 0] 
    countA3B1 = [0, 0, 0, 0] 
    countA3B3 = [0, 0, 0, 0] 
    for i in range(N):
        rescheck = x[i]
        if (sender_choices[i] == 1 and receiver_choices[i] == 1):
            for j in range(4):
                if sr_patterns[j].search(str(rescheck)):
                    countA1B1[j] += 1
        if (sender_choices[i] == 1 and receiver_choices[i] == 3):
            for j in range(4):
                if sr_patterns[j].search(str(rescheck)):
                    countA1B3[j] += 1
        if (sender_choices[i] == 3 and receiver_choices[i] == 1):
            for j in range(4):
                if sr_patterns[j].search(str(rescheck)):
                    countA3B1[j] += 1
        if (sender_choices[i] == 3 and receiver_choices[i] == 3):
            for j in range(4):
                if sr_patterns[j].search(str(rescheck)):
                    countA3B3[j] += 1
    total11 = sum(countA1B1)
    total13 = sum(countA1B3)
    total31 = sum(countA3B1)
    total33 = sum(countA3B3)
    expect11 = (countA1B1[0] - countA1B1[1] - countA1B1[2] + countA1B1[3])/total11
    expect13 = (countA1B3[0] - countA1B3[1] - countA1B3[2] + countA1B3[3])/total13
    expect31 = (countA3B1[0] - countA3B1[1] - countA3B1[2] + countA3B1[3])/total31
    expect33 = (countA3B3[0] - countA3B3[1] - countA3B3[2] + countA3B3[3])/total33
    
    corr = expect11 - expect13 + expect31 + expect33
    
    return corr

print(results)
corr = chsh_corr_value(results)
print(round(corr,3))