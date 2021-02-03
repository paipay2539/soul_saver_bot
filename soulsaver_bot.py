import ahk
import cv2
import time

def SkillExecute( MouseXNOW , MouseYNOW, PixelStart,SkillButton, SkillEnable, Refills="OFF"):
    CheckAnyKeyPress()
    global AnyKeyPress
    global SpacebarChecker
    if (AnyKeyPress == 0 and SkillEnable == 1) or (Refills == "HP" or Refills == "MP"):
        if Refills == "OFF":
            pass
    pass


def ControlHold():
    ahk.key_down('Control')
    time.sleep(0.01)
    ahk.key_up('Control')
    time.sleep(0.01)
    return



def
myhotkey = Hotkey('CTRL+T', some_script)




class soulSaverBot:
    def __init__(self):
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


    def MainTask(self):
        if self.BuffCheck == 1:
            # SkillExecute(MouseXV, MouseYV, colorV_start, "v", 1)
            self.SkillExecute(self.MouseXB, self.MouseYB,
                              self.colorB_start, "b", 1)
            self.SkillExecute(self.MouseXN, self.MouseYN,
                              self.colorN_start, "n", 1)
            self.BuffCheck = 0

        self.SkillExecute(self.MouseXHP, self.MouseYHP,
                          self.colorHP_start, 5, 1, "HP")
        self.SkillExecute(self.MouseXMP, self.MouseYMP,
                          self.colorMP_start, 6, 1, "MP")
        self.SkillExecute(self.MouseX1, self.MouseY1,
                          self.color1_start, 1, self.SkillEnable1)
        self.SkillExecute(self.MouseX2, self.MouseY2,
                          self.color2_start, 2, self.SkillEnable2)
        self.SkillExecute(self.MouseX3, self.MouseY3,
                          self.color3_start, 3, self.SkillEnable3)
        self.SkillExecute(self.MouseX4, self.MouseY4,
                          self.color4_start, 4, self.SkillEnable4)
        ahk.key_up('Control')
        # KeyPressControl = "False"
        # ControlHold()
        return

    def NoMainTask(self):
        self.SkillExecute(self.MouseXHP, self.MouseYHP,
                          self.colorHP_start, 6, 1, "HP")
        self.SkillExecute(self.MouseXMP, self.MouseYMP,
                          self.colorMP_start, 5, 1, "MP")
        return

    def CheckAnyKeyPress(self):
        KeyPressSpace = ahk.key_state('Control')
        KeyPressControl = ahk.key_state('Control')
        KeyPressUp = ahk.key_state('Control')
        KeyPressDown = ahk.key_state('Control')
        KeyPressRight = ahk.key_state('Control')
        KeyPressLeft = ahk.key_state('Control')
        if (KeyPressSpace is True
                or KeyPressControl is True
                or KeyPressUp is True
                or KeyPressDown is True
                or KeyPressRight is True
                or KeyPressLeft is True):
            self.AnyKeyPress = 1
            CountDownTime = 0
            if ((KeyPressRight is True or KeyPressLeft is True)
                    and (KeyPressUp is False)
                    and (KeyPressControl is False)
                    and (self.PickUpEnable is False)):
                ControlHold()
        else:
            if CountDownTime >= 5:
                self.AnyKeyPress = 0
            else:
                self.AnyKeyPress = 1
                CountDownTime += 1

def main():
    Bot = soulSaverBot()


if __name__ == '__main__':
    main()
