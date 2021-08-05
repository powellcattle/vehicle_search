#!/bin/sh -e
cd /home/spowell/dev/reports
rm -f *.html
cd /home/spowell/dev/vehicle_search
/home/spowell/dev/vehicle_search/venv/bin/python3.8 main.py
