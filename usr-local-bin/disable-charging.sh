#!/bin/bash

GPIO=16

# Find the actual GPIO pin number
GPIO=$(cat /sys/kernel/debug/gpio | grep "GPIO$GPIO" | awk -F'gpio-' '{print $2}' | awk -F' ' '{print $1}')

# Check if GPIO is already exported
if [ ! -d /sys/class/gpio/gpio$GPIO ]; then
    echo "$GPIO" > /sys/class/gpio/export
fi

# Set direction to output
echo "out" > /sys/class/gpio/gpio$GPIO/direction

# Disable charging
echo "1" > /sys/class/gpio/gpio$GPIO/value
