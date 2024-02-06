import numpy as np
import mss
import cv2
from win32api import GetSystemMetrics
import win32.win32gui as wg
import pyautogui as pag
import threading as th
import copy
import random
import time
import keyboard as key
from aduino import *


aduino_main()
asd = cv2.imread('asd.png')
tpl = cv2.imread('tpl.png')
            
class auto() :
    def __init__(self) -> None:
        self.cv2wait = 0
        self.mainHWND = None
        self.state = 0
        th.Thread(target=self.KeyWaiting, daemon=True).start()
        # print('시작 대기')
        # while not self.state :
        #     time.sleep(0.1)
        time.sleep(1)
        pass    
    
    def KeyWaiting(self):
        while 1 :
            if key.is_pressed('.') :                
                if self.state == 0 :                    
                    self.state = 1
                    print('시작')
                else: 
                    self.state = 0
                    print('종료')
            time.sleep(0.15)
    def Find_HWND(self, Window_name):        
        name_list = []
        name_list_ture = []
        def printer(hwnd, extra):  
                wintext = wg.GetWindowText(hwnd)
                if Window_name in wintext:
                    name_list.append(hwnd)
                if wintext == Window_name:
                    name_list_ture.append(hwnd)
        wg.EnumWindows(printer, None)
        
        if name_list_ture :
            print('[{}] 일치한 윈도우 목록'.format(Window_name))
            for i in name_list_ture :
                for i2 in name_list :
                    if i == i2 :
                        name_list.remove(i2)                    
            for i in name_list_ture :
                print(i)
        if  name_list :
            print('[{}] 포함된 윈도우 목록'.format(Window_name))        
            for i in name_list :
                print(i)
                
        if not name_list_ture and not name_list : 
            return False
            
            
        return name_list_ture, name_list
            
    def ImageLoad(self, path) :
        img = cv2.imread(path)
        
        return img
    def CaptureWindow(self,  x=0, y=0, x2=0, y2=0, hwnd = None, view = False ):
        '''윈도우 캡쳐\n
        x, y = 좌측상단 꼭짓점 x,y의 좌표, 입력시 잡힌 좌표에 합연산\n
        x2, y2 = 우측하단 꼭짓점 x,y의 좌표, 입력시 잡힌 좌표에 합연산\n
        hwnd = 캡쳐할 윈도우 핸들, 미입력시 메인 윈도우 캡쳐
        view = True시 확인용 이미지 출력 ( 기본 False)\n
        '''
        try :
            if hwnd :
                pass
            else:
                hwnd = self.mainHWND       
            img_rect = wg.GetWindowRect(hwnd)
            if x2 == GetSystemMetrics(0) :
                x2 = 0
            if y2 == GetSystemMetrics(1) :
                y2 = 0                        
            img_rect = tuple(np.add(img_rect, (x,y,x2,y2)))
            img_rect = { 'left' : int(img_rect[0]), 'top' : int(img_rect[1]), 'width' : int(img_rect[2]-img_rect[0]), 'height' : int(img_rect[3]-img_rect[1])   } 
            with mss.mss() as sct :        
                img_bit = sct.grab(img_rect)
                img = np.array(img_bit)        
            if view :
                if view == 1:
                    self.cv2wait = 0
                elif view == 2 :
                    self.cv2wait = 10
                cv2.imshow('CaptureWindow',img)
                cv2.waitKey(self.cv2wait)
            return img
        except :
            print('이미지 캡쳐 실패')
    def CaptureScreen(self, x=0, y=0, x2=0, y2=0, view = False ):   
        '''스크린 캡쳐\n
        x, y = 좌측상단 꼭짓점 x,y의 좌표\n
        x2, y2 = 우측하단 꼭짓점 x,y의 좌표\n
        view = True시 확인용 이미지 출력 ( 기본 False)\n
        아무런 인수 입력 없으면 전체화면 캡쳐\n
        '''
        try :
            if not x2 :
                x2 =  GetSystemMetrics(0)
            if not y2 :
                y2 =  GetSystemMetrics(1)
            img_rect = { 'left' : int(x), 'top' : int(y), 'width' : int(x2-x), 'height' : int(y2-y)   } 
            with mss.mss() as sct :        
                img_bit = sct.grab(img_rect)
                img = np.array(img_bit)        
            if view :
                cv2.imshow('CaptureScreen',img)
                cv2.waitKey(self.cv2wait)
            return img
        except :
            print('이미지 캡쳐 실패')
            

    
    def ImageMatch(self, main, template, accuracy=0.6, view = False) :
        '''메인 이미지에서 템플릿 이미지의 좌표 단 한개 출력\n
        main = 영역 이미지\n
        template = 찾아낼 특정 이미지\n
        accuracy = 정확도 ( 기본 0.6 )\n
        view = True시 확인용 이미지 출력 ( 기본 False)\n
        출력값 = (x, y, x2, y2)
        
        '''
        npscreen = cv2.cvtColor(main, cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        tplshape = np.shape(template)
        res1 = cv2.matchTemplate(npscreen, template ,cv2.TM_CCOEFF_NORMED )
        loc1 = np.where( res1 >= accuracy)
        xyxy = []
        for xy in zip(*loc1[::-1]) : 
            xyxy.append((xy[0], xy[1], xy[0]+tplshape[1],xy[1]+tplshape[0]))
        if xyxy and view :
            bb = xyxy[0]
            cv2.rectangle(main, (bb[0],bb[1]), (bb[2],bb[3]), (0,0,255), 1)
            npshape = np.shape(npscreen)
            y = bb[1]-50
            y2 = bb[3]+50
            x = bb[0]-50
            x2 = bb[2]+50
            if bb[1]-50 <= 0 :
                y = 0
            if bb[3]+50 >= npshape[0] :
                y2 = npshape[0]
            if bb[0]-50 <= 0 :
                x = 0
            if bb[2]+50 >= npshape[1] :
                x2 = npshape[1]
            main = main[y:y2, x:x2]
            cv2.imshow('ImageMatch',main)
            cv2.waitKey(self.cv2wait)
        elif view :
            main = np.zeros((150, 150, 3), np.uint8)
            cv2.imshow('ImageMatch',main)
            cv2.waitKey(self.cv2wait)
        if xyxy :
            return xyxy[0]
        else:
            return False
    
    
    def ImageMatch_2(self, main, template, accuracy=0.6, view = False) :
        '''메인 이미지에서 템플릿 이미지의 좌표 여러개 출력, 인접한 이미지 제외\n
        main = 영역 이미지\n
        template = 찾아낼 특정 이미지\n
        accuracy = 정확도 ( 기본 0.6 )\n
        view = True시 확인용 이미지 출력 ( 기본 False)\n
        출력값 =        [ (x, y, x2, y2)   ,   (x, y, x2, y2) ]\n
                    #첫번째로 발견한 이미지  #두번째로 발견한 이미지\n
                imagematch(main, template)[0] = 발견한 이미지중 첫번째의 xyxy좌표 # ( x, y, x2, y2 )\n
        
        '''
        npscreen = cv2.cvtColor(main, cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        tplshape = np.shape(template)
        res1 = cv2.matchTemplate(npscreen, template ,cv2.TM_CCOEFF_NORMED )
        loc1 = np.where( res1 >= accuracy)
        xyxylist = []
        checklist = []
        for xy in zip(*loc1[::-1]) : 
            checklist.append((xy[0], xy[1], xy[0]+tplshape[1],xy[1]+tplshape[0]))
        xyxylist = []        
        for num, i in enumerate(checklist) :
            if xyxylist :
                for ew in xyxylist :
                    if ew[0]+10 >= i[0] >= ew[0]-10 :
                        pass
                    else:
                        xyxylist.append(i)
            else:
                xyxylist.append(i)
            pass
        if xyxylist and view :
            bb = xyxylist[0]
            for i in xyxylist :
                cv2.rectangle(main, (i[0],i[1]), (i[2],i[3]), (0,0,255), 1)
            cv2.imshow('ImageMatch',main)
            cv2.waitKey(self.cv2wait)
        elif view :
            main = np.zeros((150, 150, 3), np.uint8)
            cv2.imshow('ImageMatch',main)
            cv2.waitKey(self.cv2wait)
            
        return xyxylist
    def WindowToScreen(self, xyxy, hwnd=None, view=False):
        '''창 내부의 좌표를 모니터 좌표로 변환\n    
        xyxy = (x,y,x2,y2) 형식의 좌표\n
        hwnd = 윈도우 핸들, 미입력시 메인 윈도우에 적용\n
        view = True시 확인용 이미지 출력 ( 기본 False)\n
        출력값 (x, y, x2, y2)            
        '''
            
        if hwnd : 
            hwnd_rect = wg.GetWindowRect(hwnd)
        else:
            hwnd_rect = wg.GetWindowRect(self.mainHWND)
        if len(xyxy) == 2 :
            x = hwnd_rect[0] + xyxy[0]
            y = hwnd_rect[1] + xyxy[1]
            return x,y
        else:
            x = hwnd_rect[0] + xyxy[0]
            y = hwnd_rect[1] + xyxy[1]
            x2 = hwnd_rect[0] + xyxy[2]
            y2 = hwnd_rect[1] + xyxy[3]
            if view :
                img = self.CaptureScreen()    
                cv2.rectangle(img, (x,y), (x2,y2), (0,0,255), 1)
                cv2.imshow('WindowToScreen',img)
                cv2.waitKey(self.cv2wait)
            return x,y,x2,y2

    def XyxyAdd(self,xyxy,add) :
        '''xyxy 좌표에서 add 만큼 이동시킴\n
        xyxy = 이동시킬 좌표 (x, y, x2, y2)\n
        add = 이동할 수치\n
        xyxyadd(xyxy, (0, 10, 0, -10))\n
        y의좌표를 +10, y2의 좌표를 -10, 좌표는 위아래로 좁아짐\n
        '''
        rect = tuple(np.add(xyxy, (add[0],add[1],add[2],add[3])))
        return rect
    
    def Click(self, xy, duration=0.25) :
        '''xy 좌표로 마우스를 이동시킨 후 클릭\n
        xy = x, y 좌표\n
        duration = 이동하는데 걸리는 시간\n
        '''        
        xt = random.randrange(-2,2)
        yt = random.randrange(-2,2)
        pag.moveTo(xy[0]+xt, xy[1]+yt)
        inputdelay()
        mouse_press('left')
        
        
    def ClickArea(self, xyxy, duration=0.25, view=False) :
        '''xyxy 좌표로 마우스를 이동시킨 후 클릭, 위치는 좌표값 사이 랜덤\n
        xyxy= x, y, x2, y2 좌표, 각각 좌측상단(x, y)과 우측하단(x2, y2)\n
        duration = 이동하는데 걸리는 시간\n
        '''       
        if view :
            img = self.CaptureScreen()         
            cv2.rectangle(img, (xyxy[0],xyxy[1]), (xyxy[2],xyxy[3]), (0,0,255), 1)
            # img = img[xyxy[1]:xyxy[3], xyxy[0]:xyxy[2]]
            imgshape = np.shape(img)
            y = xyxy[1]-50
            y2 = xyxy[3]+50
            x = xyxy[0]-50
            x2 = xyxy[2]+50
            if xyxy[1]-50 <= 0 :
                y = 0
            if xyxy[3]+50 >= imgshape[0] :
                y2 = imgshape[0]
            if xyxy[0]-50 <= 0 :
                x = 0
            if xyxy[2]+50 >= imgshape[1] :
                x2 = imgshape[1]
            img = img[y:y2, x:x2]
            cv2.imshow('ClickArea', img)
            cv2.waitKey(self.cv2wait)
        xt = (xyxy[2]- xyxy[0])*0.22
        yt = (xyxy[3]- xyxy[1])*0.22
        x = int(xyxy[0]+xt)
        y = int(xyxy[1]+yt)
        x2 = int(xyxy[2]-xt)
        y2 = int(xyxy[3]-yt)
        
        if random.random() <= 0.6 :
            x = random.randrange(x,x2)
            y = random.randrange(y,y2)
        else: 
            x = random.randrange(xyxy[0],xyxy[2])
            y = random.randrange(xyxy[1], xyxy[3])
            
        pag.moveTo(x, y, duration)
        inputdelay()
        mouse_press('left')
    def HsvMask(self,img,low,high, color=1,view=0) :
                
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        imgMASK = cv2.inRange(imgHSV,tuple(low),tuple(high) )
        img2 = cv2.bitwise_and(img, img, mask=imgMASK)
        if not color :
            img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        if view :
            if view == 1:
                self.cv2wait = 0
            elif view == 2 :
                self.cv2wait = 10
            cv2.imshow('HsvMask',img2)
            cv2.waitKey(self.cv2wait)
        return img2, imgMASK
    def WindowMouseXy(self):
        rect = wg.GetWindowRect(self.mainHWND)
        screenxy = pag.position()
        x = screenxy[0] - rect[0]
        y = screenxy[1] - rect[1]
        time.sleep(0.1)
        print(x,y)