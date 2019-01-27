#!/usr/bin/python
import RPi.GPIO as GPIO
from LcDisplay import LCDisplay
from Sensor import Dht22, Light, OutdoorTemp
from InputOutput import InputOutput
from time import sleep
from LED import LEDIndicator
from subprocess import call
from OnlinePush import OnlinePush

MEASURE_INTERVAL = 1                                        # interval in minutes
WRITE_INTERVAL = 10                                         # interval for writing to the file
UPTIME = 7                                                  # time in days that the pi is supposed to be up in one go
PAUSE = 2                                                   # pause between individual measurements
ITERATIONS_PER_DAY = int(24 * 60 / MEASURE_INTERVAL)        # iterations per day
BLINKS_OF_LED = 30 * MEASURE_INTERVAL                       # number of LED blinks to fill the interval
SECONDS = BLINKS_OF_LED * 2                                 # seconds that the interval is equal to

try:
    # init
    input_output = InputOutput()
    lcd = LCDisplay()
    lcd.clear
    lcd.backlight_on
    led_indicator = LEDIndicator(input_output.led_pins)
    lcd.print_strings("Booting Up", "One Moment")
    led_indicator.blink(4)
    dht_sensor = Dht22(input_output.dht_pins)
    light_sensor = Light(input_output.light_pins)
    out_temp_sensor = OutdoorTemp(input_output.out_temp_addr)
    input_output.title_read()
    input_output.track_init()
    input_output.log_init(dht_sensor.names, out_temp_sensor.names, light_sensor.names)
    led_indicator.blink(PAUSE)
    uploader = OnlinePush()

    for n in range(UPTIME):
        # read the track file to get the number
        input_output.track_read()
        lcd.print_strings("Name: {}".format(input_output.title), "Iteration: {}".format(input_output.iteration))
        led_indicator.blink(4)

        for i in range(ITERATIONS_PER_DAY):
            # measure
            led_indicator.on            
            dht_sensor.measure()            
            led_indicator.blink(PAUSE)
            led_indicator.on
            out_temp_sensor.measure()
            led_indicator.blink(PAUSE)
            led_indicator.on
            light_sensor.measure()
            lcd.print_strings("Done", "Measuring")            
            led_indicator.blink(PAUSE)
            # wait for next measurement
            t_in = "T-IN:  {:2.1f} {:2.1f}".format(dht_sensor.values[0][0], dht_sensor.values[0][1])
            t_out = "T-OUT: {:2.1f}".format(out_temp_sensor.values[0])
            lcd.print_strings(t_in, t_out)
            if i % WRITE_INTERVAL == 0:
                input_output.log_write(dht_sensor.values, out_temp_sensor.values, light_sensor.values) 
                uploader.push(dht_sensor.values, out_temp_sensor.values, light_sensor.values)
            led_indicator.blink(BLINKS_OF_LED)

except KeyboardInterrupt:
    print("\nUser terminated program. Shutting down.")
    led_indicator.blink()

except IOError as error:
    print("--------------------SOMETHING WENT WRONG--------------------")
    print(error.args)
    led_indicator.blink()

finally:
    lcd.backlight_off
    lcd.clear
    GPIO.cleanup()
    call("sudo reboot", shell=True)