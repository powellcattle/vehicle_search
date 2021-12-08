#!/bin/sh -e
cd /home/scot/dev/reports
rm -f *html *log*
cd /home/scot/dev/vehicle_search
/usr/bin/nordvpn disconnect
/home/scot/dev/vehicle_search/venv/bin/python3.8 main.py
/usr/bin/nordvpn connect
