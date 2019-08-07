#Author: Irshaad Dodia
#EEE4022F
#Plate Reader Project

#Description: This script manages the LED and PT array, sequentially sampling each well
#of the 96 well array at a given time interval.

#Features to add: -No chip select on MUX, find a way to 'turn off' MUX when not in use

#import required libraries
import RPi.GPIO as GPIO
import time

#configuration
GPIO.setmode(BCM)   #Broadcom Pin Configuration


#output pins for MUX selection
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

########################################################################################
#FUNCTION DECLARATIONS
########################################################################################

def choose(sensor):
    """This function allows you to choose an LED or PT (i.e. turning it ON) by parsing the
    appropriate LED or PT number, according to the diagram below. NOTE THE LED NUMBERING
      I   II  III  IV   V   VI
    A 0   1   2   3    4    5  
    B 6   7   9   10   11   12  
    C 13  14  15  16   17   18
    
    currently this only supports a 3x6 matrix"""
    A = ("0", "1", "2", "3", "4", "5")
    B = ("6", "7", "8", "9", "10", "11")
    C = ("12", "13", "14", "15", "16", "17")
    
    I = ("","","")
    II = ("","","")
    III = ("","","")
    IV = ("","","")
    V = ("","","")
    VI = ("","","")
    