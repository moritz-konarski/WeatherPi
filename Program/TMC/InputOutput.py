#!/usr/bin/python
import os
from pathlib import Path
import datetime as dt

info_path = Path("/home/pi/Desktop/Program/Info")
track_path = Path("/home/pi/Desktop/Program/Info/Tracks")
user_path = Path("/home/pi/Desktop/User")

pin_file = info_path / "pin_numbers.txt"
title_file = user_path / "title.txt"

led_signifier = "LED: "
dht_signifier = "DHT22: "
title_signifier = "Title: "
light_signifier = "Light: "
track_signifier = "Iteration: "
temp_out_signifier = "DS18: "

class InputOutput:

    def __init__(self):
        self.pin_file = pin_file
        self.title_file = title_file
        self.iteration = 0
        self.title = ""

    @property
    def dht_pins(self):
        try:
            with self.pin_file.open() as file:
                self.pin_txt_num_lines = sum(1 for line in self.pin_file.open())
            with self.pin_file.open() as file:
                for n in range(self.pin_txt_num_lines):
                    read = file.readline()
                    if read.startswith(dht_signifier):
                        read = read.replace(dht_signifier, "")
                        read = read.split(" ")
                        dht_pins = [int(number) for number in read]
                        return dht_pins
        except IOError:
            raise IOError("pin_numbers.txt not found! Folder: /home/pi/Desktop/Program/Info")

    @property
    def light_pins(self):
        try:
            with self.pin_file.open() as file:
                self.pin_txt_num_lines = sum(1 for line in self.pin_file.open())
            with self.pin_file.open() as file:
                for n in range(self.pin_txt_num_lines):
                    read = file.readline()
                    if read.startswith(light_signifier):
                        read = read.replace(light_signifier, "")
                        read = read.split(" ")
                        light_pins = [int(number) for number in read]
                        return light_pins
        except IOError:
            raise IOError("pin_numbers.txt not found! Folder: /home/pi/Desktop/Program/Info")

    @property
    def led_pins(self):
        try:
            with self.pin_file.open() as file:
                self.pin_txt_num_lines = sum(1 for line in self.pin_file.open())
            with self.pin_file.open() as file:
                for n in range(self.pin_txt_num_lines):
                    read = file.readline()
                    if read.startswith(led_signifier):
                        read = read.replace(led_signifier, "")
                        led_pin = int(read)
                        return led_pin
        except IOError:
            raise IOError("pin_numbers.txt not found! Folder: /home/pi/Desktop/Program/Info")
    
    @property
    def out_temp_addr(self):
        try:
            with self.pin_file.open() as file:
                self.pin_txt_num_lines = sum(1 for line in self.pin_file.open())
            with self.pin_file.open() as file:
                for n in range(self.pin_txt_num_lines):
                    read = file.readline()
                    if read.startswith(temp_out_signifier):
                        read = read.replace(temp_out_signifier, "")
                        addresses = read.split(" ")
                        return addresses
        except IOError:
            raise IOError("pin_numbers.txt not found! Folder: /home/pi/Desktop/Program/Info")
    
    def title_read(self):
        try:   
            with self.title_file.open() as file:
                self.title_file_num_lines = sum(1 for line in self.title_file.open())
            with self.title_file.open() as file:
                for n in range(self.title_file_num_lines):
                    read = file.readline()
                    if read.startswith(title_signifier):
                        read = read.replace(title_signifier, "")
                        self.title = read
                        log_dir_name = "{} Logs".format(self.title)
                        self.log_dir = user_path / log_dir_name
                        log_file_name = "{}_{:03}_log.txt".format(self.title, self.iteration)
                        self.log_file = self.log_dir / log_file_name
                        if self.log_dir.exists() is False:
                            self.log_dir.mkdir()                
                        break
        except IOError:
            raise IOError("name.txt not found! Folder: /home/pi/Desktop/User")
    
    def track_init(self):
        track_file_name = "{}_track.txt".format(self.title)
        self.track_file = track_path / track_file_name
        if not self.track_file.exists():
            track_file_content = "{}{}".format(track_signifier, "0")
            with self.track_file.open("w") as file:
                file.write(track_file_content.decode('utf-8'))

    def track_read(self):
        with self.track_file.open("r") as file:
            while (True):
                read = file.readline()
                if read.startswith(track_signifier):
                    read = read.replace(track_signifier, "")
                    iteration = int(read)
                    self.iteration = iteration + 1
                    break
                elif read is "":
                    # print ("There is no track number here.")
                    break
        log_file_name = "{}_{:03}_log.txt".format(self.title, self.iteration)
        self.log_file = self.log_dir / log_file_name
        track_file_content = "{}{}".format(track_signifier, self.iteration)
        with self.track_file.open("w") as file:
            file.write(track_file_content.decode('utf-8'))

    def log_init(self, dht_names=[[]], temp_out_names=[], light_names=[]):
        string = []
        string.append("{}".format("Time"))
        for name in dht_names:
            string.append("{}".format(name[0]))
        for name in dht_names:
            string.append("{}".format(name[1]))
        for name in temp_out_names:
            string.append("{}".format(name))
        for name in light_names:
            string.append("{}".format(name))   
        self.title_string = ', '.join(string) + "\n"
        if not self.log_file.exists():
            # print(self.title_string)
            with self.log_file.open("a") as file:
                file.write(self.title_string.decode('utf-8'))
        else:
            pass
            # print("Continuation...\n{}".format(self.title_string))

    def log_write(self, dht_values=[[]], temp_out_values=[], light_values=[]):
        string = []
        dateTime = dt.datetime.now().strftime("%x") + " " + dt.datetime.now().strftime("%X")
        string.append(dateTime)
        for value in dht_values:
            string.append("{}".format(value[0]))
        for value in dht_values:
            string.append("{}".format(value[1] / 100))
        for value in temp_out_values:
            string.append("{}".format(value))
        for value in light_values:
            string.append("{}".format(value))   
        self.log_string = ', '.join(string) + "\n"
        # print(self.log_string)
        with self.log_file.open("a") as file:
            file.write(self.log_string.decode('utf-8'))