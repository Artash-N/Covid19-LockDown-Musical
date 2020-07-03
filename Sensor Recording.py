import serial
arduino = serial.Serial('COM3', 9600, timeout=.1)
import csv
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


dust1 = None
dust2 = None
dust3 = None
sound = None
temp = None                                                                                                                                
hum = None
log_read = None
res = None

while True:
    data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
    if data:
        print(data)
    csv_string = ''
    if b'Dust: ' in data:
        dust = data.decode()
        dust = (dust[dust.index(':')+1:]).split(',')
        dust1  = dust[0]
        dust2 = dust[1]
        dust3 = dust[2]
    elif b'sound: ' in data:
        sound = data.decode()
        sound = sound[sound.index(':')+1:]
    elif b'Temp: ' in data:
        temp = data.decode()
        temp = temp[temp.index(':')+1:]
    elif b'Hum: ' in data:
        hum = data.decode()
        hum = hum[hum.index(':')+1:]
    elif b'analog read data: 'in data:
        log_read = data.decode()
        log_read = log_read[log_read.index(':')+1:]
    elif b'sensor resistance: ' in data:
        res = data.decode()
        res = res[res.index(':')+1:]
    
    if sound and temp and hum and log_read and res:
        rows = []
        file = open('data.csv', 'r')
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
        file.close()
        
        file = open('data.csv', 'w', newline='')
        rows.append([str(datetime.date.today()), str(datetime.datetime.today()).split(' ')[1][:8],sound,temp, hum, log_read,res])  
        writer = csv.writer(file)
        for row in rows:
            if (len(row) > 7) and (row[0]!=''):
                writer.writerow(row)
        file.close()
        print("Finished Writing")
        dust1 = None
        dust2 = None
        dust3= None
        sound = None
        temp = None
        hum = None
        log_read = None
        res = None
        
        
         
    
    