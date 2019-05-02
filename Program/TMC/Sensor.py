#!/usr/bin/python
import sys, Adafruit_DHT, re, os
from time import sleep
import RPi.GPIO as GPIO

REPETITIONS = 1         # how many times the measurement is repeated
INTERVAL = 3            # the pause between each iteration in seconds
light_limit = 200000    # maximum values of the light-value-variable

GPIO.setmode(GPIO.BCM)

def dht_measure(pin, reps=1):
    humidity, temperature = 0, 0
    for n in range(reps):
        hum_read, temp_read = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
        humidity += hum_read
        temperature += temp_read
        sleep(INTERVAL)
    humidity = round(humidity * 100 / reps) / (100)
    temperature = round(temperature * 100 / reps) / (100)
    return temperature, humidity

def dht_name(n=int):
    temp_name = "Temp_{}".format(n)
    hum_name = "Hum_{}".format(n)
    return temp_name, hum_name

def out_temp_measure(address, reps=1):
    temp = 0
    path = "/sys/bus/w1/devices/" + address + "/w1_slave"
    for n in range(reps):
        with open(path, "r") as file:
            read = file.readlines()

        while "NO\n" in read[0]:
            sleep(.25)
            with open(path, "r") as file:
                read = file.readlines()

        for read_line in read:
            if "t=" in read_line:
                nums = [float(s) for s in re.findall(r'-?\d+\.?\d*', read_line)]
                temp += nums[-1]
        sleep(INTERVAL)
    temp = round(temp / (10  * reps)) / (100)
    return temp

def light_measure(pin):
        value = 0
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        sleep(0.1)
        GPIO.setup(pin, GPIO.IN)
        while (GPIO.input(pin) == GPIO.LOW and value < light_limit):
            value += 1
        return value

class Dht22:

    def __init__(self, pins=[]):
        self.pins = pins
        self.names = [dht_name(n) for n, m in enumerate(pins)]
    
    def measure(self):
        for n in range(REPETITIONS):
            self.values = [dht_measure(pin, REPETITIONS) for pin in self.pins]

class OutdoorTemp:

    def __init__(self, addresses=[]):
        self.addresses = addresses
        self.names = ["OutdoorTemp_{}".format(n) for n, m in enumerate(addresses)]
        os.system("modprobe w1-gpio")
        os.system("modprobe w1-therm")

    def measure(self):
        for n in range(REPETITIONS):
            self.values = [out_temp_measure(address, REPETITIONS) for address in self.addresses]

class Light: 

    def __init__(self, pins=[]):
        self.pins = pins
        self.names = ["Light_{}".format(n) for n, m in enumerate(pins)]

    def measure(self):
        for n in range(REPETITIONS):
            self.values = [light_measure(pin) for pin in self.pins]