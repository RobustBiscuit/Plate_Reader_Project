#Author: Irshaad Dodia
#EEE4022F
#Plate Reader Project

#Description: This script manages the LED and PT array, sequentially sampling each well
#of the 96 well array at a given time interval.

#Features to add: -No chip select on MUX, find a way to 'turn off' MUX when not in use

#import required libraries
import RPi.GPIO as GPIO
import time
from datetime import datetime

import Adafruit_MCP3008 #this uses the MCP3008 10-bit ADC

import csv
import matplotlib.pyplot as plt
import numpy as np

import os
import glob

#configuration
plt.ion()
x=[]
y=[]

GPIO.setmode(GPIO.BCM)   #Broadcom Pin Configuration
GPIO.setwarnings(False)


#output pins for MUX selection
#MUX 1 - controls ROWS, A,B,C
GPIO.setup(13,GPIO.OUT) #a
GPIO.setup(19,GPIO.OUT) #b
GPIO.setup(26,GPIO.OUT) #c
#MUX 2 - controlls COLS, I thru VI
GPIO.setup(16,GPIO.OUT) #a
GPIO.setup(20,GPIO.OUT) #b
GPIO.setup(21,GPIO.OUT) #c

#ADC SPI Configuration
SPICLK = 11 #green
SPIMISO = 9 #white
SPIMOSI = 10  #grey
SPICS = 8 #yellow

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

#Variable Declerations
adcPin = 0 #data in pin on ADC

GreenLED = 22
RedLED = 27

GPIO.setup(GreenLED, GPIO.OUT)
GPIO.setup(RedLED, GPIO.OUT)

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
    
    for i in range(1,19):
        print("LED: " + str(i))
        choose(i)
        time.sleep(0)
        input("enter to cont")
        
def takeReadings(numSamples, readingDelay, path, readingType):
    """Iterates through each LED/PT pair, takes specified number of samples (numSamples) readings, with a delay (readingDelay) between each reading
     computes the mean, and standard deviation of each well, and writes the resuling (numSamples+2)x18 Matrix. The additional 2 rows are for the mean and stdev calculation."""
    
    readingBuffer = [[None for i in range(numSamples)] for j in range(18)] #buffer list ot hold readings from ADC - 2D array

    for i in range(1,19):
        choose(i) #select LED/PT pair
        time.sleep(0.1) #delay to avoide switching noise 
        
        for j in range(numSamples): #take numSamples number of readings from chosen well
            readingBuffer[i-1][j] = mcp.read_adc(adcPin) #read from ADC
            #readingBuffer[i-1][j] = str(mcp.read_adc(adcPin)) 
            time.sleep(readingDelay) #time between readings
        
        #compute mean for row to 1 decimal place
        mean = round(np.mean(readingBuffer[i-1]),1)
        #append mean of row
        readingBuffer[i-1].append(mean) #we are appending to the original bufferArray, not the numpy numeric type
        #comput stdev to 1 decimal place
        stdev = round(np.std(readingBuffer[i-1]),1)
        #append standard deviation of row
        readingBuffer[i-1].append(stdev)
        
    #readingBuffer = np.transpose(readingBuffer) #transpose so that cols are well number and rows are readings
    
    
    outFileName = readingType + ".csv"

    with open(path+'/'+outFileName, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(readingBuffer) 
    writeFile.close()
    
    #print(readingBuffer)
    
def plotData(path):
	"""Plot a heatmap in a 6x3 matrix of the csv data given in path. Used for visualising readings after a test."""
    global numSamples
    
    Bmean, Bstdev = np.loadtxt(path+'/baseline.csv', unpack=True, delimiter=',',usecols=(numSamples,numSamples+1))
    Cmean, Cstdev = np.loadtxt(path+'/calibration.csv', unpack=True, delimiter=',',usecols=(numSamples,numSamples+1))
    Rmean, Rstdev = np.loadtxt(path+'/readings.csv', unpack=True, delimiter=',',usecols=(numSamples,numSamples+1))
    ODvalues = np.loadtxt(path+'/ODvalues.csv', unpack=True, delimiter=',')
    
    f=open(path+'/information.txt', 'r')
    content=f.read()
    f.close()
    
    wells = list(range(1,19))
    
    fig1,(ax1,ax2) = plt.subplots(1,2)
    fig1.set_figwidth(10)
    fig1.suptitle('additional information: '+ content)
    
    ax1.scatter(wells, ODvalues)
    ax1.set_title('OD reading from each Well')
    ax1.set(xlabel='Well number', ylabel="ODvalues", xticks=wells)
    for i,j in zip(wells,ODvalues):
        ax1.annotate(str(j),xy=(i,j))
    
    ax2.set_title('OD Readings Heatmap')
    ax2.imshow(np.reshape(ODvalues,(-1,6)), cmap='jet', interpolation='nearest')
    for i in range(3):
        for j in range(6):
            text = ax2.text(j, i, np.reshape(ODvalues,(-1,6))[i, j], ha="center", va="center", color="w")
    
    fig2,((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2,3)
    fig2.set_figwidth(20)
    fig2.set_figheight(8)
    fig2.suptitle('additional information: '+ content)
    
    ax1.set_title('Baseline Readings per Well')
    ax1.set(xlabel='Well Number', ylabel='ADC Reading Value - Baseline', xticks=wells)
    ax1.scatter(wells, Bmean)
    for i,j in zip(wells,Bmean):
        ax1.annotate(str(j),xy=(i,j))
    ax1.errorbar(wells, Bmean, yerr=Bstdev, fmt='o')
    
    ax2.set_title('Calibration Readings per Well')
    ax2.set(xlabel='Well Number', ylabel='ADC Reading Value - Calibration', xticks=wells)
    ax2.scatter(wells, Cmean)
    for i,j in zip(wells,Cmean):
        ax2.annotate(str(j),xy=(i,j))
    ax2.errorbar(wells, Cmean, yerr=Cstdev, fmt='o')
    
    ax3.set_title('Meaurement Readings per Well')
    ax3.set(xlabel='Well Number', ylabel='ADC Reading Valued - Measurement', xticks=wells)
    ax3.scatter(wells, Rmean)
    for i,j in zip(wells,Rmean):
        ax3.annotate(str(j),xy=(i,j))
    ax3.errorbar(wells, Rmean, yerr=Rstdev, fmt='o')
    
    ax4.set_title('Baseline Heatmap')
    ax4.imshow(np.reshape(Bmean,(-1,6)), cmap='jet', interpolation='nearest')
    for i in range(3):
        for j in range(6):
            text = ax4.text(j, i, np.reshape(Bmean,(-1,6))[i, j], ha="center", va="center", color="w")
            
    ax5.set_title('Calibration Heatmap')
    ax5.imshow(np.reshape(Cmean,(-1,6)), cmap='jet', interpolation='nearest')
    for i in range(3):
        for j in range(6):
            text = ax5.text(j, i, np.reshape(Cmean,(-1,6))[i, j], ha="center", va="center", color="w")
            
    ax6.set_title('Reading Heatmap')
    ax6.imshow(np.reshape(Rmean,(-1,6)), cmap='jet', interpolation='nearest')
    for i in range(3):
        for j in range(6):
            text = ax6.text(j, i, np.reshape(Rmean,(-1,6))[i, j], ha="center", va="center", color="w")
    
def toggleLED():
    global cont
    global red
    global green
    
    cont = not(cont)
    red = not(red)
    green = not(green)
    
    GPIO.output(GreenLED, green)
    GPIO.output (RedLED, red)
    
        
###################################################################################################
#Main Code
###################################################################################################
#Modes: 1 - Debug Mode testMatrix()
#       2 - Plot Mode (given path information, plots the data)
#       3 - Single test mode, takes a set of reading from all 18 wells, saves to file, and plots scatter plot and heatmap

MODE = 3

numSamples = 30 #number of samples per well
readingDelay = 0.1 #delay between each reading

if (MODE == 1):
    testMatrix()


elif (MODE==2):
    path='Plate_Readings/05092019_180435'
    plotData(path)

elif (MODE==3):

	#set local parameters
    cont = 0 	#counter
    red = 0		#redLED
    green = 1	#greenLED

    GPIO.output(GreenLED, green)
    GPIO.output(RedLED,red)

    input('Press Enter Key to Start...') #wait for user
    toggleLED()
    
    text = input('Enter OD of plate being read or any relavent information: ') #enter a useful description to help with data management later on

    now = datetime.now() #get timestamp

    #create a foldered for all the associated readings when the experiment is started
    path = r'Plate_Readings/' + now.strftime("%d%m%Y_%H%M%S")
    if not os.path.exists(path):
        os.makedirs(path)
    
    outFileName = "information.txt"

    with open(path+'/'+outFileName, 'w') as writeFile:
        writeFile.write(text)
    writeFile.close()

	#wait for user input
    toggleLED()
    input('Press Enter Key to Continue...')
    toggleLED()

	#take readings, with numSamples number of samples, readingDelay delay between each sample, and save to the identified path. The last parameter is used to identify the type of reading.
    takeReadings(numSamples, readingDelay, path, 'readings') #first parameter is numSamples, second parameter is readingDelay

    Rmean, Rstdev = np.loadtxt(path+'/readings.csv', unpack=True, delimiter=',',usecols=(numSamples,numSamples+1)) #compute mean and stdev

    wells = list(range(1,19))
    
	#open file and prepare for plotting
    f=open(path+'/information.txt', 'r')
    content=f.read()
    f.close()
    
	#configure plots
    fig1,(ax1,ax2) = plt.subplots(1,2)
    fig1.set_figwidth(10)
    fig1.suptitle('additional information: ' + content)
    
	#scatter plot
    ax1.scatter(wells, Rmean)
    ax1.set_title('Reading from each Well')
    ax1.set(xlabel='Well number', ylabel="Reading", xticks=wells)
    for i,j in zip(wells,Rmean):
        ax1.annotate(str(j),xy=(i,j))
		
    #heatmap
    ax2.set_title('Readings Heatmap')
    ax2.imshow(np.reshape(Rmean,(-1,6)), cmap='jet', interpolation='nearest')
    for i in range(3):
        for j in range(6):
            text = ax2.text(j, i, np.reshape(Rmean,(-1,6))[i, j], ha="center", va="center", color="w")

    
