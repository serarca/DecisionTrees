import math
import numpy as np

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
	print (sensor , var ,beg,end)

# Lists all available variables after a given variable
def available(index, v):
    mat = col_ref_matrix(168)[0]
    beg = mat[int(index % 1097)]
    avail = []
    for i in v:
        if (mat[int(i % 1097)]>=beg):
            avail.append(i)
    return avail
