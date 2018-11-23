import spidev
import time
import os
from time import sleep
import minimalmodbus
import serial
import requests
from datetime import datetime as date
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import serial
from ina219 import INA219
try:
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
except:
    pass 
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16, GPIO.OUT)
a=0
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave add$ 
except:
    pass
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB1', 1) # port name, slave add$ 
except:
    pass
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB2', 1) # port name, slave add$ 
except:
    pass
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB3', 1) # port name, slave add$ 
except:
    pass
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB4', 1) # port name, slave add$ 
except:
    pass
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB5', 1) # port name, slave add$ 
except:
    pass
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB6', 1) # port name, slave add$ 
except:
    pass
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB7', 1) # port name, slave add$ 
except:
    pass
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB8', 1) # port name, slave add$ 
except:
    pass
try:
    SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB9', 1) # port name, slave add$ 
except:
    pass
print(SharkMeter)
t=0
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

    S_1 = ((((S1/m)+7)*(5.0/1023))-2.5)/(0.095)
    S_2 = ((((S2/m)+5)*(5.0/1023))-2.5)/(0.063)
    S_3 = ((((S3/m)+5)*(5.0/1023))-2.5)/(0.090)
    S_4 = ((((S4/m)+5)*(5.0/1023))-2.5)/(0.095)
    S_5 = ((((S5/m)+5)*(5.0/1023))-2.5)/(0.088)
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
	    ctrl=str(1)

    elif (S_1>0.5 or S_2>0.5 and S_5>0.09): 
	    GPIO.output(16, True)
	    print("Carga conectada")
	    ctrl=str(0)
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
    
    If = i+i1+i2+i3
    Pf = str(round(If*S_6,2))
    Vp = ((2.5+S_2*0.1)*6)
    Pp = str(round((Vp)*S_2,2))
    Ib = S_5-S_3
    Pb = str(abs(round((S_8+1)*Ib,2)))
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
    n=0
    while  n<50:
	## Voltaje de linea A con linea B
	try:
            fVoltageAB = SharkMeter.read_float(1005,3,2)
            VNAB = str(round(fVoltageAB/210.0,2))
	    VoltageAB = str(round(fVoltageAB,2))
            print("Voltaje linea A-B = "+VoltageAB)
            
	
    	except:
            VoltageAB = set()
       

    ## Voltaje de linea B con linea C
    	try:
            fVoltageBC=SharkMeter.read_float(1007,3,2)
            VNBC = str(round(fVoltageBC/210.0,2))
	    VoltageBC=str(round(fVoltageBC,2))
	    print("Voltaje linea B-C = "+VoltageBC)
	
    	except:
            VoltageBC = set()
        
	## Voltaje de linea C con linea A
    	try:
	    fVoltageCA=SharkMeter.read_float(1009,3,2)
	    VNCA = str(round(fVoltageCA/210.0,2))
	    VoltageCA=str(round(fVoltageCA,2))
	    print("Voltaje linea C-A = "+VoltageCA)
	
    	except:
            VoltageCA = set()
        
	
	## Voltaje de linea A con Neutro
    	try:
            fVoltageA = SharkMeter.read_float(999,3,2)
	    VoltageA = str(round(fVoltageA,2))
	    print("Voltaje linea A-N = "+VoltageA)
	
    	except:
            VoltageA = set()

	## Voltaje de linea B con Neutro
    	try:
            fVoltageB=SharkMeter.read_float(1001,3,2)
	    VoltageB=str(round(fVoltageB,2))
	    print("Voltaje linea B-N = "+VoltageB)
	
    	except:
            VoltageB = set()
        
	## Voltaje de linea C con Neutro
    	try:
            fVoltageC=SharkMeter.read_float(1003,3,2)
	    VoltageC=str(round(fVoltageC,2))
	    print("Voltaje linea C-N = "+VoltageC)
	
    	except:
            VoltageC = set()
       
	##Corriente de linea A
    	try:
            fAmpA = SharkMeter.read_float(1011,3,2)
	    AmpA=str(round(fAmpA,2))
	    print("Corriente A = "+AmpA)
	
    	except:
            AmpA = set()
        

	##Corriente de linea B
    	try:
	    fAmpB = SharkMeter.read_float(1013,3,2)
	    AmpB=str(round(fAmpB,2))
	    print("Corriente B = "+AmpB)
		
    	except:
            AmpB = set()
        	

	##Corriente de linea C
    	try:
	    fAmpC = SharkMeter.read_float(1015,3,2)
	    AmpC=str(round(fAmpC,2))
	    print("Corriente C = "+AmpC)
	
    	except:
            AmpC = set()
        	

	##Potencia Activa
    	try:
	    fWatt = SharkMeter.read_float(1017,3,2)
	    Watt=str(round((fWatt/1000.0),3))
	    print("Potencia Activa Total = "+Watt)
	
    	except:
            Watt = set()
        

	##Energia Activa
    	try:
	    fwatth = SharkMeter.read_long(1105,3,True)*10
	    Watth=str(fwatth/1000.0)
	    print("Energia Activa Total = "+Watth)

    	except:
            Watth = set()
        
	
	##Potencia Reactiva
    	try:
	    fVar = SharkMeter.read_float(1019,3,2)
	    Var = str(round((fVar/1000.0),3))
	    print("Potencia Reactiva Total = "+Var)
    	except:
            Var = set()
        

	##Energia Reactiva
    	try:
	    fVarh = SharkMeter.read_long(1113,3,True)*10
	    Varh=str((fVarh/1000.0))
	    print("Energia Reactiva Total = "+Varh)
	
    	except:
            Varh = set()
        

	##Potencia Aparente
    	try:
	    fVas = SharkMeter.read_float(1021,3,2)
	    Vas = str(round((fVas/1000.0),3))
	    print("Potencia Aparente Total = "+Vas)
	
    	except:
            Vas = set()
        

	##Energia Aparente
    	try:
	    fVash = SharkMeter.read_long(1115,3,True)*10
	    Vash=str(fVash/1000.0)
	    print("Energia Aparente Total = "+Vash)
	
    	except:
            Vash = set()
        

	##Factor de potencia
    	try:
	    fFp = SharkMeter.read_float(1023,3,2)
	    Fp = str(round(fFp,2))
	    print("Factor Potencia = "+Fp)
	
    	except:
            Fp = set()
        

	##Frecuencia
    	try:
	    fFreq = SharkMeter.read_float(1025,3,2)
	    Freq = str(round(fFreq,2))
	    print("Frecuencia = "+Freq)
	
    	except:
            fFreq = set()
        

	## Angulo de corriente linea A
	try:
            fAmpPA = SharkMeter.read_register(4099,1,3,True)
            AmpPA = str(int(fAmpPA))
            print("Fase de corriente linea A = "+AmpPA)
	
    	except:
            AmpPA = set()
		

	## Angulo de corriente linea B
    	try:
            fAmpPB = SharkMeter.read_register(4100,1,3,True)
            if fAmpB!=0:
                fAmpPB = fAmpPB + 120
                AmpPB = str(int(fAmpPB))
                print("Fase de corriente linea B = "+AmpPB) 
            elif fAmpB==0:
                AmpPB = str(int(fAmpPB))
                print("Fase de corriente linea B = "+AmpPB)
		
    	except:
            AmpPB = set()
		

	## Angulo de corriente linea C
    	try:	
	    fAmpPC = SharkMeter.read_register(4101,1,3,True)
            if fAmpC!=0:
                fAmpPC = fAmpPC - 120
                AmpPC = str(int(fAmpPC))
                print("Fase de corriente linea C = "+AmpPC)
            elif fAmpC==0:
                AmpPC = str(int(fAmpPC))
                print("Fase de corriente linea C = "+AmpPC)
		
    	except:
            AmpPC = set()
			

	## Angulo entra fase A y B
    	try:	
	    fVABPhase = SharkMeter.read_register(4102,1,3,True) + 120
	    VABPhase = str(int(fVABPhase))
	    print("Fase de voltaje linea AB = "+VABPhase)
		
    	except:
            VABPhase = set()
        
	
	## Angulo entra fase B y C
    	try:	
	    fVBCPhase = SharkMeter.read_register(4103,1,3,True) + 240
	    VBCPhase = str(int(fVBCPhase)) 
	    print("Fase de voltaje linea BC = "+VBCPhase)
    	except:
            VBCPhase = set()
        
	
	## Angulo entra fase C y A
    	try:	
	    fVCAPhase = SharkMeter.read_register(4104,1,3,True)
	    VCAPhase=str(int(fVCAPhase))
	    print("Fase de voltaje linea CA = "+VCAPhase)
    	except:
            VCAPhase = set()
        print(n)
        if len(VCAPhase)!=0 and len(VABPhase)!=0 and len(VBCPhase)!=0 and len(AmpPA)!=0 and len(AmpPB)!=0 and len(AmpPC)!=0:
            break
        n=n+1
    t=t+1
    print(t)
    print(str(date.now()))
    try:
        response0 = requests.get('http://104.236.0.105:8080/line_voltages_phases?vab=%s&pab=%s&vbc=%s&pbc=%s&vca=%s&pca=%s&create=%s'%(VoltageAB, VABPhase, VoltageBC, VBCPhase, VoltageCA, VCAPhase,str(date.now())),
                        auth=requests.auth.HTTPBasicAuth(
                            'admin',
                            'uninorte'))
        response1 = requests.get('http://104.236.0.105:8080/phase_voltages?va=%s&vb=%s&vc=%s&create=%s'%(VoltageA, VoltageB, VoltageC, str(date.now())),
                        auth=requests.auth.HTTPBasicAuth(
                            'admin',
                            'uninorte'))
        response1_1 = requests.get('http://104.236.0.105:8080/line_voltages_nor?vab_n=%s&vbc_n=%s&vca_n=%s&create=%s'%(VNAB, VNBC, VNCA, str(date.now())),
                        auth=requests.auth.HTTPBasicAuth(
                            'admin',
                            'uninorte'))
        response2 = requests.get('http://104.236.0.105:8080/currents_phases?ca=%s&pa=%s&cb=%s&pb=%s&cc=%s&pc=%s&create=%s'%(AmpA, AmpPA, AmpB, AmpPB, AmpC, AmpPC,str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        response3 = requests.get('http://104.236.0.105:8080/frequency?freq=%s&pf=%s&create=%s'%(Freq,Fp,str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                                'admin',
                                'uninorte'))

        response4 = requests.get('http://104.236.0.105:8080/powers?watt=%s&var=%s&vas=%s&create=%s'%(Watt, Var, Vas, str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))

        response5 = requests.get('http://104.236.0.105:8080/energies?watth=%s&varh=%s&vash=%s&create=%s'%(Watth, Varh, Vash, str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
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
        response10 = requests.get('http://104.236.0.105:8080/control?state=%s&create=%s'%(ctrl, str(date.now())),
                            auth=requests.auth.HTTPBasicAuth(
                              'admin',
                              'uninorte'))
        print(response6)
        print(response7)
        print(response8)
        print(response9)
 
        print(response0)
        print(response1)
        print(response1_1)
        print(response2)
        print(response3)
        print(response4)
        print(response5)
        print(response10)
        time.sleep(50)
    except:
        time.sleep(10)