import spidev
import os
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import time
import serial
import requests
from datetime import datetime as date
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
n=0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16, GPIO.OUT)
while True:
    S1 = 0
    S2 = 0
    S3 = 0
    S4 = 0
    S5 = 0
    S6 = 0
    S7 = 0
    S8 = 0
    t = 0
    while t<120:
    	A1 = mcp.read_adc(2)
	A2 = mcp.read_adc(7)
	A3 = mcp.read_adc(3)
	A4 = mcp.read_adc(1)
	A5 = mcp.read_adc(0)
	V1 = mcp.read_adc(4)
	V2 = mcp.read_adc(5)
	V3 = mcp.read_adc(6)
	
	S1 = S1 + A1
	S2 = S2 + A2
	S3 = S3 + A3
	S4 = S4 + A4
	S5 = S5 + A5
	S6 = S6 + V1
	S7 = S7 + V2
	S8 = S8 + V3
	t = t + 1
    
    m = 120
    print(S1/m)
    print(S2/m)
    print(S3/m)
    print(S4/m)
    print(S5/m)
    S_1 = ((((S1/m)-15)*(5.0/1023))-2.5)/(0.115)
    S_2 = ((((S2/m)-15)*(5.0/1023))-2.5)/(0.115)
    S_3 = ((((S3/m)-15)*(5.0/1023))-2.5)/(0.105)
    S_4 = ((((S4/m)-15)*(5.0/1023))-2.5)/(0.115)
    S_5 = ((((S5/m)-15)*(5.0/1023))-2.5)/(0.105)
    S_6 = (((S6/m)*(5.0/1023))*(37000.0/7500.0))*14.4594417077 
    S_7 = (((S7/m)*(5.0/1023))*(37000.0/7500.0))*13.4594417077	
    S_8 = ((S8/m)*(5.0/1023))*(37000.0/7500.0)
    p = 1.0
    while (p<10.0):
        if (S_1>p and S_1<(p+1.0)):
            S_6 = S_6+((3.2*p)-(p-1))
            S_7 = S_7-1.5*(p-1)
            S_8 = S_8-(p-1)/2
            break
        p=p+1.0
    if(S_1<0.05):
        S_6=0.0
    if (S_1<0.5 and S_2<0.5 and S_5>0.09):
	    GPIO.output(16, False)
	    print("Carga desconectada")

    elif (S_1>0.5 or S_2>0.5 and S_5>0.09): 
	    GPIO.output(16, True)
	    print("Carga conectada")
    print("Corriente sensor 1 = "+str(S_1))
    print("Corriente sensor 2 = "+str(S_2))
    print("Corriente sensor 3 = "+str(S_3))
    print("Corriente sensor 4 = "+str(S_4))
    print("Corriente sensor 5 = "+str(S_5))
    print("Voltaje sensor 6 = "+str(S_6))
    print("Voltaje sensor 7 = "+str(S_7))
    print("Voltaje sensor 8 = "+str(S_8))
    n=n+1
    print(n)
    time.sleep(1)