import RPi.GPIO as GPIO
import time
from SMCP.py import S1
from SMCP.py import S2
from SMCP.py import S5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16, GPIO.OUT)
while True:

	if (S1<0.09 and S2<0.09 and S5>0.09):
		GPIO.output(16, True)
		Print("Carga conectada")

	elif (S1>0.09 and S2>0.09 and S5<0.09): 
		GPIO.output(16, False)
		Print("Carga desconectada")

