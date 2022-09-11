import csv
import serial
import pandas as pd
from datetime import datetime

#input: arduino output: fingerprint ID, weight status
#output: a csv with: use order, real time, fingerprint ID, student's name, student's ID, weight status before unlocking, weight status after unlocking, action (place or take an item), difference in weight between before and after unlocking 

def data_processing_and_storing(loop):
    user_info = pd.read_csv('user_information.csv', sep = ',')
    arduino_port = '/dev/cu.usbmodem141101' #serial port of Arduino
    baud = 9600 #arduino uno runs at 9600 baud
    fileName = 'analog-data.csv'
    ser = serial.Serial(arduino_port, baud)
    print("Connected to Arduino port:" + arduino_port)
    file = open(fileName, "a")
    print("Created file")

    #display the data to the terminal
    sensor_data = [['#', 'Date and time', 'Fingerprint ID', "Student's name", "Student's ID", 'Before', 'After', 'Status', 'Difference']] #store data

    # collect the samples
    index = 0
    while index < loop:
        getData = ser.readline()
        dataString = getData.decode('utf-8')
        data = dataString[0:][:-2]
        print(data)
        
        #foung fingerprint --> store user's information
        if data == 'Fingerprint ID:':
            #order of use time
            order = index + 1
            sensor_data.append([])
            sensor_data[order].append(index)
            
            #date and time
            right_now = datetime.now() #get time
            sensor_data[order].append(right_now.strftime("%d/%m/%Y %H:%M:%S"))
            
            #read fingerprint ID
            getData = ser.readline()
            dataString = getData.decode('utf-8')
            fingerprint_id = dataString[0:][:-2] 
            print(fingerprint_id)
            
            #store fingerprint
            sensor_data[order].append(fingerprint_id)
            
            #match student's name and ID from enrollment database
            name = user_info["Student's name"][user_info["Fingerprint ID"] == int(fingerprint_id)].iloc[0] #print student's name of the fingerprint ID
            sensor_data[order].append(name)
            student_id = user_info["Student's ID"][user_info["Fingerprint ID"] == int(fingerprint_id)].iloc[0] #print student's ID of the fingerprint ID
            sensor_data[order].append(student_id)
            print(sensor_data[order])
           
        #action log --> store weight status before unlocking
        if data == 'Weight status:':
            getData = ser.readline()
            dataString = getData.decode('utf-8')
            weight = dataString[0:][:-2]
            print(weight)
            sensor_data[order].append(weight)
            index += 1
        
        #action log --> store weight status after closing
        if index >= 2: #from the second user
            difference = float(sensor_data[index - 1][5]) - float(weight)
            if difference > 0:
                status = 'Placed'
            elif difference == 0:
                status = 'Unchanged'
            else:
                status = 'Taken'
            sensor_data[index - 1].extend([weight, status, difference])
            
            
    # create the CSV
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sensor_data)

    print("Data collection complete!")
    file.close()