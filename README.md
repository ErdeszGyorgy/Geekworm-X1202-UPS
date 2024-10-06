# Geekworm-X1202-UPS
Geekworm X1202 UPS HAT files for Raspberry Pi 5 Bookworm

These are the files which can be used for the UPS HAT to safe shutdown of Pi in case of power loss, and to manually turn on and off the charging of the batteries.

If you want to use the X2012 as a backup power source, please consult the official github page of it.

**1. Create the UPS files directory:**
sudo mkdir /home/pi/x1202
The other three are existing like etc-systemd-system => /etc/systemd/system and so on.

**2. Copy the files in their directories.**

**3. Make the .sh files executable:**
sudo chmod +x /home/pi/x1201/power-monitor.sh
sudo chmod +x /usr/local/bin/*.sh

**4. Install the services:**
sudo systemctl daemon-reload
sudo systemctl enable battery
sudo systemctl start battery
sudo systemctl daemon-reload
sudo systemctl enable power-monitor
sudo systemctl start power-monitor

## Battery service:

It exports the GPIO16 pin (translates it to actual number gpio587) and sets it to high (1), which means charging disabled. So after boot or reboot, the batteries are not charged.

In the file /home/pi/usefulcodes.txt, there are the codes which can be run afterwards, which let the corresponding bash file of the two run:
sudo bash /usr/local/bin/enable-charging.sh
sudo bash /usr/local/bin/disable-charging.sh

The enabled state is highly likely an automated charging management, but I like to charge mines manually, since I use them only for shutdown which happens not too often.

The state of the batteries can be check with this code, also in the usefulcodes.txt:
sudo python3 /home/pi/x1202/battery.py

## Power monitor service:

It checks the power loss in an endless loop on the GPIO6 pin and run the poweroff on the Pi in case of power loss. 3 seconds after shutdown of the Pi, the UPS will be turned off or rather it goes in a battery power saving state.
