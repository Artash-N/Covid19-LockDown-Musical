# -*- coding: utf-8 -*-
"""
Created on Fri May 17 19:46:45 2020

@author: Artash Nath (HotPopRobot.com)

Twitter @wonrobot

------------------------------------------
THIS CODE ANALYSES FRAMES RECORDED BY "Traffic-Video-Recording"
CODE, AND OUTPUTS A CSV FILE CONTAINING TRAFFIC LEVELS
OVER TIME
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
import time

font= cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText= (125,12)
fontScale= 0.4
fontColor  = (255,255,255)
lineType= 1

#################################################################################################
cmt = lambda: int(round(time.time() * 1000))
def connected_components(image):
    # list of tags we have used 
    tags = []
    # current  tag (remember 1 and 0 are already in image so start from 2)
    tag = 2
    # counter
    cntr = 0 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] != 0:
                if i != 0 and j != 0 and image[i, j-1] != 0 and image[i-1, j] != 0 and image[i-1, j] != image[i, j-1]:
                    image[i, j] = image[i, j - 1]
                    tags.remove(image[i - 1, j])
                    cntr -= 1
                    image[image == image[i - 1, j]] = image[i, j]
                elif i != 0 and image[i-1, j] != 0:
                    image[i, j] = image[i-1, j]
                elif j != 0 and image[i, j-1] != 0:
                    image[i, j] = image[i, j-1]
                else:
                    image[i, j] = tag
                    tags.append(tag)
                    tag += 1
                    cntr += 1
    return tags, cntr
def mask3d(im0, im1):
    diff = abs(gray(im1)-gray(im0))
    diff_fl = diff.flatten()
    diff_fl = list(map(mask_map, diff_fl))
    m = np.reshape(diff_fl, (250,220))
    return gaussian_filter(m*256, 10)
def mask(im0, im1, gf):
    diff = abs(gray(im1)-gray(im0))
    diff_fl = diff.flatten()
    diff_fl = list(map(mask_map, diff_fl))
    m = np.reshape(diff_fl, (250,220))
    return gaussian_filter(m*256, gf)
def binarize(im0):
    diff_fl = im0.flatten()
    diff_fl = list(map(mask_map2, diff_fl))
    m = np.reshape(diff_fl, (250,220))
    return m
def gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.3333333333 * r + 0.3333333333 * g + 0.3333333333 * b
    return gray
def mask_map(im_p):
    if im_p > 80:
        return 1
    else:
        return 0
def mask_map2(im_p):
    if im_p > 0.2:
        return 1
    else:
        return 0


def border2(x):
    return (x*1.6)-100

def border1(x):
    return (x*7.142)


def remove_background(image):
    im_data = image
    for yc in range(len(image)):
        for xc in range(len(image[yc])):
            if (border1(xc) < yc) or (border2(xc) > yc):
                im_data[yc,xc] = [0,0,0]
    return im_data
    
    
#################################################################################################
images = []

main_dir =  './recorded-data/run1/photos'
all_dirs = os.listdir(main_dir)
all_dirs = sorted(all_dirs, key=int)
COUNT = 0

for sub_dir in all_dirs:
    start = time.time()
    sub_dir = os.path.join(main_dir,sub_dir)
    dir_subpaths = os.listdir(sub_dir)
    im1 = cv2.imread(os.path.join(sub_dir, dir_subpaths[0]))[230:, 320:540]
    im2 = cv2.imread(os.path.join(sub_dir, dir_subpaths[1]))[230:, 320:540]
    
    im2 = remove_background(im2)
    im1 = remove_background(im1)
    cv2.imshow("im1", im1)
    key = cv2.waitKey(1) & 0xFF
    
    m = binarize(mask(im1,im2,10))
    m = m.astype('float32')
    cv2.imshow("mask", m)
    key = cv2.waitKey(1) & 0xFF
    
    car_count = list(np.array(connected_components(m)[0])>10).count(True)
    with open('./recorded-data/run1/Traffic-Levels.csv', 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow([car_count])
            
    print("READING FOLDER : " + str(COUNT) + "| TIME/FOLDER ==> " + str(time.time()-start)+'   CARCOUNT :'+str(car_count))
    COUNT+=1