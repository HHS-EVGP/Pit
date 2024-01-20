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
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import RFM9x
import adafruit_rfm9x
# import sqlite3

# Connect to SQLite database (or create a new one if it doesn't exist)
# imu = sqlite3.connect('/home/pit/2024/imu.db')
# cursor_imu = imu.cursor()

lable_id = 0

# Create a table if it doesn't exist
# cursor_imu.execute('''
#     CREATE TABLE IF NOT EXISTS imu (
#         id REAL,
#         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         acceleration_x REAL,
#         acceleration_y REAL,
#         acceleration_z REAL,
#         gyro_x REAL,
#         gyro_y REAL,
#         gyro_z REAL
#     )
# ''')
# imu.commit()

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

packet = None

try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0)
    rfm9x.tx_power = 23

    while True:

        # check for packet rx
        packet = rfm9x.receive()
        if packet is not None:
            lable_id += 1
            # Display the packet text and rssi
            try:
                packet_text = str(packet, "utf-8")

                print(packet_text)

                if packet_text.startswith("$imu"):
                    packet_text = packet_text[4:]

                    packet_text = packet_text.split(',')
                    imu1, imu2, imu3, imu4, imu5, imu6 = map(float, packet_text)
                    
                    # cursor_imu.execute('''
                    #     INSERT INTO imu (id, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z)
                    #     VALUES (?, ?, ?, ?, ?, ?, ?)
                    # ''', (lable_id, imu1, imu2, imu3, imu4, imu5, imu6))

                    # imu.commit()
                    print(packet_text)

            except:
                pass

            
except RuntimeError as error:
    # imu.close()
    print("\nDatabase connection closed.")
    print('RFM9x Error: ', error)

except KeyboardInterrupt:
    # imu.close()
    print("\nDatabase connection closed.")

