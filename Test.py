import spidev
import time
import os
import time

import minimalmodbus
import serial
import requests
from datetime import datetime as date
SharkMeter = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave add$ 
print(SharkMeter)

## Voltaje de linea A con linea B
fVoltageAB = SharkMeter.read_float(1005,3,2)
VoltageAB = str(fVoltageAB)
print("Voltaje linea A-B = "+VoltageAB)

## Voltaje de linea B con linea C
fVoltageBC=SharkMeter.read_float(1007,3,2)
VoltageBC=str(fVoltageBC)
print("Voltaje linea B-C = "+VoltageBC)

## Voltaje de linea C con linea A
fVoltageCA=SharkMeter.read_float(1009,3,2)
VoltageCA=str(fVoltageCA)
print("Voltaje linea C-A = "+VoltageCA)

## Voltaje de linea A con Neutro
fVoltageA = SharkMeter.read_float(999,3,2)
VoltageA = str(fVoltageA)
print("Voltaje linea A-N = "+VoltageA)

## Voltaje de linea B con Neutro
fVoltageB=SharkMeter.read_float(1001,3,2)
VoltageB=str(fVoltageB)
print("Voltaje linea B-N = "+VoltageB)

## Voltaje de linea C con Neutro
fVoltageC=SharkMeter.read_float(1003,3,2)
VoltageC=str(fVoltageC)
print("Voltaje linea C-N = "+VoltageC)

##Corriente de linea A
fAmpA = SharkMeter.read_float(1011,3,2)
AmpA=str(fAmpA)
print("Corriente A = "+AmpA)

##Corriente de linea B
fAmpB = SharkMeter.read_float(1013,3,2)
AmpB=str(fAmpB)
print("Corriente B = "+AmpB)

##Corriente de linea C
fAmpC = SharkMeter.read_float(1015,3,2)
AmpC=str(fAmpC)
print("Corriente C = "+AmpC)

##Potencia Activa
fWatt = SharkMeter.read_float(1017,3,2)
Watt=str(fWatt)
print("Potencia Activa Total = "+Watt)

##Energia Activa
fwatth = SharkMeter.read_float(1105,3,2)
Watth=str(fWatth)
print("Potencia Activa Total = "+Watth)

##Potencia Reactiva
fVar = SharkMeter.read_float(1019,3,2)
Var = str(fVar)
print("Potencia Reactiva Total = "+Var)

##Energia Reactiva
fVarh = SharkMeter.read_float(1113,3,2)
Varh=str(fVarh)
print("Potencia Activa Total = "+Varh)

##Potencia Aparente
fVas = SharkMeter.read_float(1021,3,2)
Vas = str(fVas)
print("Potencia Aparente Total = "+Vas)

##Energia Aparente
fVash = SharkMeter.read_float(1115,3,2)
Vash=str(fVash)
print("Potencia Activa Total = "+Vash)

##Factor de potencia
fFp = SharkMeter.read_float(1023,3,2)
Fp = str(fFp)
print("Factor Potencia = "+Fp)

##Frecuencia
fFreq = SharkMeter.read_float(1025,3,2)
Freq = str(fFreq)
print("Frecuencia = "+Freq)

## Angulo de corriente linea A
fAmpPA = SharkMeter.read_register(4099,2,3,True)
AmpPA = str(fAmpPA)
print("Fase de corriente linea A = "+AmpPA)

## Angulo de corriente linea B
fAmpPB = SharkMeter.read_register(4100,2,3,True)
AmpPB = str(fAmpPB)
print("Fase de corriente linea B = "+AmpPB)

## Angulo de corriente linea C
fAmpPC = SharkMeter.read_register(4101,2,3,True)
AmpPC = str(fAmpPC)
print("Fase de corriente linea C = "+AmpPC)

## Angulo entra fase A y B
fVABPhase = SharkMeter.read_register(4102,2,3,True)
VABPhase = str(fVABPhase)
print("Fase de voltaje linea AB = "+VABPhase)

## Angulo entra fase B y C
fVBCPhase = SharkMeter.read_register(4103,2,3,True)
VBCPhase = str(fVBCPhase)
print("Fase de voltaje linea BC = "+VBCPhase)

## Angulo entra fase C y A
fVCAPhase = SharkMeter.read_register(4104,2,3,True)
VCAPhase=str(fVCAPhase)
print("Fase de voltaje linea CA = "+VCAPhase)