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
GPIO.setmode(GPIO.BCM)   #Broadcom Pin Configuration


#output pins for MUX selection
#MUX 1 - controls ROWS, A,B,C
GPIO.setup(13,GPIO.OUT) #a
GPIO.setup(19,GPIO.OUT) #b
GPIO.setup(26,GPIO.OUT) #c
#MUX 2 - controlls COLS, I thru VI
GPIO.setup(16,GPIO.OUT) #a
GPIO.setup(20,GPIO.OUT) #b
GPIO.setup(21,GPIO.OUT) #c

########################################################################################
#FUNCTION DECLARATIONS
########################################################################################

def setMUX(MUX, c, b, a):
    """this function allows you to set the MUX selection by parsing either MUX 1 or 2 ,
        and the corresponding a,b,c commands (HIGH or LOW). Irshaad fix this doc string it is terrible"""
    
    if MUX==1: #ROWS: A,B,C
        GPIO.output(13, a) #MUX 1a
        GPIO.output(19, b) #MUX 1b
        GPIO.output(26, c) #MUX 1c
        
        
    if MUX==2: #COLS: I,II,III,IV,V,VI
        GPIO.output(16, a) #MUX 2a
        GPIO.output(20, b) #MUX 2b
        GPIO.output(21, c) #MUX 2c


def choose(sensor):
    """This function allows you to choose an LED or PT (i.e. turning it ON) by parsing the
    appropriate LED or PT number, according to the diagram below. NOTE THE LED NUMBERING
      I   II  III  IV   V   VI
    A 1   2   3    4    5   6
    B 7   8   9   10   11   12  
    C 13  14  15  16   17   18
    
    currently this only supports a 3x6 matrix"""
    
    A = (1, 2, 3, 4, 5, 6)
    B = (7, 8, 9, 10, 11, 12)
    C = (13, 14, 15, 16, 17, 18)
    
    I = (1,7,13)
    II = (2,8,14)
    III = (3,9,15)
    IV = (4,10,16)
    V = (5,11,17)
    VI = (6,12,18)
    
    if sensor in A:
        setMUX(1, 0, 0, 0) #CH0
        
    elif sensor in B:
        setMUX(1, 0, 0, 1) #CH1
        
    elif sensor in C:
        setMUX(1, 0, 1, 0) #CH2
        
        
    if sensor in I:
        setMUX(2, 0, 0, 0) #CH0
        
    elif sensor in II:
        setMUX(2, 0, 0, 1) #CH1
        
    elif sensor in III:
        setMUX(2, 0, 1, 0) #CH2
        
    elif sensor in IV:
        setMUX(2, 0, 1, 1) #CH3
        
    elif sensor in V:
        setMUX(2, 1, 0, 0) #CH4
        
    elif sensor in VI:
        setMUX(2, 1, 0, 1) #CH5
        
def testMatrix():
    """This function tests the 3x6 matrix by choosing each LED/PT from 1 to 16 squentially with a 1sec delay"""
    
    for i in range(1,18):
        print("LED: " + str(i))
        choose(i)
        time.sleep(1)
        
        
###################################################################################################
#Main Code
###################################################################################################

testMatrix()

GPIO.cleanup()
    