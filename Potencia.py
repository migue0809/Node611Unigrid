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
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
a=0
GPIO.output(20, False)
GPIO.output(26, True)
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
    i = round(ina.current()/1000,2)
    i1 = round(ina1.current()/1000,2)
    i2 = round(ina2.current()/1000,2)
    i3 = round(ina3.current()/1000,2)
    iajus=i+i1+i2+i3
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
    if (iajus<0.2):
        Aju=(S1/m)-513
    if (iajus>0.2):
        Aju=(S2/m)-513

    Aju=12
    S_1 = (((((S1/m)-Aju)*(5.0/1023))-2.5)/(0.115))
    S_2 = (((((S2/m)-Aju)*(5.0/1023))-2.5)/(0.115))
    S_3 = (((((S3/m)-Aju)*(5.0/1023))-2.5)/(0.091))
    S_4 = (((((S4/m)-Aju)*(5.0/1023))-2.5)/(0.115))
    S_5 = (((((S5/m)-Aju)*(5.0/1023))-2.5)/(0.092))
    S_6 = (((S6/m)*(5.0/1023))*(37000.0/7500.0))*14.5
    S_7 = (((S7/m)*(5.0/1023))*(37000.0/7500.0))*12.5
    S_8 = ((S8/m)*(5.0/1023))*(37000.0/7500.0)

    p = 1.0
    while (p<10.0):
        if (S_1>(p+0.5) and S_1<(p+1.5)):
            S_6 = S_6+(2*p)
            S_7 = S_7-(1.5*p)
            S_8 = S_8-(p+1)/2
            break
        p=p+1
    if(S_1<0.05):
        S_6=0.0
    if (S_1<0.2 and S_2<0.2 and S_5>0.09):
	    GPIO.output(16, False)
	    print("Carga desconectada")

    elif (S_1>0.2 or S_2>0.2 and S_5>0.09): 
	    GPIO.output(16, True)
	    print("Carga conectada")
    if (S_4>=0.35):
        GPIO.output(20, False)
        GPIO.output(26, True)
    elif (S_4<0.35):
        GPIO.output(26, False)
        GPIO.output(20, True)
   	if (S_5-S_3<=0.7):
       		 GPIO.output(26, False)
       		 GPIO.output(20, True)
    if (S_5-S_3>0.7):
        GPIO.output(20, False)
        GPIO.output(26, True)

    if(i<=0.0):
        i=0.01
    if(i1<=0.0):
        i1=0.01
    if(i2<=0.0):
        i2=0.01
    if(i3<=0.0):
        i3=0.01
    if(S_1<=0.0):
        S_1=0.01
    if(S_2<=0.0):
        S_2=0.01
    if(S_3<=0.0):
        S_3=0.01
    if(S_4<=0.0):
        S_4=0.01
    if(S_5<=0.0):
        S_5=0.01
    i4=S_1
    i5=S_2
    if S_3==S_4:
        i6=0.01
    else:
        i6=abs(S_3-S_4)
    i7=S_4
    i8=abs(S_5-S_3+S_4)
    If = i+i1+i2+i3
    Pf = str(round(If*S_6,2))
    Vp = ((2.5+S_2*0.1)*6)
    Pp = str(round(Vp*S_2,2))
    Ib = S_5-S_3
    Pb = str(abs(round(S_8*Ib,2)))
    VD0_AB=round(0.0326*log(i)+0.7812,3)
    VD1_AB=round(0.0326*log(i1)+0.7812,3)
    VD2_AB=round(0.0326*log(i2)+0.7812,3)
    VD3_AB=round(0.0326*log(i3)+0.7812,3)
    VD4_AB=round(0.0326*log(i4)+0.7812,3)
    VD5_AB=round(0.0326*log(i5)+0.7812,3)
    VD6_AB=round(0.0326*log(i6)+0.7812,3)
    VD7_AB=round(0.0326*log(i7)+0.7812,3)
    VD8_AB=round(0.0326*log(i8)+0.7812,3)
    
    VAD0=VD0_AB+S_6
    VAD1=VD1_AB+S_6
    VAD2=VD2_AB+S_6
    VAD3=VD3_AB+S_6
    VAD4=VD4_AB+S_7
    VAD5=VD5_AB+S_7
    VAD6=VD6_AB+S_8
    VAD8=VD8_AB+S_8
    print("Voltaje Diodo 0 "+str(VD0_AB))
    print("Voltaje Diodo 1 "+str(VD1_AB))
    print("Voltaje Diodo 2 "+str(VD2_AB))
    print("Voltaje Diodo 3 "+str(VD3_AB))
    print("Voltaje Diodo 4 "+str(VD4_AB))
    print("Voltaje Diodo 5 "+str(VD5_AB))
    print("Voltaje Diodo 6 "+str(VD6_AB))
    print("Voltaje Diodo 7 "+str(VD7_AB))
    print("Voltaje Diodo 8 "+str(VD8_AB))

    #Potencias antes de diodos
    PAD0=VAD0*i
    PAD1=VAD1*i1
    PAD2=VAD2*i2
    PAD3=VAD3*i3
    PAD4=VAD4*i4
    PAD5=VAD5*i5
    PAD6=VAD6*i6
    PAD7=VAD6*i7
    PAD8=VAD8*i8
    print("Potencia antes del Diodo 0 "+str(PAD0))
    print("Potencia antes del Diodo 1 "+str(PAD1))
    print("Potencia antes del Diodo 2 "+str(PAD2))
    print("Potencia antes del Diodo 3 "+str(PAD3))
    print("Potencia antes del Diodo 4 "+str(PAD4))
    print("Potencia antes del Diodo 5 "+str(PAD5))
    print("Potencia antes del Diodo 6 "+str(PAD6))
    print("Potencia antes del Diodo 7 "+str(PAD7))
    print("Potencia antes del Diodo 8 "+str(PAD8))
    #Potencias despues diodos
    PDD0=S_6*i
    PDD1=S_6*i1
    PDD2=S_6*i2
    PDD3=S_6*i3
    PDD4=S_7*i4
    PDD5=S_7*i5
    PDD6=S_8*i6
    PDD7=VAD8*i7
    PDD8=S_8*i8
    print("Potencia despues del Diodo 0 "+str(PDD0))
    print("Potencia despues del Diodo 1 "+str(PDD1))
    print("Potencia despues del Diodo 2 "+str(PDD2))
    print("Potencia despues del Diodo 3 "+str(PDD3))
    print("Potencia despues del Diodo 4 "+str(PDD4))
    print("Potencia despues del Diodo 5 "+str(PDD5))
    print("Potencia despues del Diodo 6 "+str(PDD6))
    print("Potencia despues del Diodo 7 "+str(PDD7))
    print("Potencia despues del Diodo 8 "+str(PDD8))

    PD1=str(round(VD1_AB*i1,3))
    PD2=str(round(VD2_AB*i2,3))
    PD3=str(round(VD3_AB*i3,3))
    PD4=str(round(VD4_AB*i4,3))
    PD5=str(round(VD5_AB*i5,3))
    PD6=str(round(VD6_AB*i6,3))
    PD7=str(round(VD7_AB*i7,3))
    PD8=str(round(VD8_AB*i8,3))
    VAfterBuck=round(S_7+VD4_AB,3)
    
    PBeforeBuck=Pf
    if If<0.1:
        S_1=0.0
    PAfterBuck=str(round((VAfterBuck*S_1),1))
    
        
    
    PBeforeBuck1=str(round((S_7*(i4+i5)),1))
    VAfterBuck1=round(S_8+VD6_AB,1)
    PAfterBuck1=str(round(VAfterBuck1*S_3,1))
    PBeforeInverter=str(round(S_8*S_5,1))

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
    
    fichero = open('Diodo0.txt', 'a')
    fichero.write(str(PAD0)+os.linesep)
    fichero.write(str(PDD0)+os.linesep)
    fichero.close()
    fichero1= open('Diodo1.txt', 'a')
    fichero1.write(str(PAD1)+os.linesep)
    fichero1.write(str(PDD1)+os.linesep)
    fichero1.close()
    fichero2= open('Diodo2.txt', 'a')
    fichero2.write(str(PAD2)+os.linesep)
    fichero2.write(str(PDD2)+os.linesep)
    fichero2.close()
    fichero3= open('Diodo3.txt', 'a')
    fichero3.write(str(PAD3)+os.linesep)
    fichero3.write(str(PDD3)+os.linesep)
    fichero3.close()
    fichero4= open('Diodo4.txt', 'a')
    fichero4.write(str(PAD4)+os.linesep)
    fichero4.write(str(PDD4)+os.linesep)
    fichero4.close()
    fichero5= open('Diodo5.txt', 'a')
    fichero5.write(str(PAD5)+os.linesep)
    fichero5.write(str(PDD5)+os.linesep)
    fichero5.close()
    fichero6= open('Diodo6.txt', 'a')
    fichero6.write(str(PAD6)+os.linesep)
    fichero6.write(str(PDD6)+os.linesep)
    fichero6.close()
    fichero7= open('Diodo7.txt', 'a')
    fichero7.write(str(PAD7)+os.linesep)
    fichero7.write(str(PDD7)+os.linesep)
    fichero7.close()
    fichero8= open('Diodo8.txt', 'a')
    fichero8.write(str(PAD8)+os.linesep)
    fichero8.write(str(PDD8)+os.linesep)
    fichero8.close()
    fichero9= open('Buck1.txt', 'a')
    fichero9.write(PBeforeBuck+os.linesep)
    fichero9.write(PAfterBuck+os.linesep)
    fichero9.close()
    fichero10= open('Buck2.txt', 'a')
    fichero10.write(PBeforeBuck1+os.linesep)
    fichero10.write(PAfterBuck1+os.linesep)
    fichero10.close()
    fichero11= open('Inverter.txt', 'a')
    fichero11.write(PBeforeInverter+os.linesep)
    fichero11.close()
        


    #Vistos de izquierda a derecha
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
    time.sleep(30)
