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

def setMUX(MUX, a, b, c):
    """this function allows you to set the MUX selection by parsing either MUX 1 or 2 ,
        and the corresponding a,b,c commands (HIGH or LOW). Irshaad fix this doc string it is terrible"""
    
    if MUX==1: #ROWS: A,B,C
        GPIO.output(13, GPIO.a) #MUX 1a
        GPIO.output(19, GPIO.b) #MUX 1b
        GPIO.output(26, GPIO.c) #MUX 1c
        
        
    if MUX==2: #COLS: I,II,III,IV,V,VI
        GPIO.output(16, GPIO.a) #MUX 2a
        GPIO.output(20, GPIO.b) #MUX 2b
        GPIO.output(21, GPIO.c) #MUX 2c


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
    
    I = ("0","6","13")
    II = ("1","7","14")
    III = ("2","9","15")
    IV = ("3","10","16")
    V = ("4","11","17")
    VI = ("5","12","18")
    
    if sensor in A:
        setMUX(1, LOW, LOW, LOW) #CH0
        
    elif sensor in B:
        setMUX(1, LOW, LOW, HIGH) #CH1
        
    elif sensor in C:
        setMUX(1, LOW, HIGH, LOW) #CH2
        
        
    if sensor in I:
        setMUX(2, LOW, LOW, LOW) #CH0
        
    elif sensor in II:
        setMUX(2, LOW, LOW, HIGH) #CH1
        
    elif sensor in III:
        setMUX(2, LOW, HIGH, LOW) #CH2
        
    elif sensor in IV:
        setMUX(2, LOW, HIGH, HIGH) #CH3
        
    elif sensor in V:
        setMUX(2, HIGH, LOW, LOW) #CH4
        
    elif sensor in VI:
        setMUX(2, HIGH, LOW, HIGH) #CH5
    