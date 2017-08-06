import numpy as np
import pandas as pd
import os
import math
import sys

def min_result(list1, n):
    temp = list1
    result = list1
    window = 1
    for iter in range(n):
        temp = np.fmin(temp[0:(np.size(temp)-window)], temp[window:])
        result = np.concatenate((result, temp))
        window = window * 2
    return result


def max_result(list1, n):
    temp = list1
    result = list1
    window = 1
    for iter in range(n):
        temp = np.fmax(temp[0:(np.size(temp)-window)], temp[window:])
        result = np.concatenate((result, temp))
        window = window * 2
    return result

# list1, list2 are the average of the first and second moments of the datapoints
def avg_sd_result(list1, list2, list3, n):
    temp1 = list1
    temp2 = list2
    temp3 = list3
    result1 = temp1
    result2 = temp2
    window = 1
    for iter in range(n):
        temp1 = temp1 * temp3
        temp2 = temp2 * temp3
        temp1 = np.nansum(np.array([temp1[0:(np.size(temp1)-window)], temp1[window:]]), axis = 0)
        temp2 = np.nansum(np.array([temp2[0:(np.size(temp2)-window)], temp2[window:]]), axis = 0)
        temp3 = np.nansum(np.array([temp3[0:(np.size(temp3)-window)], temp3[window:]]), axis = 0)
        temp4 = np.fmax(temp3, 1)
        temp1 = temp1/temp4
        temp2 = temp2/temp4
        result1 = np.concatenate((result1, temp1))
        result2 = np.concatenate((result2, temp2))
        window = window * 2
    result2 = np.sqrt(result2 - np.square(result1))
    return np.concatenate((result1, result2))


def min_max_avg_sd(stats, n):
    result_min = min_result(stats[:, 0], n)
    result_max = max_result(stats[:, 1], n)
    # result_avg_sd = avg_sd_result(stats[:, 2], np.square(stats[:, 2]) + np.square(stats[:, 3]), n)
    result_avg_sd = avg_sd_result(stats[:, 2], np.square(stats[:, 2]) + np.square(stats[:, 3]) * (1-1/np.fmax(1, stats[:, 4])), stats[:, 4], n)
    return np.concatenate((result_min, result_max, result_avg_sd))



def col_ref_matrix(n):
    window = 1
    result1 = range(n)
    result2 = range(n)
    size = n
    for iter in range(math.floor(math.log(n, 2))):
        size = size - window
        result1 = np.concatenate((result1, range(0, size)))
        result2 = np.concatenate((result2, range(n-size, n)))
        window = window * 2
    return np.vstack((result1, result2))




def ParsePositives(directory, filename):

    # Delay in hours
    delay = 24
    
    dfOrig = pd.read_csv(directory+filename,
                     parse_dates=[['Date','Time']], delimiter='\t')
    dfOrig2 = dfOrig.drop([0]) #TODO - remove this?
    dfOrig2['Date_Time'] = pd.to_datetime(dfOrig2['Date_Time'], format='%d.%m.%Y %H:%M:%S', errors = 'coerce')
    dfOrig2 = dfOrig2.dropna(subset=['Date_Time'])

    #Only select the columns we care about
    dfSubset = dfOrig2[['Date_Time', 'Operating_status:_Error_Locking', 'Operating_status:_Error_Blocking',
                   'Actual_Power', 'Number_of_burner_starts', 'Operating_status:_Central_heating_active',
                  'Operating_status:_Hot_water_active', 'Operating_status:_Flame', 'Relay_status:_Gasvalve',
                  'Relay_status:_Fan', 'Relay_status:_Ignition', 'Relay_status:_internal_3-way-valve',
                  'Relay_status:_HW_circulation_pump', 'Supply_temperature_(primary_flow_temperature)',
                  'Maximum_supply_(primary_flow)_temperature', 'Hot_water_temperature_setpoint', 
                  'Hot_water_outlet_temperature', 'Actual_flow_rate_turbine', 'Fan_speed']]
    
    #Fill in missing entries
    df = dfSubset.fillna(method = 'ffill')
    
    print "Successfully loaded:", directory + filename
    
    Positives = df.loc[(df['Operating_status:_Error_Locking'] == 1) 
                       & (df['Operating_status:_Error_Locking'].shift(1) == 0)]
    
    
    sensorList = ['Actual_Power', 'Number_of_burner_starts', 'Operating_status:_Central_heating_active',
                  'Operating_status:_Hot_water_active', 'Operating_status:_Flame', 'Relay_status:_Gasvalve',
                  'Relay_status:_Fan', 'Relay_status:_Ignition', 'Relay_status:_internal_3-way-valve',
                  'Relay_status:_HW_circulation_pump', 'Supply_temperature_(primary_flow_temperature)',
                  'Maximum_supply_(primary_flow)_temperature', 'Hot_water_temperature_setpoint', 
                  'Hot_water_outlet_temperature', 'Actual_flow_rate_turbine', 'Fan_speed']
    
    
    Positive_result = np.zeros((np.size(Positives, 0) * 24, 4388 * len(sensorList)))
    TimeStamps = [""] * (np.size(Positives, 0) * 24)
    outer_iter = 0
    
    for index, row in Positives.iterrows():
        for de in range(0, delay):
            #For each Positive example...
            eventTime = row['Date_Time']
            startTime = eventTime - pd.Timedelta('7 days') - pd.Timedelta('1 hours') * (de+1)
            endTime = eventTime - pd.Timedelta('1 hours') * (de+1)
            dfPos = df[(df['Date_Time'] >= startTime) & (df['Date_Time'] < endTime)]
            
            
            d = {}
            for sensor in sensorList:
                d["rawData_"+sensor] = np.zeros((168,5))
            
            for j in range(168):

                lastTime = startTime + j*pd.Timedelta('1 hour')
                currTime = startTime + (j+1)*pd.Timedelta('1 hour')

                dfHourly = dfPos[(dfPos['Date_Time'] >= lastTime) & (dfPos['Date_Time'] < currTime)]

                for sensor in sensorList:
                    
                    description = dfHourly[sensor].describe()
                    d["rawData_"+sensor][j,0] = description['min']
                    d["rawData_"+sensor][j,1] = description['max']
                    d["rawData_"+sensor][j,2] = description['mean']
                    d["rawData_"+sensor][j,3] = description['std']
                    d["rawData_"+sensor][j,4] = description['count']

            inner_iter = 0
            for sensor in sensorList:
                Positive_result[outer_iter, (inner_iter * 4388):(inner_iter+1)*4388] = min_max_avg_sd(d["rawData_"+sensor], 7)    
                inner_iter = inner_iter + 1
                
            TimeStamps[outer_iter] = str(eventTime) + " Delay: " + str(de+1)
            outer_iter = outer_iter + 1

    filename = filename[:-4]    
    Positive_result.tofile("/dfs/scratch0/sergio/PositiveData/"+filename+".np")
    with open("/dfs/scratch0/sergio/PositiveTimestamps/"+filename+".np",'w') as f_handle:
        np.savetxt(f_handle, TimeStamps, fmt="%s")



def main(argv):

    print "Starting", argv[0], argv[1]
    parseFile = argv[0] + argv[1]
    if (os.stat(parseFile).st_size > 0):
        ParsePositives(argv[0], argv[1])

    # ParseNegatives('/dfs/scratch0/bosch/BG-Data_Part11/', '2029718103746674690.csv')




if __name__ == "__main__":
    main(sys.argv[1:])
