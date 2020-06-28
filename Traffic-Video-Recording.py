# -*- coding: utf-8 -*-
"""
Created on Fri May 17 19:46:45 2020

@author: Artash Nath (HotPopRobot.com)

Twitter @wonrobot


---------------------------------------------
THIS CODE CONSTANTLY TAKES PICTURES THORUGH YOUR CONNECT CAMMERA
ONCE YOU HAVE RUN THIS CODE FOR THE PERIOD YOU WOULD LIKE TO COUNT
TRAFFIC LEVELS FOR, PLEASE PROCEED TO RUN THE "Traffic-Recording-Analysis" 
CODE TO CALCULATE AND SAVE TRAFFIC TIME-SERIES DATA
---------------------------------------------
"""

import pyrealsense2 as rs
import cv2
from time import sleep
import os
import numpy as np
from scipy.ndimage import gaussian_filter
import time
import matplotlib.pyplot as plt
import datetime
import csv

pipe = rs.pipeline()
pipe.start()


################################################################################################
################################################################################################
cap = cv2.VideoCapture(0)
sleep(3)

def take_clip(name):
    temp = []
    f_times = []
    f_dates = []
    
    out = cv2.VideoWriter((str(name)+'.mp4'),cv2.VideoWriter_fourcc(*'DIVX'), 30, (640, 480))
    c_time = str(datetime.datetime.today()).split(' ')[1][:8]
    c_date = str(datetime.date.today())
    for i in range(200): 
        ret, frame = cap.read()
        cv2.imshow("im", frame)
        cv2.waitKey(1) & 0xFF
        out.write(frame)
        temp.append(frame)
        f_times.append(str(datetime.datetime.today()).split(' ')[1][:8])
        f_dates.append(str(datetime.date.today()))
    out.release()
    return temp,f_times, f_dates, c_time, c_date
################################################################################################
################################################################################################
os.mkdir('./recorded-data')
os.mkdir('./recorded-data/run1/')
os.mkdir('./recorded-data/run1/photos')
################################################################################################
with open(r'./recorded-data/run1/metadata.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Picture Number', 'Date', 'Time'])
    
################################################################################################
################################################################################################
################################################################################################    
    
    
cap = cv2.VideoCapture(1)
COUNT= 0


while True:
    start_t = time.time()
    path = os.path.join('./recorded-data/run1/photos', str(COUNT)) #Path to store photos
    os.mkdir(path)
    
    c_time = str(datetime.datetime.today()).split(' ')[1][:8]
    c_date = str(datetime.date.today())
    ret, frame1 = cap.read()
    sleep(0.25)
    ret, frame2 = cap.read()
    
    impath1 = os.path.join(path, 'a.jpg')
    impath2 = os.path.join(path, 'b.jpg')
    cv2.imshow("frame 1", frame1)
    cv2.imshow("frame 2", frame2)
    key = cv2.waitKey(1) & 0xFF
    cv2.imwrite(impath1, frame1)
    cv2.imwrite(impath2, frame2)
    
    with open('./recorded-data/run1/metadata.csv', 'a+', newline='') as write_obj:  # Path to MetaData file
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow([str(COUNT), c_date, c_time])
        
    
    COUNT+=1
    p_time = time.time() - start_t
    sleep(4 - p_time)
    print(time.time() - (start_t+0.0003))
################################################################################################