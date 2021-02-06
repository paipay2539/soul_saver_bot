from ahk import AHK
import time
# import threading
import keyboard
# import pyautogui
# import cv2
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

        keyboard.add_hotkey('spacebar', self.triggeredAltx)
        keyboard.add_hotkey('esc', self.triggeredEsc)
        while self.Exit is False:
            time.sleep(0.1)
            if self.Active is True:
                self.MainTask()
                print("mainloop")
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

    def InitialPos(self):
        self.MouseX = 180 - self.IsFullScreenX
        self.MouseY = 43 - self.IsFullScreenY
        self.MouseXHP = self.MouseX
        self.MouseXMP = self.MouseX
        self.MouseX1 = self.MouseXHP + 250
        self.MouseX2 = self.MouseX1 + 35
        self.MouseX3 = self.MouseX2 + 35
        self.MouseX4 = self.MouseX3 + 35
        self.MouseX5 = self.MouseX4 + 35
        self.MouseX6 = self.MouseX5 + 35

        self.MouseXV = self.MouseX4
        self.MouseXB = self.MouseXV + 35
        self.MouseXN = self.MouseXB + 35

        self.MouseYHP = self.MouseY
        self.MouseYMP = self.MouseYHP + 14
        self.MouseY1 = self.MouseYHP + 682
        self.MouseY2 = self.MouseY1
        self.MouseY3 = self.MouseY1
        self.MouseY4 = self.MouseY1
        self.MouseY5 = self.MouseY1 + 15
        self.MouseY6 = self.MouseY1 + 15

        self.MouseYV = self.MouseY4 + 35
        self.MouseYB = self.MouseYV
        self.MouseYN = self.MouseYB

        self.MouseXHP = self.MouseXHP - 20
        self.MouseXMP = self.MouseXMP - 50

        self.colorHP_start = self.ahk.pixel_get_color(self.MouseXHP,
                                                      self.MouseYHP)
        self.colorMP_start = self.ahk.pixel_get_color(self.MouseXMP,
                                                      self.MouseYMP)
        self.color1_start = self.ahk.pixel_get_color(self.MouseX1,
                                                     self.MouseY1)
        self.color2_start = self.ahk.pixel_get_color(self.MouseX2,
                                                     self.MouseY2)
        self.color3_start = self.ahk.pixel_get_color(self.MouseX3,
                                                     self.MouseY3)
        self.color4_start = self.ahk.pixel_get_color(self.MouseX4,
                                                     self.MouseY4)
        self.color5_start = self.ahk.pixel_get_color(self.MouseX5,
                                                     self.MouseY5)
        self.color6_start = self.ahk.pixel_get_color(self.MouseX6,
                                                     self.MouseY6)
        self.colorV_start = self.ahk.pixel_get_color(self.MouseXV,
                                                     self.MouseYV)
        self.colorB_start = self.ahk.pixel_get_color(self.MouseXB,
                                                     self.MouseYB)
        self.colorN_start = self.ahk.pixel_get_color(self.MouseXN,
                                                     self.MouseYN)

        if ((self.IsFullScreenX != 0) and (self.IsFullScreenY != 0)):
            self.colorHP_start = "0x4A4AFF"
            self.colorMP_start = "0xFFEE4A"
        else:
            self.colorHP_start = "0x0000FF"
            self.colorMP_start = "0xFF7B00"
        return

    def PixelUpdate(self):
        self.colorHP = self.ahk.pixel_get_color(self.MouseXHP, self.MouseYHP)
        self.colorMP = self.ahk.pixel_get_color(self.MouseXMP, self.MouseYMP)
        self.color1 = self.ahk.pixel_get_color(self.MouseX1, self.MouseY1)
        self.color2 = self.ahk.pixel_get_color(self.MouseX2, self.MouseY2)
        self.color3 = self.ahk.pixel_get_color(self.MouseX3, self.MouseY3)
        self.color4 = self.ahk.pixel_get_color(self.MouseX4, self.MouseY4)
        self.color5 = self.ahk.pixel_get_color(self.MouseX5, self.MouseY5)
        self.color6 = self.ahk.pixel_get_color(self.MouseX6, self.MouseY6)
        self.colorV = self.ahk.pixel_get_color(self.MouseXV, self.MouseYV)
        self.colorB = self.ahk.pixel_get_color(self.MouseXB, self.MouseYB)
        self.colorN = self.ahk.pixel_get_color(self.MouseXN, self.MouseYN)

    def MainTask(self):
        if self.BuffCheck == 1:
            # SkillExecute(MouseXV, MouseYV, colorV_start, "v", 1)
            self.SkillExecute(self.MouseXB, self.MouseYB,
                              self.colorB_start, "b", 1)
            self.SkillExecute(self.MouseXN, self.MouseYN,
                              self.colorN_start, "n", 1)
            self.BuffCheck = 0

        self.SkillExecute(self.MouseXHP, self.MouseYHP,
                          self.colorHP_start, "5", 1, "HP")
        self.SkillExecute(self.MouseXMP, self.MouseYMP,
                          self.colorMP_start, "6", 1, "MP")
        self.SkillExecute(self.MouseX1, self.MouseY1,
                          self.color1_start, "1", self.SkillEnable1)
        self.SkillExecute(self.MouseX2, self.MouseY2,
                          self.color2_start, "2", self.SkillEnable2)
        self.SkillExecute(self.MouseX3, self.MouseY3,
                          self.color3_start, "3", self.SkillEnable3)
        self.SkillExecute(self.MouseX4, self.MouseY4,
                          self.color4_start, "4", self.SkillEnable4)
        self.ahk.key_up('Control')
        # KeyPressControl = "False"
        # ControlHold()
        return

    def NoMainTask(self):
        self.SkillExecute(self.MouseXHP, self.MouseYHP,
                          self.colorHP_start, 6, 1, "HP")
        self.SkillExecute(self.MouseXMP, self.MouseYMP,
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
