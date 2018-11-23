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
from Tkinter import *

root=Tk()
Frame=Frame(root,width=750,height=400)

imagen_de_fondo = PhotoImage(file="Esq.gif")
fondo = Label(root, image=imagen_de_fondo).place(x=0,y=0)

D0=StringVar()
D1=StringVar()
D2=StringVar()
D3=StringVar()
PBB=StringVar()
PAB=StringVar()
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
a=0
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

    S_1 = (((((S1/m)+7)*(5.0/1023))-2.5)/(0.090))
    S_2 = (((((S2/m)+6)*(5.0/1023))-2.5)/(0.063))+0.1
    S_3 = (((((S3/m)+7)*(5.0/1023))-2.5)/(0.075))
    S_4 = (((((S4/m)+7)*(5.0/1023))-2.5)/(0.095))
    S_5 = (((((S5/m)+7)*(5.0/1023))-2.5)/(0.083))
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
        p=p+1
    if(S_1<0.05):
        S_6=0.0
    if (S_1<0.5 and S_2<0.5 and S_5>0.09):
	    GPIO.output(16, False)
	    print("Carga desconectada")

    elif (S_1>0.5 or S_2>0.5 and S_5>0.09): 
	    GPIO.output(16, True)
	    print("Carga conectada")
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
    #VD0_AB=round(0.0565*Ln(i)+0.779,1)
##    VD1_AB=round(0.0565*log(i1)+0.779,1)
##    VD2_AB=round(0.0565*log(i2)+0.779,1)
##    VD3_AB=round(0.0565*log(i3)+0.779,1)
##    PD1=str(round(VD1_AB*i1,1))
##    PD2=str(round(VD2_AB*i2,1))
##    PD3=str(round(VD3_AB*i3,1))
    If = i+i1+i2+i3
    Pf = str(round(If*S_6,2))
##    V5_AB=round(0.0565*log(S_1)+0.779,1)
##    VAfterBuck=round(S_7+V5_AB,1)
##    PAfterBuck=str(round(VAfterBuck*S_1,1))
    Vp = ((2.5+S_2*0.1)*6)
    Pp = str(round(Vp*S_2,2))
    Ib = S_5-S_3
    Pb = str(abs(round(S_8*Ib,2)))
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
           #<<<<<<<< Cambiar
##    imagen_de_fondo = PhotoImage(file="Esq.gif")
##    fondo = Label(root, image=imagen_de_fondo)
    ##D0.set(PD0)
##    D1.set(PD1)
##    D2.set(PD2)
##    D3.set(PD3)
##    PBB.set(Pf)
##    PAB.set(PAfterBuck)
##    Sensor1Label=Label(Frame,text="PDiodo 1").grid(row=0, column=0)
##    cuadro1=Entry(Frame, textvariable=0).grid(row=0, column=1)
##    Sensor2Label=Label(Frame,text="PDiodo 2").grid(row=1, column=0)
##    cuadro2=Entry(Frame, textvariable=D1).grid(row=1, column=1)
##    Sensor3Label=Label(Frame,text="PDiodo 3").grid(row=2, column=0)
##    cuadro3=Entry(Frame, textvariable=D2).grid(row=2, column=1)
##    Sensor4Label=Label(Frame,text="PDiodo 4").grid(row=3, column=0)
##    cuadro4=Entry(Frame, textvariable=D3).grid(row=3, column=1)
##    Sensor5Label=Label(Frame,text="PAntesBuck ").grid(row=4, column=0)
##    cuadro5=Entry(Frame, textvariable=PBB).grid(row=4, column=1)
##    Sensor6Label=Label(Frame,text="PDespuesBuck ").grid(row=5, column=0)
##    cuadro6=Entry(Frame, textvariable=PAB).grid(row=5, column=1)
    
    root.title("Interfaz Nodo 611")
    Frame.pack()
    root.update()
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
    