# from csh_ldap import *
import RPi.GPIO as GPIO
from Leaderboard.__main__ import read_button

# instance = CSHLDAP("leaderboard", "reprimand5075$namely")
# ibutton1 = read_button()
# print(instance.get_member_ibutton(ibutton1))
GPIO.app_event_detect(7, GPIO.FALLING)
GPIO.app_event_detect(38, GPIO.FALLING)
while True:
    if GPIO.event_detected(7):
        print("Button 1 Pressed!")
    if GPIO.event_detected(38):
        print("Button 2 Pressed!")
