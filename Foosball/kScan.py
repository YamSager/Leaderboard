import os
import random
import time
import RPi.GPIO as GPIO
import get_ibutton
import mail_sender

GPIO.setmode(GPIO.BCM)

try:
    GPIO.cleanup()

except:

    pass


def main():

    get_ibutton.init()


    GPIO.setup(24, GPIO.OUT)
    base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
    delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'
    GPIO.output(24, True)
    start_time = time.time()

    while True:

        tick = time.time()
        if tick == start_time + 604800:

            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tick)))

            start_time = time.time()
            user_dirs = os.popen("ls /scans").read()
            folders = user_dirs.split()

            for each in folders:
                if each == "TMP":
                    pass
                else:
                    os.system("rm -rf /scans/" + each)
                    mail_sender.goodbyeMail(each)

            os.system("mkdir /scans/TMP")

        data = open(base_dir, "r")
        ibutton = data.read()
        ibutton = ibutton.strip()
        data.close()

        if ibutton != 'not found.\n':
            GPIO.output(24, False)
            time.sleep(1)
            print(ibutton)

            try:
                user = get_ibutton.find_user(ibutton[3:] + "01")
                if user is None:
                    print("Cannot scan, ldap didn't give me a user")
                else:
                    print("iButton read! you must be " + user)
                    file_name = takeScan(user)

                    mail_sender.sendMail(file_name, user)

                    print("scan saved as" + file_name)

            except Exception as e:
                print(e)
                print("Captain, I'm afraid the ship is sinking")

            d = open(delete_dir, "w")
            d.write(ibutton)
            GPIO.output(24, True)

    d.close()
    GPIO.cleanup()


def saveDoc(file_name, user):

    directory = os.popen("ls /scans/").read()
    folders = directory.split()

    if user not in folders:

        os.system("mkdir /scans/" + user)
        os.system("mv /scans/TMP/" + file_name + " /scans/" + user + "/")

    else:

        os.system("mv /scans/TMP/" + file_name + " /scans/" + user + "/")


    print("File saved in /scans/" + user)


def takeScan(user):

    file_name = user + "_" + str(random.randint(0, 100)) + "_scan.jpg"

    os.system("scanimage --resolution 300 -x 215 -y 279 > /scans/TMP/" + file_name)

    os.system("mogrify -resize 90% /scans/TMP/" + file_name)

    saveDoc(file_name, user)

    return file_name


if __name__ == "__main__":

    main()

