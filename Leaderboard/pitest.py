# from csh_ldap import *
import RPi.GPIO as GPIO
import time
# from Leaderboard.__main__ import read_button

print("Running")
# instance = CSHLDAP("leaderboard", "reprimand5075$namely")
# ibutton1 = read_button()
# print(instance.get_member_ibutton(ibutton1))
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    input1 = GPIO.input(4)
    input2 = GPIO.input(21)
    if input1 == False:
        print("Button 1 Pressed!")
        time.sleep(0.2)
        while input1 == False:
            input1 = GPIO.input(4)
            time.sleep(0.2)
    if input2 == False:
        print("Button 2 Pressed!")
        time.sleep(0.2)
        while input2 == False:
            input2 = GPIO.input(21)
            time.sleep(0.2)
