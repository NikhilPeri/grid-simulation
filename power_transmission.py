import numpy as np
from grid_sim.helpers import power_matrix, power_factor

input=np.array([
    [500e3],
    [1.05e3]
])

LENGTH=170e3
RADIUS=0.03
SEPERATION=3

AL_RESISTIVITY=2.83e-8

resistance  =  AL_RESISTIVITY/(np.pi*(RADIUS**2))
inductance  = 4e-7*np.log(SEPERATION/(0.7788*RADIUS))
capacitance = 2*np.pi*8.85e-12/np.log(SEPERATION/RADIUS)

print 'resistance {} / km'.format(resistance*1000)
print 'capacitance {} / km'.format(capacitance*1000)
print 'inductance {} / km'.format(inductance*1000)

resistance *=LENGTH
capacitance *= LENGTH
inductance *= LENGTH

Z = resistance + (1j)*(2*np.pi*60)*inductance
Y=1j*2*np.pi*60*capacitance

A = Z*Y/2 +1
B = Z
C = Y*(Z*Y/4 +1)
D = Z*Y/2 +1

print 'A = {}'.format(A)
print 'B = {}'.format(B)
print 'C = {}'.format(C)
print 'D = {}'.format(D)

transmission_line_matrix = np.array([
    [A, B],
    [C, D],
])

output = np.matmul(np.linalg.inv(transmission_line_matrix), input)
vi=input[0][0]
ii=input[1][0]
pi=vi*ii
v=output[0][0]
i=output[1][0]
p=v*i
print 'Voltage {}'.format(np.absolute(output[0][0]))
print 'Current {}'.format(np.absolute(output[1][0]))
print 'Power Factor {}'.format(power_factor(output[0][0], output[1][0]))
print 'Total Power {}'.format(np.absolute(output[0][0] * output[1][0]))
print '% Voltage Regulation {}'.format((np.absolute(output[0][0]) - np.absolute(input[0][0]))/ np.absolute(input[0][0]))
