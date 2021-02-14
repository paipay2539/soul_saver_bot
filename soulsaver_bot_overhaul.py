from ahk import AHK
import time
# import threading
import keyboard
import win32gui
import pyautogui
import cv2
import numpy as np
# from opencvKeyboardDetect import waitKeyFunc


class soulSaverBot:
    def __init__(self):
        self.ahk = AHK()
        self.BuffCheck = 1
        self.Counter = 0
        self.IsFullScreen = 0
        self.SkillEnable1 = 0
        self.SkillEnable2 = 0
        self.IsFullScreen = 0
        self.SkillEnable1 = 1
        self.SkillEnable2 = 1
        self.SkillEnable3 = 1
        self.SkillEnable4 = 1
        self.PickUpEnable = 1
        self.IsFullScreenX = 0
        self.IsFullScreenY = 0

        self.AnyKeyPress = 0
        self.SpacebarChecker = 0
        self.CountDownTime = 0
        self.Active = False
        self.Exit = False
        self.wpercent = 50
        self.hpercent = 50

        keyboard.add_hotkey('spacebar', self.triggeredAltx)
        keyboard.add_hotkey('esc', self.triggeredEsc)
        keyboard.add_hotkey('z', self.triggeredZ)
        '''
        cv2.namedWindow('SoulSaverOnline_cv')
        cv2.createTrackbar('axis_X', 'SoulSaverOnline_cv', 0, 255,self.nothing)
        cv2.createTrackbar('axis_Y', 'SoulSaverOnline_cv', 0, 255,self.nothing)
        '''
        #time_start = time.time()
        while self.Exit is False:
            #print(1/(time.time()-time_start+0.00000001))
            #time_start = time.time()
            time.sleep(0.1)
            if self.Active is True:
                # self.MainTask()
                self.monitoring()
                # print("mainloop")

        cv2.destroyAllWindows()
        print("end")

    def triggeredAltx(self):  # can't use arg
        print("space")
        if self.Counter == 0:
            self.Counter = 1
            self.InitialPos()
        self.Active = not self.Active
        if self.Active is True:
            pass
        else:
            self.SpacebarChecker = 1
            self.ahk.key_up('Control')

    def triggeredEsc(self):
        self.Exit = True

    def triggeredZ(self):
        print((int(self.mouse_now_x), int(self.mouse_now_y)))

    def windowScreenshot(self, window_title=None, wpercent=50, hpercent=50):
        if window_title:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)
                x, y, x1, y1 = win32gui.GetClientRect(hwnd)
                x, y = win32gui.ClientToScreen(hwnd, (x, y))
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
        mouse_pos = (int(self.mouse_now_x), int(self.mouse_now_y))

        '''
        self.trackbars()
        trackbars_pos = (int(self.axis_X), int(self.axis_Y))
        '''
        print(rescale_img[self.button1_pos[1], self.button1_pos[0]])
        text = "X:"+str(self.mouse_now_x)+" Y:"+str(self.mouse_now_y)
        self.drawText(rescale_img, text, text_pos)
        im = cv2.circle(rescale_img, mouse_pos, radius=5,
                        color=(0, 255, 255), thickness=-1)
        self.coloring(im)
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
        img = cv2.circle(img, self.buttonHP_pos, radius=5, color=self.getColour(img,self.buttonHP_pos), thickness=-1)
        img = cv2.circle(img, self.buttonMP_pos, radius=5, color=self.getColour(img,self.buttonMP_pos), thickness=-1)
        img = cv2.circle(img, self.button1_pos , radius=5, color=self.getColour(img,self.button1_pos ), thickness=-1)
        img = cv2.circle(img, self.button2_pos , radius=5, color=self.getColour(img,self.button2_pos ), thickness=-1)
        img = cv2.circle(img, self.button3_pos , radius=5, color=self.getColour(img,self.button3_pos ), thickness=-1)
        img = cv2.circle(img, self.button4_pos , radius=5, color=self.getColour(img,self.button4_pos ), thickness=-1)
        img = cv2.circle(img, self.button5_pos , radius=5, color=self.getColour(img,self.button5_pos ), thickness=-1)
        img = cv2.circle(img, self.button6_pos , radius=5, color=self.getColour(img,self.button6_pos ), thickness=-1)
        img = cv2.circle(img, self.buttonV_pos , radius=5, color=self.getColour(img,self.buttonV_pos ), thickness=-1)
        img = cv2.circle(img, self.buttonB_pos , radius=5, color=self.getColour(img,self.buttonB_pos ), thickness=-1)
        img = cv2.circle(img, self.buttonN_pos , radius=5, color=self.getColour(img,self.buttonN_pos ), thickness=-1)

    def getColour(self, img, pos):
        color = (int(img[pos[1], pos[0]][0]),
                 int(img[pos[1], pos[0]][1]),
                 int(img[pos[1], pos[0]][2]))
        return color

    def drawText(self, img, text, text_pos):
        cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 1, cv2.LINE_AA)

    def InitialPos(self):
        # self.MouseX = 180 - self.IsFullScreenX
        # self.MouseY = 43 - self.IsFullScreenY
        now_wpercent = self.wpercent
        now_hpercent = self.hpercent
        reverse_x_ratio = now_wpercent/50  # we measure position at 50pc
        reverse_y_ratio = now_hpercent/50  # we measure position at 50pc
        MouseXHP = 85 * reverse_x_ratio
        MouseXMP = 85 * reverse_x_ratio
        MouseYHP = 5 * reverse_y_ratio
        MouseYMP = 13 * reverse_y_ratio

        startButton1_x_pos = 213 * reverse_x_ratio
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

        startButton1_y_pos = 350 * reverse_y_ratio
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

        self.colorHP_start = self.ahk.pixel_get_color(self.buttonHP_pos[0],
                                                      self.buttonHP_pos[1])
        self.colorMP_start = self.ahk.pixel_get_color(self.buttonMP_pos[0],
                                                      self.buttonMP_pos[1])
        self.color1_start = self.ahk.pixel_get_color(self.button1_pos[0],
                                                     self.button1_pos[1])
        self.color2_start = self.ahk.pixel_get_color(self.button2_pos[0],
                                                     self.button2_pos[1])
        self.color3_start = self.ahk.pixel_get_color(self.button3_pos[0],
                                                     self.button3_pos[1])
        self.color4_start = self.ahk.pixel_get_color(self.button4_pos[0],
                                                     self.button4_pos[1])
        self.color5_start = self.ahk.pixel_get_color(self.button5_pos[0],
                                                     self.button5_pos[1])
        self.color6_start = self.ahk.pixel_get_color(self.button6_pos[0],
                                                     self.button6_pos[1])
        self.colorV_start = self.ahk.pixel_get_color(self.buttonV_pos[0],
                                                     self.buttonV_pos[1])
        self.colorB_start = self.ahk.pixel_get_color(self.buttonB_pos[0],
                                                     self.buttonB_pos[1])
        self.colorN_start = self.ahk.pixel_get_color(self.buttonN_pos[0],
                                                     self.buttonN_pos[1])

        if ((self.IsFullScreenX != 0) and (self.IsFullScreenY != 0)):
            self.colorHP_start = "0x4A4AFF"
            self.colorMP_start = "0xFFEE4A"
        else:
            self.colorHP_start = "0x0000FF"
            self.colorMP_start = "0xFF7B00"
        return

    def PixelUpdate(self):
        self.colorHP = self.ahk.pixel_get_color(self.buttonHP_pos[0],
                                                self.buttonHP_pos[1])
        self.colorMP = self.ahk.pixel_get_color(self.buttonMP_pos[0],
                                                self.buttonMP_pos[1])
        self.color1 = self.ahk.pixel_get_color(self.button1_pos[0],
                                               self.button1_pos[1])
        self.color2 = self.ahk.pixel_get_color(self.button2_pos[0],
                                               self.button2_pos[1])
        self.color3 = self.ahk.pixel_get_color(self.button3_pos[0],
                                               self.button3_pos[1])
        self.color4 = self.ahk.pixel_get_color(self.button4_pos[0],
                                               self.button4_pos[1])
        self.color5 = self.ahk.pixel_get_color(self.button5_pos[0],
                                               self.button5_pos[1])
        self.color6 = self.ahk.pixel_get_color(self.button6_pos[0],
                                               self.button6_pos[1])
        self.colorV = self.ahk.pixel_get_color(self.buttonV_pos[0],
                                               self.buttonV_pos[1])
        self.colorB = self.ahk.pixel_get_color(self.buttonB_pos[0],
                                               self.buttonB_pos[1])
        self.colorN = self.ahk.pixel_get_color(self.buttonN_pos[0],
                                               self.buttonN_pos[1])

    def MainTask(self):
        if self.BuffCheck == 1:
            self.SkillExecute(self.buttonV_pos[0], self.buttonV_pos[1],
                              self.colorV_start, "v", 1)
            self.SkillExecute(self.buttonB_pos[0], self.buttonB_pos[1],
                              self.colorB_start, "b", 1)
            self.SkillExecute(self.buttonN_pos[0], self.buttonN_pos[1],
                              self.colorN_start, "n", 1)
            self.BuffCheck = 0

        self.SkillExecute(self.buttonHP_pos[0], self.buttonHP_pos[1],
                          self.colorHP_start, "5", 1, "HP")
        self.SkillExecute(self.buttonMP_pos[0], self.buttonMP_pos[1],
                          self.colorMP_start, "6", 1, "MP")
        self.SkillExecute(self.button1_pos[0], self.button1_pos[1],
                          self.color1_start, "1", self.SkillEnable1)
        self.SkillExecute(self.button2_pos[0], self.button2_pos[1],
                          self.color2_start, "2", self.SkillEnable2)
        self.SkillExecute(self.button3_pos[0], self.button3_pos[1],
                          self.color3_start, "3", self.SkillEnable3)
        self.SkillExecute(self.button4_pos[0], self.button4_pos[1],
                          self.color4_start, "4", self.SkillEnable4)
        self.ahk.key_up('Control')
        # KeyPressControl = "False"
        # ControlHold()
        return

    def NoMainTask(self):
        self.SkillExecute(self.buttonHP_pos[0], self.buttonHP_pos[1],
                          self.colorHP_start, 6, 1, "HP")
        self.SkillExecute(self.buttonMP_pos[0], self.buttonMP_pos[1],
                          self.colorMP_start, 5, 1, "MP")
        return

    def SkillExecute(self, MouseXNOW, MouseYNOW,
                     PixelStart, SkillButton, SkillEnable, Refills="OFF"):
        self.CheckAnyKeyPress()
        if ((self.AnyKeyPress == 0 and SkillEnable == 1)
                or (Refills == "HP" or Refills == "MP")):
            PixelNow = self.ahk.pixel_get_color(MouseXNOW, MouseYNOW)
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
                        PixelNow = self.ahk.pixel_get_color(MouseXNOW,
                                                            MouseYNOW)
                        if (PixelNow != PixelStart
                                or LoopChecker >= 20
                                or self.SpacebarChecker == 1):
                            self.SpacebarChecker = 0
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
        KeyPressSpace = self.ahk.key_state('Control')
        KeyPressControl = self.ahk.key_state('Control')
        KeyPressUp = self.ahk.key_state('Control')
        KeyPressDown = self.ahk.key_state('Control')
        KeyPressRight = self.ahk.key_state('Control')
        KeyPressLeft = self.ahk.key_state('Control')
        if (KeyPressSpace is True
                or KeyPressControl is True
                or KeyPressUp is True
                or KeyPressDown is True
                or KeyPressRight is True
                or KeyPressLeft is True):
            self.AnyKeyPress = 1
            self.CountDownTime = 0
            if ((KeyPressRight is True or KeyPressLeft is True)
                    and (KeyPressUp is False)
                    and (KeyPressControl is False)
                    and (self.PickUpEnable is False)):
                self.ControlHold()
        else:
            if self.CountDownTime >= 5:
                self.AnyKeyPress = 0
            else:
                self.AnyKeyPress = 1
                self.CountDownTime += 1

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
