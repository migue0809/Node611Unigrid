from time import sleep
from ina219 import INA219
import time
t=0
while True:
    ina1 = INA219(shunt_ohms=0.1,
                  max_expected_amps = 2.0,
                  address=0x40)
    ina2 = INA219(shunt_ohms=0.1,
                 max_expected_amps = 2.0,
                 address=0x41)
    ina3 = INA219(shunt_ohms=0.1,
                 max_expected_amps = 2.0,
                 address=0x44)
    ina4 = INA219(shunt_ohms=0.1,
                  max_expected_amps = 2.0,
                  address=0x45) 
    ina1.configure(voltage_range=ina1.RANGE_32V,
                   gain=ina1.GAIN_AUTO,
                   bus_adc=ina1.ADC_128SAMP,
                   shunt_adc=ina1.ADC_128SAMP)
    ina2.configure(voltage_range=ina2.RANGE_32V,
                  gain=ina2.GAIN_AUTO,
                  bus_adc=ina2.ADC_128SAMP,
                  shunt_adc=ina2.ADC_128SAMP)
    ina3.configure(voltage_range=ina3.RANGE_32V,
                  gain=ina3.GAIN_AUTO,
                  bus_adc=ina3.ADC_128SAMP,
                  shunt_adc=ina3.ADC_128SAMP)
    ina4.configure(voltage_range=ina4.RANGE_32V,
                   gain=ina4.GAIN_AUTO,
                   bus_adc=ina4.ADC_128SAMP,
                  shunt_adc=ina4.ADC_128SAMP)
    t=t+1
    print(t)
    v1  = ina1.voltage()
    i1 = ina1.current()/1000
    p1 = ina1.power()
    print("Voltage Sensor 1= "+str(v1))   
    print("Current Sensor 1= "+str(i1))   
    print("Power Sensor 1= "+str(p1))
    v2  = ina2.voltage()
    i2 = ina2.current()/1000
    p2 = ina2.power()
    print("Voltage Sensor 2= "+str(v2))   
    print("Current Sensor 2= "+str(i2))   
    print("Power Sensor 2= "+str(p2))
    v3  = ina3.voltage()
    i3 = ina3.current()/1000
    p3 = ina3.power()
    print("Voltage Sensor 3= "+str(v3))   
    print("Current Sensor 3= "+str(i3))   
    print("Power Sensor 3= "+str(p3))
    v4 = ina4.voltage()
    i4 = ina4.current()/1000
    p4 = ina4.power()
    print("Voltage Sensor 4= "+str(v4))   
    print("Current Sensor 4= "+str(i4))   
    print("Power Sensor 4= "+str(p4)) 
    time.sleep(15)