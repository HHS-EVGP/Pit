# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import time
import datetime
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import RFM9x
import adafruit_rfm9x
import csv



lable_id = 0



# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

packet = None

with open('imu_data.csv', mode='w', newline='') as csv_file:
    # fieldnames = [
    #     'label_id',
    #     'timestamp',
    #     'acceleration_x',
    #     'acceleration_y',
    #     'acceleration_z',
    #     'gyro_x',
    #     'gyro_y',
    #     'gyro_z'
    #     ]  # Add more fields as needed
    fieldnames = [
        'label_id',
        'timestamp',
        'imu_data'
        ]  # Add more fields as needed
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0)
        rfm9x.tx_power = 23

        while True:

            # check for packet rx
            packet = rfm9x.receive()
            if packet:
                lable_id += 1
                # Display the packet text and rssi
                try:
                    packet_text = str(packet, "utf-8")

                    if packet_text.startswith("$imu"):

                        writer.writerow({'label_id': lable_id, 'timestamp': datetime.datetime.now(), 'imu_data': packet})

                        print("Wrote to imu.db")

                except:
                    pass

                
    except RuntimeError as error:
        print('\nRFM9x Error: ', error)

    except KeyboardInterrupt:
        print("\nConnection Closed.")

