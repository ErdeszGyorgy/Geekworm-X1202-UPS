# Geekworm-X1202-UPS
Geekworm X1202 UPS HAT files for Raspberry Pi 5 Bookworm

These are the files which can be used for the UPS HAT to safe shutdown of Pi in case of power loss, and to manually turn on and off the charging of the batteries.

If you want to use the X1202 as a backup power source, please consult the official pages of it:

https://suptronics.com/Raspberrypi/Power_mgmt/x120x-v1.0_software.html

https://github.com/suptronics/x120x.git

*1. Create the UPS files directory:*

sudo mkdir /home/pi/x1202

The other three are existing like etc-systemd-system => /etc/systemd/system and so on.

*2. Copy the files in their directories.*

*3. Make the .sh files executable:*

sudo chmod +x /home/pi/x1202/power-monitor.sh

sudo chmod +x /usr/local/bin/*.sh

*4. Install the services:*

sudo systemctl daemon-reload

sudo systemctl enable battery

sudo systemctl start battery

--------------------------------

sudo systemctl daemon-reload

sudo systemctl enable power-monitor

sudo systemctl start power-monitor

## Battery service:

It exports the GPIO16 pin (translates it to actual number gpio587) and sets it to high (1), which means charging disabled. So after boot or reboot, the batteries are not charged.

## Check the GPIO16

So it is more complicated since the actual number depends on the hardware.
You have to enable debugfs.

1. Check if debugfs is already mounted

mount | grep debugfs

If you get something like:

debugfs on /sys/kernel/debug type debugfs (...)

then it’s already mounted.

4. Mount it manually (temporary)
If not mounted, run:

sudo mount -t debugfs none /sys/kernel/debug

6. View GPIO info
Now you can read the GPIO debug file:

sudo cat /sys/kernel/debug/gpio

You have to search for something liek this for GPIO16:

gpio-585 (GPIO16              |sysfs               ) out hi

This shows the actual kernel-level global GPIO number, whether it is gpio587, or gpio585 (in latter case with the new hardware, that is, another pi 5 board).

8. (Optional) Make the mount permanent
To have it auto-mounted at boot:

echo "debugfs  /sys/kernel/debug  debugfs  defaults  0  0" | sudo tee -a /etc/fstab

Then reboot.

This GPIO16 number like gpio585 must be set in the battery.py file in this line:

Path to the GPIO value file

gpio_value_path = "/sys/class/gpio/gpio585/value"

## Set the charging manually

In the file /home/pi/usefulcodes.txt, there are the codes which can be run afterwards, which let the corresponding bash file of the two run:

sudo bash /usr/local/bin/enable-charging.sh

sudo bash /usr/local/bin/disable-charging.sh

The enabled state is highly likely an automated charging management, but I like to charge mines manually, since I use them only for shutdown which happens not too often.

The state of the batteries can be checked with this code, also in the usefulcodes.txt:

sudo python3 /home/pi/x1202/battery.py

## Power monitor service:

It checks the power loss in an endless loop on the GPIO6 pin and run the poweroff on the Pi in case of power loss. 3 seconds after shutdown of the Pi, the UPS will be turned off automatically or rather it goes into a battery power saving state.
