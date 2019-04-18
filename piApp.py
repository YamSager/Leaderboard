import requests
import json
import time
import RPi.GPIO as GPIO

button1GPIO = 17
button2GPIO = 21
onewireGPIO = 4

def play_game():
    score1 = 0
    score2 = 0
    GPIO.setup(button1GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button1GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while score1 < 10 and score2 < 10:
        input1 = GPIO.input(button1GPIO)
        input2 = GPIO.input(button2GPIO)
        if input1 == False:
            score1 += 1
            time.sleep(0.2)
            while input1 == False:
                input1 = GPIO.input(button1GPIO)
                time.sleep(0.2)
        if input2 == False:
            score2 += 1
            time.sleep(0.2)
            while input2 == False:
                input2 = GPIO.input(button2GPIO)
                time.sleep(0.2)
    return score1, score2


def read_button():
    start = time.time()
    end = start
    GPIO.setup(onewireGPIO, GPIO.OUT)
    base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
    delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'
    GPIO.output(onewireGPIO, True)
    while start - end < 60: # 60 second timeout
        data = open(base_dir, "r")
        ibutton = data.read()
        ibutton = ibutton.strip()
        data.close()
        d = open(delete_dir, "w")
        if not "not" in ibutton:
            GPIO.output(onewireGPIO, False)
            #print("*" + ibutton[3:] + "01")
            d.write(ibutton)
            d.flush()
            GPIO.output(onewireGPIO, True)
            return "*" + ibutton[3:] + "01"
        end = time.time()
    return None


def main():
    GPIO.setmode(GPIO.BCM)
    while True:
        member1 = read_button()
        print(member1)
        member2 = read_button()
        print(member2)
        if member1 is not None and member2 is not None and member1 != member2:
            print("Game in progress")
            score1, score2 = play_game()
            jsonObj = json.dumps('{{"player1":{}, "player2":{}, "score1":{}, "score2":{}}}'.format('"'+ member1 + '"', '"'+ member2 + '"', score1, score2))
            r = requests.post(address, json=jsonObj)
        else:
            print("User not found")
main()
