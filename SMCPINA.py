#import modules
import spidev
import time
import os
from math import *
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import serial
import requests
from datetime import datetime as date
from time import sleep
from ina219 import INA219

#Sensor and I2C configuration
ina = INA219(shunt_ohms=0.1,
             max_expected_amps = 2.0,
             address=0x40)

ina1 = INA219(shunt_ohms=0.1,
             max_expected_amps = 2.0,
             address=0x44)

ina2 = INA219(shunt_ohms=0.1,
             max_expected_amps = 2.0,
             address=0x41)

ina3 = INA219(shunt_ohms=0.1,
             max_expected_amps = 2.0,
             address=0x45)

ina.configure(voltage_range=ina.RANGE_32V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

ina1.configure(voltage_range=ina.RANGE_32V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

ina2.configure(voltage_range=ina.RANGE_32V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)

ina3.configure(voltage_range=ina.RANGE_32V,
              gain=ina.GAIN_AUTO,
              bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP)
#Configuration SPI Port and device
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#Configuration pin output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16, GPIO.OUT)
a=0
#Cycle for to take measures
while True:
    #Initialization of sensors
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
        #Reading of each adc channel
	A1 = mcp.read_adc(2)
	A2 = mcp.read_adc(7)
	A3 = mcp.read_adc(3)
	A4 = mcp.read_adc(1)
	A5 = mcp.read_adc(0)
	V1 = mcp.read_adc(4)
	V2 = mcp.read_adc(5)
	V3 = mcp.read_adc(6)
	#Sum of each measure
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
    #Value for zero adjustment of the sensors
    Aju=12
    #Conversion of digital value to analog
    S_1 = (((((S1/m)-Aju)*(5.0/1023))-2.5)/(0.115))
    S_2 = (((((S2/m)-Aju)*(5.0/1023))-2.5)/(0.115))
    S_3 = (((((S3/m)-Aju)*(5.0/1023))-2.5)/(0.091))
    S_4 = (((((S4/m)-Aju)*(5.0/1023))-2.5)/(0.115))
    S_5 = (((((S5/m)-Aju)*(5.0/1023))-2.5)/(0.092))
    S_6 = (((S6/m)*(5.0/1023))*(37000.0/7500.0))*14.5 
    S_7 = (((S7/m)*(5.0/1023))*(37000.0/7500.0))*12.5
    S_8 = ((S8/m)*(5.0/1023))*(37000.0/7500.0)
    
    p = 1.0
    #Adjustment of source voltage sensor due to failure of a source
    while (p<10.0):
        if (S_1>(p+0.5) and S_1<(p+1.5)):
            S_6 = S_6+(2*p)
            S_7 = S_7-(1.5*p)
            S_8 = S_8-(p+1)/2
            break
        p=p+1.0
    #Condition that Current sensor of the first buck is zero, the voltage of the sources is zero
    if(S_1<0.05):
        S_6=0.0
    #Condition for disconnection of non-essential load
    #If the current sensor values of the first buck and the solar panel
    # are lower than a set value and the inverter sensor current is greater than a set value
    #you must disconnect the non-essential load
    if (S_1<0.5 and S_2<0.5 and S_5>0.09):
	    GPIO.output(16, False)
	    print("Carga desconectada")
    #If the current sensor values of the first buck or solar panel are higher
    #than a set value and the inverter sensor current is greater than a set value,
    #you must disconnect the non-essential load
    elif (S_1>0.5 or S_2>0.5 and S_5>0.09): 
	    GPIO.output(16, True)
	    print("Carga conectada")
    #Take values of each low current sensor
    v = ina.voltage()
    i = round(ina.current()/1000,2)
    p = ina.power()

    v1 = ina1.voltage()
    i1 = round(ina1.current()/1000,2)
    p1 = ina1.power()

    v2 = ina2.voltage()
    i2 = round(ina2.current()/1000,2)
    p2 = ina2.power()

    v3 = ina3.voltage()
    i3 = round(ina3.current()/1000,2)
    p3 = ina3.power()
    #Sum of the currents of each source
    If = i+i1+i2+i3
    #Power of the source
    Pf = str(round(If*S_6,2))
    #Calculation of panel voltage
    Vp = ((2.5+S_2*0.1)*6)
    #Power of the panel
    Pp = str(round(Vp*S_2,2))
    #Calculation of battery current
    Ib = S_5-S_3+S_4
    #Power of the battery
    Pb = str(abs(round(S_8*Ib,2)))
    #Conversion to string
    i=str(i)
    i1=str(i1)
    i2=str(i2)
    i3=str(i3)
    S_1=str(round(S_1,2))
    S_2=str(round(S_2,2))
    S_3=str(round(S_3,2))
    S_4=str(round(S_4,2))
    S_5=str(round(S_5,2))
    S_6=str(round(S_6,2))
    S_7=str(round(S_7,2))
    S_8=str(round(S_8,2))
    #Print values of each sensor
    #Sensors viewed from left to right and from bottom to top
    print("Corriente sensor 1 = "+i)   ## Sensor de corriente 1 de I2C
    print("Corriente sensor 2 = "+i1)	## Sensor de corriente 2 de I2C
    print("Corriente sensor 3 = "+i2)	## Sensor de corriente 3 de I2C
    print("Corriente sensor 4 = "+i3)	## Sensor de corriente 4 de I2C

    print("Voltaje sensor 1 = "+S_6)	## Sensor 1 de ADC  Canal 4
    print("Corriente sensor 5 = "+S_1)	## Sensor 2 de ADC  Canal 2
    print("Corriente sensor 6 = "+S_2)	## Sensor 3 de ADC  Canal 7
    print("Voltaje sensor 2 = "+S_7)	## Sensor 4 de ADC  Canal 5
    print("Corriente sensor 7 = "+S_3)	## Sensor 5 de ADC  Canal 3
    print("Corriente sensor 8 = "+S_4)	## Sensor 6 de ADC  Canal 1
    print("Corriente sensor 9 = "+S_5)	## Sensor 7 de ADC  Canal 0
    print("Voltaje sensor 3 = "+S_8)	## Sensor 8 de ADC  Canal 6
    print("Potencia de la fuente = "+Pf)
    print("Potencia del panel = "+Pp)
    print("Potencia de la bateria = "+Pb)
    a=a+1	
    print("Iteracion ="+str(a))
    #Sending to the database
    try:
        response6 = requests.get('http://104.236.0.105:8080/voltage_sensors?voltage1=%s&voltage2=%s&voltage3=%s&create=%s'%(S_6,S_7,S_8, str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        response7 = requests.get('http://104.236.0.105:8080/low_current_sensors?current1=%s&current2=%s&current3=%s&current4=%s&create=%s'%(i, i1, i2, i3,str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        response8 = requests.get('http://104.236.0.105:8080/high_current_sensors?current5=%s&current6=%s&current7=%s&current8%s&current9=%s&create=%s'%(S_1,S_2,S_3,S_4,S_5,str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        response9 = requests.get('http://104.236.0.105:8080/node_powers?batteries=%s&red=%s&panel=%s&create=%s'%(Pb,Pf,Pp, str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        print(response6)
        print(response7)
        print(response8)
        print(response9)
        time.sleep(30)
    except:
        time.sleep(10)
    