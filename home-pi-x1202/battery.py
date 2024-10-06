#!/usr/bin/env python
import struct
import smbus
import sys
import time
import gpiod
import subprocess

# Global settings
GPIO_PORT = 26
I2C_ADDR = 0x36

# Set up GPIO
chip = gpiod.Chip('/dev/gpiochip0')  # The chip name might need to be adjusted based on your hardware
line = chip.get_line(GPIO_PORT)
line.request(consumer='example', type=gpiod.LINE_REQ_DIR_OUT)

def readVoltage(bus):
    address = I2C_ADDR
    read = bus.read_word_data(address, 2)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * 1.25 / 1000 / 16
    return voltage

def readCapacity(bus):
    address = I2C_ADDR
    read = bus.read_word_data(address, 4)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped / 256
    if capacity > 100:
        capacity = 100
    return capacity

bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

voltage = readVoltage(bus)
capacity = readCapacity(bus)

# Path to the GPIO value file
gpio_value_path = "/sys/class/gpio/gpio587/value"

try:
    # Use subprocess to execute the cat command and capture the output
    result = subprocess.run(['cat', gpio_value_path], capture_output=True, text=True, check=True)
    
    # The value will be '0' or '1', so strip any extra whitespace
    gpio_value = result.stdout.strip()
        # Print the GPIO value
    print(" ")
    print("********************")
    print(f"GPIO 16 value is: {gpio_value}")

except subprocess.CalledProcessError as e:
    print(f"Error reading GPIO value: {e}")
except FileNotFoundError:
    print(f"GPIO path {gpio_value_path} not found.")

if gpio_value == "1":
        print("Charging disabled")
if gpio_value == "0":
        print("Charging enabled")

print("********************")
print("Voltage:%5.2fV" % voltage)

if 3.87 <= voltage <= 4.25:
    print ("Voltage Level Full")
elif 3.7 <= voltage < 3.87:
    print ("Voltage Level High")
elif 3.55 <= voltage < 3.7:
    print ("VoltageLevel medium")
elif 3.4 <= voltage < 3.55:
    print ("Voltage Level Low")
elif voltage < 3.4:
    print ("Voltage Level Critical")
else:
    print ("Voltage Level Unknown")
    
print("Battery:%5i%%" % capacity)

if capacity == 100:
    print("Battery FULL")
if capacity < 20:
    print("Battery Low")

print("********************")
print(" ")
