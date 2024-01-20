# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
# Wiring Check, Pi Radio w/RFM9x
# Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
# Author: Brent Rubell for Adafruit Industries
# Editted: Joshua Nafziger 12/27/2023

import adafruit_rfm9x
import board
import busio
import csv
import os
import time
from datetime import datetime
from digitalio import DigitalInOut, Direction, Pull

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0)
rfm9x.tx_power = 23

index = 1
conter = 0
while os.path.exists(f"{index}.data.csv"):
    index += 1
new_file_name = f"{index}.data.csv"

with open(new_file_name, 'w', newline='') as csv_file: 
    fieldnames = [
        'time','counter',
        'IMU_Accel_x', 'IMU_Accel_y', 'IMU_Accel_z',
        'IMU_Gyro_x', 'IMU_Gyro_y', 'IMU_Gyro_z',
        'Battery_1','Battery_2','Brake_Pedal',
        'ca_AmpHrs','ca_Voltage','ca_Current','ca_Speed','ca_Miles',
        'motor_temp','control_info'
        ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'time':datetime.now(),'counter':conter,})
    while True:
        conter += 1
        packet = None

        # check for packet rx
        packet = rfm9x.receive()

        if packet is None:
            print('- Waiting for PKT -')
        else:

            current_packet = str(packet, "utf-8")
            
            if current_packet.startswith("imu,"):
                ax = None
                ay = None
                az = None
                gx = None
                gy = None
                gz = None

                # ADD CODE TO PULL APART DATA

                values = current_packet.split(',')
                ax, ay, az, gx, gy, gz = map(float, values[1:])
                
                writer.writerow({
                    'time':datetime.now(),'counter':conter,
                    'IMU_Accel_x': ax,'IMU_Accel_y': ay,'IMU_Accel_z': az,
                    'IMU_Gyro_x': gx,'IMU_Gyro_y': gy,'IMU_Gyro_z': gz
                    })
                
            if current_packet.startswith("temps,"):
                batt1 = None
                batt2 = None

                # ADD CODE TO PULL APART DATA
                
                values = current_packet.split(',')
                batt1, batt2 = map(float, values[1:])

                if batt1 == -6:
                    batt1 = None
                if batt2 == -6:
                    batt2 = None

                writer.writerow({
                    'time':datetime.now(),'counter':conter,
                    'Battery_1':batt1,'Battery_2':batt2
                    })
            
            if current_packet.startswith("bp,"):
                BP = None

                # ADD CODE TO PULL APART DATA
                
                values = current_packet.split(',')
                BP = values[1:][0]

                writer.writerow({
                    'time':datetime.now(),'counter':conter,
                    'Brake_Pedal':BP
                    })
            
            if current_packet.startswith("ca,"):
                AH = None
                V = None
                C = None
                S = None
                M = None

                # ADD CODE TO PULL APART DATA

                values = current_packet.split(',')

                try:
                    AH, V, C, S, M, Other = values[1:]
                    
                    writer.writerow({
                        'time':datetime.now(),'counter':conter,
                        'ca_AmpHrs':AH,'ca_Voltage':V,'ca_Current':C,'ca_Speed':S,'ca_Miles':M
                        })
                except:
                    pass

            if current_packet.startswith("motor,"):
                temp = None

                # ADD CODE TO PULL APART DATA
                
                writer.writerow({
                    'time':datetime.now(),'counter':conter,
                    'motor_temp':temp
                    })

            if current_packet.startswith("control,"):
                info = None

                # ADD CODE TO PULL APART DATA
                
                writer.writerow({
                    'time':datetime.now(),'counter':conter,
                    'control_info':info,
                    })