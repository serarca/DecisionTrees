import math
import numpy as np
import random

# Takes a list of features and returns those that are not too short, where a feature
# is too short if it isshort and it is closed to the beginning (the intuition here is
# that the behavior of one hour seven days before a failure should not be very important)
def longer_intervals(features, multiplier, limit):
	new_features = []
	for f in features:
		beg = col_ref_matrix(168)[0][int(f % 1097)]
		end = col_ref_matrix(168)[1][int(f % 1097)]
		l = end - beg + 1
		if (beg >= 168 - multiplier*l or l >= limit):
			new_features.append(f)
			print info(f)
	return new_features


def col_ref_matrix(n):
    window = 1
    result1 = range(n)
    result2 = range(n)
    size = n
    for iter in range(int(math.floor(math.log(n, 2)))):
        size = size - window
        result1 = np.concatenate((result1, range(0, size)))
        result2 = np.concatenate((result2, range(n-size, n)))
        window = window * 2
    return np.vstack((result1, result2))

sensorList = ['Actual_Power', 'Number_of_burner_starts', 'Operating_status:_Central_heating_active',
                  'Operating_status:_Hot_water_active', 'Operating_status:_Flame', 'Relay_status:_Gasvalve',
                  'Relay_status:_Fan', 'Relay_status:_Ignition', 'Relay_status:_internal_3-way-valve',
                  'Relay_status:_HW_circulation_pump', 'Supply_temperature_(primary_flow_temperature)',
                  'Maximum_supply_(primary_flow)_temperature', 'Hot_water_temperature_setpoint',
                  'Hot_water_outlet_temperature', 'Actual_flow_rate_turbine', 'Fan_speed']

variable = ['min','max','avg','sd']

# Gives information about a given variable
def info(index):
	sensor = sensorList[int(math.floor(index/4388))]
	var = variable[int(math.floor((index % 4388)/1097))]
	beg = col_ref_matrix(168)[0][int(index % 1097)]
	end = col_ref_matrix(168)[1][int(index % 1097)]
	return sensor +" "+ var +" " +str(beg) + "-" + str(end)

# Returns sensor name
def sensor(index):
	return sensorList[int(math.floor(index/4388))]

# Sample sensors. This returns a list of sensors sampled
def sample_sensors(n):
	s = random.sample(sensorList, n)
	s_list = []
	for i in range(0, 70208):
		if (sensor(i) in s):
			s_list.append(i)
	return s_list

# Gives the end_day of a variable
def end_day(index):
    return col_ref_matrix(168)[1][int(index % 1097)]

# Calculates the mean entropy for events that end in different days
def get_mean_entropy(entropies, var):
    d = np.zeros(168)
    c = np.zeros(168)
    for v in var:
        if entropies[v] != float('inf'):
            d[end_day(v)] += entropies[v]
            c[end_day(v)] += 1
        else:
            print v
    return d


def linear_weights(var, slope):
    weights = np.zeros(len(var))
    for v in var:
        weights[v] = (end_day(v)+1)*slope/168.0 + (1-slope)
    return weights

# Lists all available variables from v after a given variable
def available(index, v):
    mat = col_ref_matrix(168)[0]
    beg = mat[int(index % 1097)]
    avail = []
    for i in v:
        if (mat[int(i % 1097)]>=beg):
            avail.append(i)
    return avail

# Lists all available variables from v after a given time. Overrides the previous
def available(t0, t1, v):
	mat1 = col_ref_matrix(168)[1]
	mat0 = col_ref_matrix(168)[0]
	avail = []
	for i in v:
		if (mat1[int(i % 1097)] < t1*168 and mat0[int(i % 1097)] >= t0*168):
			avail.append(i)
	return avail
