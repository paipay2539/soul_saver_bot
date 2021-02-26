from ahk import AHK
import time
import threading
import keyboard
import win32gui
import pyautogui
import cv2
import numpy as np

import sys
sys.dont_write_bytecode = True
from find_sub_img_research import findsubimglib as fsi


class soulSaverBot:
    def __init__(self):
        self.ahk = AHK()
        self.BuffCheck = False  # no check buff
        self.Counter = 0
        self.IsFullScreen = 0
        self.SkillEnable1 = False  # True
        self.SkillEnable2 = False  # True
        self.SkillEnable3 = False  # True
        self.SkillEnable4 = False  # True
        self.PickUpEnable = 1
        self.IsFullScreenX = 0
        self.IsFullScreenY = 0

        self.AnyKeyPress = False
        self.SpacebarChecker = False
        self.CountDownTime = 0
        self.Active = False
        self.Exit = False
        self.wpercent = 100
        self.hpercent = 100

        '''
        keyboard.add_hotkey('spacebar', self.triggeredSpace)
        keyboard.add_hotkey('esc', self.triggeredEsc)
        keyboard.add_hotkey('z', self.triggeredZ)
        '''
        '''
        cv2.namedWindow('SoulSaverOnline_cv')
        cv2.createTrackbar('axis_X', 'SoulSaverOnline_cv', 0, 255,self.nothing)
        cv2.createTrackbar('axis_Y', 'SoulSaverOnline_cv', 0, 255,self.nothing)
        '''
        self.maintask = threading.Thread(target=self.maintask_thread)
        self.maintask.start()  # start new threading
        self.CountUpTime = 0
        while self.Exit is False:
            self.checkKey('space', self.triggeredSpace)
            self.checkKey('esc', self.triggeredEsc)
            self.checkKey('z', self.triggeredZ)
            self.checkKey('up')
            self.checkKey('down')
            self.checkKey('control')
            self.checkKey('left')
            self.checkKey('right')

            if self.AnyKeyPress is True:
                self.CountUpTime = self.CountUpTime + 1
            if self.CountUpTime > 10:  # 0.1sec cooldown
                self.CountUpTime = 0
                self.AnyKeyPress = False
            # print(self.CountUpTime)
            # print(self.Active)
            time.sleep(0.01)  # prevent CPU high processing

    def maintask_thread(self):
        # time_start = time.time()
        while self.Exit is False:
            # print(1/(time.time()-time_start+0.00000001))
            # time_start = time.time()
            if self.Active is True:
                self.MainTask()
                '''
                time_start = time.time()
                self.monitoring()
                print((time.time()-time_start))
                '''
                # print("mainloop")
            elif self.Active is False and self.Counter == 1:
                self.NoMainTask()
            time.sleep(0.1)

        cv2.destroyAllWindows()
        threading.Event().set()
        print("end")

    def checkKey(self, key, func=None):
        if keyboard.is_pressed(str(key)):
            if func is not None:
                func()
            if key != 'space' or self.Active is False:
                self.AnyKeyPress = True
                self.CountUpTime = 0
            time.sleep(0.2)  # prevent bouncing button

    def triggeredSpace(self):  # can't use arg
        print("space")
        if self.Counter == 0:
            self.windowScreenshot('SoulSaverOnline',  # initial ref frame
                                  hpercent=self.hpercent,
                                  wpercent=self.wpercent)
            self.InitialPos()  # need ref frame from windowScreenshot
            self.Counter = 1
        self.Active = not self.Active
        if self.Active is True:
            pass
        else:
            self.SpacebarChecker = True
            self.ahk.key_up('Control')

    def triggeredEsc(self):
        self.Exit = True

    def triggeredZ(self):
        print((int(self.mouse_now_x), int(self.mouse_now_y)))
        # self.Active = False
        self.BuffCheck = True

    def windowScreenshot(self, window_title=None, wpercent=50, hpercent=50):
        if window_title:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)
                x, y, x1, y1 = win32gui.GetClientRect(hwnd)
                x, y = win32gui.ClientToScreen(hwnd, (x, y))
                self.x_frame, self.y_frame = x, y
                x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
                mouse_now_x = int((pyautogui.position()[0]-x)*wpercent/100)
                mouse_now_y = int((pyautogui.position()[1]-y)*hpercent/100)
                raw_img = pyautogui.screenshot(region=(x, y, x1, y1))
                raw_img = cv2.cvtColor(np.array(raw_img), cv2.COLOR_RGB2BGR)
                rescale, width, height = self.rescale_frame(raw_img, wpercent,
                                                            hpercent)
                return rescale, width, height, mouse_now_x, mouse_now_y
            else:
                print('Window not found!')
        else:
            mouse_now_x = int((pyautogui.position()[0])*wpercent/100)
            mouse_now_y = int((pyautogui.position()[1])*hpercent/100)
            raw_img = pyautogui.screenshot()
            raw_img = cv2.cvtColor(np.array(raw_img), cv2.COLOR_RGB2BGR)
            rescale, width, height = self.rescale_frame(raw_img, wpercent,
                                                        hpercent)
            return rescale, width, height, mouse_now_x, mouse_now_y

    def rescale_frame(self, frame, wpercent, hpercent):
        w = int(frame.shape[1] * wpercent / 100)
        h = int(frame.shape[0] * hpercent / 100)
        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
        return frame, w, h

    def monitoring(self):
        rescale_img, \
            self.width, \
            self.height, \
            self.mouse_now_x, \
            self.mouse_now_y = self.windowScreenshot('SoulSaverOnline',
                                                     hpercent=self.hpercent,
                                                     wpercent=self.wpercent)

        mid_pos = (int(self.width/2), int(self.height/2))
        text_pos = (int(self.width/2), int(self.height/4))
        text2_pos = (int(self.width/2), int(self.height*3/4))
        mouse_pos = (int(self.mouse_now_x), int(self.mouse_now_y))

        neko_monster = cv2.imread(r'data\pink_neko.png')
        character = cv2.imread(r'data\character.png')

        neko_monster_pos = fsi.findsubimg(rescale_img, neko_monster)
        character_pos = fsi.findsubimg(rescale_img, character)

        character_direction = fsi.character_direction(character_pos)

        neko_monster_pos = fsi.list_fast_flat(neko_monster_pos)
        character_pos = fsi.list_fast_flat(character_pos)
        # rescale_img = fsi.mask_roi(rescale_img, [neko_monster_pos, character_pos])

        character_qpos = fsi.quantization(character_pos, self.width, self.height, rescale_img ,(255, 255, 0))
        neko_monster_qpos = fsi.quantization(neko_monster_pos, self.width, self.height, rescale_img, (255, 0, 255))
        mouse_qpos = fsi.quantization([mouse_pos], self.width, self.height, rescale_img, (0, 0, 255))
        fsi.quantization_table_drawing(rescale_img, self.width, self.height)

        '''
        self.trackbars()
        trackbars_pos = (int(self.axis_X), int(self.axis_Y))
        '''
        # print("getColour:", self.getColour(rescale_img, self.button1_pos),
        #     "getColourWindow:", self.getColourWindow(self.button1_pos),
        #     "getColourWindowAHK:", self.getColourWindowAHK(self.button1_pos))
        '''
        raw
        getColour: 0.0009999275207519531
        getColourWindow: 0.0260009765625
        getColourWindowAHK: 0.19802093505859375
        avg
        getColour: 0.0
        getColourWindow: 0.012013554573059082
        getColourWindowAHK: 0.11300599575042725
        '''


        text = "X:"+str(self.mouse_now_x)+" Y:"+str(self.mouse_now_y)
        self.drawText(rescale_img, text, text_pos)
        self.drawText(rescale_img, character_direction, text2_pos)
        im = cv2.circle(rescale_img, mouse_pos, radius=5,
                        color=(0, 255, 255), thickness=-1)
        self.coloring(im)
        im, _, _ = self.rescale_frame(im, 40, 100)
        cv2.imshow('SoulSaverOnline_cv', im)
        cv2.waitKey(1)

    def nothing(self):
        pass

    def trackbars(self):
        self.axis_X = cv2.getTrackbarPos('axis_X', 'SoulSaverOnline_cv')
        self.axis_X = int(self.axis_X/255*self.width)
        self.axis_Y = cv2.getTrackbarPos('axis_Y', 'SoulSaverOnline_cv')
        self.axis_Y = int(self.axis_Y/255*self.height)

    def coloring(self, img):
        show_colour = (0, 255, 255)
        special_colour =  (0, 255, 255)
        '''
        img = cv2.circle(img, self.buttonHP_pos, radius=5, color=self.getColour(img, self.buttonHP_pos), thickness=-1)
        img = cv2.circle(img, self.buttonMP_pos, radius=5, color=self.getColour(img, self.buttonMP_pos), thickness=-1)
        img = cv2.circle(img, self.button1_pos, radius=5, color=self.getColour(img, self.button1_pos), thickness=-1)
        img = cv2.circle(img, self.button2_pos, radius=5, color=self.getColour(img, self.button2_pos), thickness=-1)
        img = cv2.circle(img, self.button3_pos, radius=5, color=self.getColour(img, self.button3_pos), thickness=-1)
        img = cv2.circle(img, self.button4_pos, radius=5, color=self.getColour(img, self.button4_pos), thickness=-1)
        img = cv2.circle(img, self.button5_pos, radius=5, color=self.getColour(img, self.button5_pos), thickness=-1)
        img = cv2.circle(img, self.button6_pos, radius=5, color=self.getColour(img, self.button6_pos), thickness=-1)
        img = cv2.circle(img, self.buttonV_pos, radius=5, color=self.getColour(img, self.buttonV_pos), thickness=-1)
        img = cv2.circle(img, self.buttonB_pos, radius=5, color=self.getColour(img, self.buttonB_pos), thickness=-1)
        img = cv2.circle(img, self.buttonN_pos, radius=5, color=self.getColour(img, self.buttonN_pos), thickness=-1)
        '''

        img = cv2.circle(img, self.buttonHP_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.buttonMP_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.button1_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.button2_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.button3_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.button4_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.button5_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.button6_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.buttonV_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.buttonB_pos, radius=5, color=show_colour, thickness=-1)
        img = cv2.circle(img, self.buttonN_pos, radius=5, color=show_colour, thickness=-1)

    def getColour(self, img, pos):
        color = (int(img[pos[1], pos[0]][0]),
                 int(img[pos[1], pos[0]][1]),
                 int(img[pos[1], pos[0]][2]))
        '''
        opencv2
        BGR [255 255 255]
        print(rescale_img[self.button1_pos[1], self.button1_pos[0]])
        '''
        return color

    def getColourWindow(self, pos):
        window_pos = [[], []]
        window_pos[0] = int(self.x_frame + pos[0] * (100/self.wpercent))
        window_pos[1] = int(self.y_frame + pos[1] * (100/self.hpercent))
        color = (int(pyautogui.pixel(*window_pos)[2]),  # RGB to BGR
                 int(pyautogui.pixel(*window_pos)[1]),
                 int(pyautogui.pixel(*window_pos)[0]))
        '''
        pyautogui
        RGB to BGR (255,255,255)
        '''
        return color

    def getColourWindowAHK(self, pos):
        window_pos = [[], []]
        window_pos[0] = int(self.x_frame + pos[0] * (100/self.wpercent))
        window_pos[1] = int(self.y_frame + pos[1] * (100/self.hpercent))
        color = (int(self.ahk.pixel_get_color(*window_pos)[6:8], 16),
                 int(self.ahk.pixel_get_color(*window_pos)[4:6], 16),
                 int(self.ahk.pixel_get_color(*window_pos)[2:4], 16))
        '''
        ahk
        RGB to BGR 0xFFFFFF
        '''
        return color

    def drawText(self, img, text, text_pos):
        cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 1, cv2.LINE_AA)

    def InitialPos(self):
        # self.MouseX = 180 - self.IsFullScreenX
        # self.MouseY = 43 - self.IsFullScreenY
        '''
        hwnd = win32gui.FindWindow(None, 'SoulSaverOnline')
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            width = x1-x
            height = y1-y
            print(width, height)
            start_x_offset = int(width/2) - 400
            start_y_offset = height - 400
            width, height
        else:
            print('Window not found!')
            return
        '''
        now_wpercent = self.wpercent
        now_hpercent = self.hpercent
        reverse_x_ratio = now_wpercent/50  # we measure position at 50pc
        reverse_y_ratio = now_hpercent/50  # we measure position at 50pc
        MouseXHP = 85 * reverse_x_ratio
        MouseXMP = 85 * reverse_x_ratio
        MouseYHP = 5 * reverse_y_ratio
        MouseYMP = 13 * reverse_y_ratio

        start_x_offset = 240  # 1280x720
        startButton1_x_pos = start_x_offset * reverse_x_ratio
        x_pos_diff = 19 * reverse_x_ratio
        MouseX1 = startButton1_x_pos + x_pos_diff*0
        MouseX2 = startButton1_x_pos + x_pos_diff*1
        MouseX3 = startButton1_x_pos + x_pos_diff*2
        MouseX4 = startButton1_x_pos + x_pos_diff*3
        MouseX5 = startButton1_x_pos + x_pos_diff*4
        MouseX6 = startButton1_x_pos + x_pos_diff*5

        MouseXV = startButton1_x_pos + x_pos_diff*3
        MouseXB = startButton1_x_pos + x_pos_diff*4
        MouseXN = startButton1_x_pos + x_pos_diff*5

        start_y_offset = 320  # 1280x720
        startButton1_y_pos = start_y_offset * reverse_y_ratio
        y_pos_diff = 17 * reverse_y_ratio
        MouseY1 = startButton1_y_pos
        MouseY2 = startButton1_y_pos
        MouseY3 = startButton1_y_pos
        MouseY4 = startButton1_y_pos
        MouseY5 = startButton1_y_pos
        MouseY6 = startButton1_y_pos

        MouseYV = startButton1_y_pos + y_pos_diff
        MouseYB = startButton1_y_pos + y_pos_diff
        MouseYN = startButton1_y_pos + y_pos_diff

        self.buttonHP_pos = (int(MouseXHP), int(MouseYHP))
        self.buttonMP_pos = (int(MouseXMP), int(MouseYMP))
        self.button1_pos = (int(MouseX1), int(MouseY1))
        self.button2_pos = (int(MouseX2), int(MouseY2))
        self.button3_pos = (int(MouseX3), int(MouseY3))
        self.button4_pos = (int(MouseX4), int(MouseY4))
        self.button5_pos = (int(MouseX5), int(MouseY5))
        self.button6_pos = (int(MouseX6), int(MouseY6))
        self.buttonV_pos = (int(MouseXV), int(MouseYV))
        self.buttonB_pos = (int(MouseXB), int(MouseYB))
        self.buttonN_pos = (int(MouseXN), int(MouseYN))

        '''
        upper x = 213 + 19 y = 352 + 17
        lower x = 213 + 19 y = 369

        1 (214, 350) 21
        2 (235, 350) 18
        3 (252, 349) 18
        4 (270, 350) 18
        5 (288, 352) 17
        6 (305, 352)

        z (213, 369) 21
        x (234, 369) 19
        c (253, 369) 18
        v (271, 369) 19
        b (290, 369) 18
        n (308, 368)

        HP (85, 5)
        MP (86, 13)
        '''

        self.colorHP_start = self.getColourWindow(self.buttonHP_pos)
        self.colorMP_start = self.getColourWindow(self.buttonMP_pos)
        self.color1_start = self.getColourWindow(self.button1_pos)
        self.color2_start = self.getColourWindow(self.button2_pos)
        self.color3_start = self.getColourWindow(self.button3_pos)
        self.color4_start = self.getColourWindow(self.button4_pos)
        self.color5_start = self.getColourWindow(self.button5_pos)
        self.color6_start = self.getColourWindow(self.button6_pos)
        self.colorV_start = self.getColourWindow(self.buttonV_pos)
        self.colorB_start = self.getColourWindow(self.buttonB_pos)
        self.colorN_start = self.getColourWindow(self.buttonN_pos)
        # print(self.colorHP_start, self.colorMP_start)

        if ((self.IsFullScreenX != 0) and (self.IsFullScreenY != 0)):
            self.colorHP_start = (0, 0, 247)
            self.colorMP_start = (255, 189, 8)
        else:
            self.colorHP_start = (0, 0, 247)
            self.colorMP_start = (255, 189, 8)

        return

    def PixelUpdate(self):
        self.colorHP = self.getColourWindow(self.buttonHP_pos)
        self.colorMP = self.getColourWindow(self.buttonMP_pos)
        self.color1 = self.getColourWindow(self.button1_pos)
        self.color2 = self.getColourWindow(self.button2_pos)
        self.color3 = self.getColourWindow(self.button3_pos)
        self.color4 = self.getColourWindow(self.button4_pos)
        self.color5 = self.getColourWindow(self.button5_pos)
        self.color6 = self.getColourWindow(self.button6_pos)
        self.colorV = self.getColourWindow(self.buttonV_pos)
        self.colorB = self.getColourWindow(self.buttonB_pos)
        self.colorN = self.getColourWindow(self.buttonN_pos)

    def MainTask(self):
        if self.BuffCheck is True:
            self.SkillExecute(self.buttonV_pos,
                              self.colorV_start, "v", True)
            self.SkillExecute(self.buttonB_pos,
                              self.colorB_start, "b", True)
            self.SkillExecute(self.buttonN_pos,
                              self.colorN_start, "n", True)
            self.BuffCheck = False
        self.SkillExecute(self.buttonHP_pos,
                          self.colorHP_start, "5", True, "HP")
        self.SkillExecute(self.buttonMP_pos,
                          self.colorMP_start, "6", True, "MP")
        self.SkillExecute(self.button1_pos,
                          self.color1_start, "1", self.SkillEnable1)
        self.SkillExecute(self.button2_pos,
                          self.color2_start, "2", self.SkillEnable2)
        self.SkillExecute(self.button3_pos,
                          self.color3_start, "3", self.SkillEnable3)
        self.SkillExecute(self.button4_pos,
                          self.color4_start, "4", self.SkillEnable4)
        # self.ahk.key_up('Control')
        # KeyPressControl = "False"
        # ControlHold()
        return

    def NoMainTask(self):
        self.SkillExecute(self.buttonHP_pos,
                          self.colorHP_start, "5", True, "HP")
        self.SkillExecute(self.buttonMP_pos,
                          self.colorMP_start, "6", True, "MP")
        return

    def SkillExecute(self, pos,
                     PixelStart, SkillButton, SkillEnable, Refills="OFF"):
        '''
        delay
        self.CheckAnyKeyPress()
        '''

        #time_start = time.time()
        self.monitoring()
        #print((time.time()-time_start))

        # print(pos,PixelStart)
        if ((self.AnyKeyPress is False and SkillEnable is True)
                or (Refills == "HP" or Refills == "MP")):
            PixelNow = self.getColourWindow(pos)
            if Refills == "OFF":
                # if PixelNow == PixelStart:
                #     self.ahk.key_down(SkillButton)
                #     time.sleep(0.10)
                #     self.ahk.key_up(SkillButton)
                #     time.sleep(0.35)
                if PixelNow == PixelStart:
                    LoopChecker = 0
                    while True:
                        self.ahk.key_down(SkillButton)
                        time.sleep(0.10)
                        self.ahk.key_up(SkillButton)
                        time.sleep(0.01)
                        PixelNow = self.getColourWindow(pos)
                        if (PixelNow != PixelStart
                                or LoopChecker >= 20
                                or self.SpacebarChecker is True):
                            self.SpacebarChecker = False
                            break
                        LoopChecker += 1
            else:
                if PixelNow != PixelStart:
                    self.ahk.key_down(SkillButton)
                    time.sleep(0.10)
                    self.ahk.key_up(SkillButton)
                    time.sleep(0.01)
        return

    def CheckAnyKeyPress(self):
        KeyPressSpace = self.ahk.key_state('Space')
        KeyPressControl = self.ahk.key_state('Control')
        KeyPressUp = self.ahk.key_state('Up')
        KeyPressDown = self.ahk.key_state('Down')
        KeyPressRight = self.ahk.key_state('Right')
        KeyPressLeft = self.ahk.key_state('Left')
        '''
        print("KeyPressSpace:", KeyPressSpace,
              "KeyPressControl:", KeyPressControl,
              "KeyPressUp:", KeyPressUp,
              "KeyPressDown:", KeyPressDown,
              "KeyPressRight:", KeyPressRight,
              "KeyPressLeft:", KeyPressLeft)
        '''
        if (KeyPressSpace is True
                or KeyPressControl is True
                or KeyPressUp is True
                or KeyPressDown is True
                or KeyPressRight is True
                or KeyPressLeft is True):
            self.AnyKeyPress = True
            self.CountDownTime = 0
            if ((KeyPressRight is True or KeyPressLeft is True)
                    and (KeyPressUp is False)
                    and (KeyPressControl is False)
                    and (self.PickUpEnable is False)):
                self.ControlHold()
        else:
            if self.CountDownTime >= 3:
                self.AnyKeyPress = False
            else:
                self.AnyKeyPress = True
                self.CountDownTime += 1
        # print(self.CountDownTime)

    def ControlHold(self):
        self.ahk.key_down('Control')
        time.sleep(0.01)
        self.ahk.key_up('Control')
        time.sleep(0.01)
        return


def main():
    Bot = soulSaverBot()


if __name__ == '__main__':
    main()
