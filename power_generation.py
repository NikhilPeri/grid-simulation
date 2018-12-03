import numpy as np
from grid_sim.helpers import power_matrix, power_factor

'''
Computes resulting power of
N: parallely connected turbines
'''
N=50
M=11

STEP_UP_EFFICIENCY=0.98

TURBINE_VOLTAGE=690
TURBINE_CURRENT=3.078e3
TURBINE_POWER_FACTOR=0.95

TURBINE_STEP_UP=11000/(TURBINE_VOLTAGE*STEP_UP_EFFICIENCY)
print 'TURBINE_STEP_UP {}'.format(TURBINE_STEP_UP)

turbine=power_matrix(
    STEP_UP_EFFICIENCY*TURBINE_STEP_UP*TURBINE_VOLTAGE,
    TURBINE_CURRENT/TURBINE_STEP_UP,
    TURBINE_POWER_FACTOR
)

print "\nTURBINE STEP UP"
print "Voltage: {}".format(np.absolute(turbine[0][0]))
print "Current: {}".format(np.absolute(turbine[1][0]))
print "Total Power {}".format(np.absolute(turbine[0][0] * turbine[1][0]))
print "Power Factor {}".format(power_factor(turbine[0][0], turbine[1][0]))

cluster = np.array([
    [turbine[0][0]+0j],
    [0+0j]
])

cluster_line_matrix = np.linalg.inv(np.array([
    [1, 0.504*(3.6e-3+1.35e-3j)],
    [0, 1]
]))

for i in range(N):
    cluster[1][0] += turbine[1][0]
    cluster=np.matmul(cluster_line_matrix, cluster)

print "\nCLUSTER"
print "Voltage: {}".format(np.absolute(cluster[0][0]))
print "Current: {}".format(np.absolute(cluster[1][0]))
print "Total Power {}".format(np.absolute(cluster[0][0] * cluster[1][0]))
print "Power Factor {}".format(power_factor(cluster[0][0], cluster[1][0]))

# cluster step up
CLUSTER_STEUP_UP=5
cluster[0][0] *=CLUSTER_STEUP_UP*STEP_UP_EFFICIENCY
cluster[1][0] /= CLUSTER_STEUP_UP

print "\nCLUSTER STEP UP"
print "Voltage: {}".format(np.absolute(cluster[0][0]))
print "Current: {}".format(np.absolute(cluster[1][0]))
print "Total Power {}".format(np.absolute(cluster[0][0] * cluster[1][0]))
print "Total Power {}".format(power_factor(cluster[0][0], cluster[1][0]))

farm = np.array([
    [cluster[0][0] + 0j],
    [0+0j]
])

farm_line_matrix = np.linalg.inv(np.array([
    [1, 0.748*(3.6e-3+1.35e-3j)],
    [0, 1]
]))

for i in range(M):
    farm[1][0] += cluster[1][0]
    farm=np.matmul(farm_line_matrix, farm)

print "\nFARM"
print "Voltage: {}".format(np.absolute(farm[0][0]))
print "Current: {}".format(np.absolute(farm[1][0]))
print "Total Power {}".format(np.absolute(farm[0][0] * farm[1][0]))
print "Power Factor {}".format(power_factor(farm[0][0], farm[1][0]))

# farm step up
farm_step_up=500000/(farm[0][0]*STEP_UP_EFFICIENCY)
print 'FARM STEUP UP {}:1'.format(farm_step_up)
farm[0][0] *=farm_step_up*STEP_UP_EFFICIENCY
farm[1][0] /= farm_step_up

print "\FARM STEP UP"
print "Voltage: {}".format(np.absolute(farm[0][0]))
print "Current: {}".format(np.absolute(farm[1][0]))
print "Total Power {}".format(np.absolute(farm[0][0] * farm[1][0]))
print "Power Factor {}".format(power_factor(farm[0][0], farm[1][0]))
