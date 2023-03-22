# BabyActivityTracker
 Tracks activities of a baby from Raspberry Pi Pico W to Google Sheets using micropython.
 DIY version of Talli Baby Tracker


## Requirements
1. Raspberry Pi Pico W
2. Google App Credentials
3. Some buttons/input devices
4. Internet connection


## Basic Setup
1. On local machine install Thonny `pip install thonny`
2. On Raspberry Pi Pico W install micropython
3. Start thonny from terminal
4. Copy code from this repository into directory.
5. Run `google/generateRefreshToken.py` on the pico and copy the returned temporary token into secrets.py


## Customization
1. Setup to write to the worksheet set in secrets.py
2. Change individual sheet names in main.py lines 61-70
3. Change pins used on Pico in main.py line 56
4. Supports as many pins as you'd like, only 8 are used by default: pins 14-23
5. To save processing potentially large columns, store `=COUNTA(A:A)` in a specific cell of your sheet, and point to it in main.py line 34
