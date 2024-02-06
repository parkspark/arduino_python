# -*- mode: python ; coding: utf-8 -*-
#!python
#cython: language_level=3
import serial
import time

import serial.tools.list_ports
import threading as th
import sys
import os
import random


timesave = 0
state = 0

def randomdelay(min, max) :
    '''
    랜덤한 시간동안 대기

    min = 최소

    max = 최대
    '''
    if random.random() <= 0.7 :
        aa = (max-min)/4
        dd = random.uniform(min+aa,max-aa)    
    else:
        dd = random.uniform(min, max)
    time.sleep(dd)
    
def inputdelay() :
    '''
    인풋 딜레이

    키를 누르고 떼는 사이의 평균 딜레이
    
    randomdelay(0.065, 0.083)
    '''
    # randomdelay(0.1152, 0.2213)
    if random.random() <= 0.7 :
        randomdelay(0.065, 0.083)
    else :            
        randomdelay(0.052, 0.105)
        
def aduino_main():
    global hard
    hard = None
    while 1:
        try :            
            ports = serial.tools.list_ports.comports()
            for port, desc, hwid in sorted(ports):
                if desc.find('Arduino Leonardo') >= 0 :
                    print('아두이노 포트 {}'.format(port))                    
                    hard =serial.Serial(port, 19200)
                    break
            if not hard :
                print('아두이노 인식 실패')
                time.sleep(1)
                continue
            break
        except :
            print('아두이노 인식 실패')
            time.sleep(1)
            continue
            
    
def key_press(key):
    ''' 키를 눌렀다 뗌 '''
    key_down(key)          
    inputdelay()                     
    key_up(key)         
    
                
def key_down( key) :
    global timesave
    while 1:
        try:
            hard.write('KD{}'.format(key).encode())
            break
        except:
            if (time.time() - timesave) >= 3 :
                timesave = time.time()
                print('아두이노 통신 오류')                
            time.sleep(0.001)
                
def key_up( key) :
    global timesave
    '''키를 뗌'''
    while 1:
        try:
            hard.write('KU{}'.format(key).encode())
            break
        except:
            if (time.time() - timesave) >= 3 :
                timesave = time.time()
                print('아두이노 통신 오류')                
            time.sleep(0.001)
            
def key_all_release():
    global timesave
    '''모든 키를 뗌'''
    while 1:
        try:
            hard.write('D'.encode())
            break
        except:
            if (time.time() - timesave) >= 3 :
                timesave = time.time()
                print('아두이노 통신 오류')                
            time.sleep(0.001)
    time.sleep(0.001)

def mouse_press( button):
    mouse_down(button)
    inputdelay()
    mouse_up(button)
    

def mouse_down( button):
    global timesave
    while 1:
        try:
            if button == 'left' :
                asd = 1
            elif button == 'right' :
                asd = 5
            else:
                break
            hard.write('{}'.format(asd).encode())
            break
        except:
            if (time.time() - timesave) >= 3 :
                timesave = time.time()
                print('아두이노 통신 오류')       
            time.sleep(0.001)

def mouse_up(button):
    global timesave
    while 1:
        try:
            if button == 'left' :
                asd = 2
            elif button == 'right' :
                asd = 6
            else:
                break
            hard.write('{}'.format(asd).encode())
            break
        except:
            if (time.time() - timesave) >= 3 :
                timesave = time.time()
                print('아두이노 통신 오류')       
            time.sleep(0.001)







if __name__ == "__main__":
    aduino_main()
# def key_down(key) :
#     hard.write('KD{}'.format(key).encode())

# def key_up(key) :
#     '''키를 뗌'''
#     hard.write('KU{}'.format(key).encode())
# def key_all_release():
#     '''모든 키를 뗌'''
#     hard.write('D'.encode())
