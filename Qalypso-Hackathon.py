from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from numpy.random import randint
import matplotlib.pyplot as plt
import regex as re
from random_word import RandomWords

# initialise the empty lists to be used later on
circuits = []
sendResults = []
receiveResults = []
results = []
sendkey = []
receivekey= []
recieve_message_list = []
end_msg_list = []
# calling qiskit backend for simulator
backend = Aer.get_backend('aer_simulator')
# dictionary for regex patterns
sr_patterns = [re.compile("'..00"), re.compile("'..01"), re.compile("'..10"), re.compile("'..11")]

# generating the random word and turning it into binary
r = RandomWords()
msg = str(r.get_random_word())
binary_encoded_message = [bin(ord(x))[2:].zfill(8) for x in msg]

N = len(binary_encoded_message)

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

# list for all measurements
sender_measurements = [s1, s2, s3]
receiver_measurements = [r1, r2, r3]

# random selection of measurement bases
sender_choices = [randint(1, 4) for i in range(N)]
receiver_choices = [randint(1, 4) for i in range(N)]

# getting the result for the measurement bases for both sender and receiver
for i in range(N):
    cN = str(i) + ':S' + str(sender_choices[i]) + '_R'
    sub_circ = singlet_state.compose(sender_measurements[sender_choices[i]-1]).compose(receiver_measurements[receiver_choices[i]-1])
    circuits.append(cN)
    result = execute(sub_circ, backend=backend, shots=1, memory=True).result()
    results.append(result.get_counts())
    sub_circ.draw('mpl')
    plt.savefig('Circuits.pdf')
    print(sub_circ)

# comparing the regex to the result list to compute matching or not
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

# if tey select the correct bases this creates a one time pad for them communicate and send data
for i in range(N):
    if (sender_choices[i] == 2 and receiver_choices[i] == 1) or (sender_choices[i] == 3 and receiver_choices[i] == 2):
        sendkey.append(sendResults[i])
        receivekey.append(- receiveResults[i])
        for j in range(N):
            end_msg_list.append(int(binary_encoded_message[j]))

# printing the original message, along with receiver binary list
print( msg ,end_msg_list)

# prints how long the word used is for the key
keylength = len(binary_encoded_message)
print('The key length is: ' + str(keylength))