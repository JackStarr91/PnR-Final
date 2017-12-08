import pigo
import time  # import just in case students need
import datetime
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        self.start_time = datetime.datetime.utcnow()
        self.next_right = True
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 83
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 35
        self.HARD_STOP_DIST = 20
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 125
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 128
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()

    def switch_turn(self,enc):
        if self.next_right:
            if not self.something_to_my_right():
                self.encR(enc)
            else:
                self.encB(2)


        else:
            if not self.something_to_my_left():
                self.encL(enc)
            else:
                self.encB(2)
        self.next_right = not self.next_right

    def something_to_my_right(self):
        self.servo(self.MIDPOINT - 40)
        time.sleep(.5)
        dist = self.dist()
        self.servo(self.MIDPOINT)
        return dist < self.HARD_STOP_DIST

    def something_to_my_left(self):
        self.servo(self.MIDPOINT + 40)
        time.sleep(.5)
        dist = self.dist()
        self.servo(self.MIDPOINT)
        return dist > self.HARD_STOP_DIST





    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "s": ("Check status", self.status),
                "q": ("Quit", quit_now),
                "t": ("Test restore heading", self.restore_heading)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])

        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()






    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        print("\n---- LET'S DANCE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE
        if self.safety_check():
            self.to_the_right()
            self.to_the_left()
            self.back_it_up()
            #self.hit_the_quan()
            #    self.walk_it_by_yourself()

    def safety_check(self):
        self.servo(self.MIDPOINT)  # Looks straight ahead
        for x in range(4):
            if not self.is_clear():
                return False
            print("Check Distance")
            self.encR(8)
        print("Safe to dance!")
        return True


                #loop 3 times
        # turn 90 deg
        # scan again

  #  def to_the_right(self):
     #   """subroutine of dance method"""
      #  for x in range(3):
       #     self.encR(5)
        #    self.encF(10)

    def to_the_left(self):
        for x in range(3):
            self.encL(10)
            self.encB(5)

    def back_it_up(self):
        for x in range(3):
            self.encR(5)
            self.encB(10)
            self.encL(5)
            self.encF(15)
            self.encB(15)




#Robot should find a way to navigate forward without moving into an object


    def restore_heading(self):
        """
          Uses self.turn_track to reorient original heading
        """
        print("Restoring heading!")
        if self.turn_track > 0:
            self.encL(abs(self.turn_track))
        elif self.turn_track < 0:
            self.encR(abs(self.turn_track))

    def test_restore_heading(self):
        self.encR(5)
        self.encL(15)
        self.encR(10)
        self.encR(10)
        self.encL(7)
        self.restore_heading()

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        right_now = datetime.datetime.utcnow()
        difference = (right_now - self.start_time).seconds
        print ("It took you %d seconds to run this" % difference)
        # I want my robot to navigate without stopping in the middle
        count = 0
        while True:
            if self.is_clear():
                count = 0
                self.cruise()
            else:
                self.switch_turn(9)
                count += 1
                if count > 2:
                    self.switch_turn(12)

            #I want my robot to look twice on both sides for an opening, if it does not see one, I want the robot to make a wide switch_turn


    def smooth_turn(self):
        self.right_rot()
        start = datetime.datetime.utcnow()
        self.servo(self.MIDPOINT)
        while True:
            if self.dist() > 100:
                self.stop()
            elif datetime.datetime.utcnow() - start > datetime.timedelta(seconds=10):
                self.stop()
        time.sleep(.1)

    def cruise(self):
        """drive straight while path is clear"""
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.1)
        self.stop()

####################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
