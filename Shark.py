import spidev
import time
import os
from time import sleep

import minimalmodbus
import serial
import requests
from datetime import datetime as date


SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave add$ 
print(SharkMeter)
t=0
while True:
    n=0
    while  n<50:
	## Voltaje de linea A con linea B
	try:
            fVoltageAB = SharkMeter.read_float(1005,3,2)
	    VoltageAB = str(round(fVoltageAB,2))
            print("Voltaje linea A-B = "+VoltageAB)
            
	
    	except:
            VoltageAB = set()
       

    ## Voltaje de linea B con linea C
    	try:
            fVoltageBC=SharkMeter.read_float(1007,3,2)
	    VoltageBC=str(round(fVoltageBC,2))
	    print("Voltaje linea B-C = "+VoltageBC)
	
    	except:
            VoltageBC = set()
        
	## Voltaje de linea C con linea A
    	try:
	    fVoltageCA=SharkMeter.read_float(1009,3,2)
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
	    Watt=str(round(fWatt,2)/1000.0)
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
	    Var = str(round(fVar,2)/1000.0)
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
	    Vas = str(round(fVas,2)/1000.0)
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
 
        print(response0)
        print(response1)
        print(response2)
        print(response3)
        print(response4)
        print(response5)
        time.sleep(50)
    except:
        time.sleep(10)