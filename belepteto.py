#https://learn.adafruit.com/character-lcd-with-raspberry-pi-or-beaglebone-black/wiring
#LCD git library: https://github.com/adafruit/Adafruit_Python_CharLCD

import binascii
import sys
import time
import serial
import Adafruit_CharLCD as LCD

port =serial.Serial(
    "/dev/ttyUSB0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout = 0,
    timeout = 1)

print(port.isOpen())
print("Com Port opened...")

# CharLCD pin configuration:
lcd_rs    = 27  
lcd_en    = 22
lcd_d4    = 5
lcd_d5    = 6
lcd_d6    = 13
lcd_d7    = 19
lcd_red   = 16
lcd_green = 21
lcd_blue  = 20

#CharLCD rows abd coloumns config
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                              lcd_columns, lcd_rows, lcd_red, lcd_green, lcd_blue)

def lcdMsg(message, color):
    lcd.clear()
    if color == 'blue':
	lcd.set_color(0.0, 0.0, 1.0) #blue background color
    elif color == 'green':
	lcd.set_color(0.0, 1.0, 0.0) #green background color
    elif color == 'white':
	lcd.set_color(1.0, 1.0, 1.0) #white bg color
    elif color == 'none':
	lcd.set_color(0.0, 0.0, 0.0) #no bg color
    elif color == 'red':
	lcd.set_color(1.0, 0.0, 0.0) #red bg color

    lcd.message(message)

    if '\n' not in message:
	case = len(message) > lcd_columns
    else:
	case =  len(message.split('\n')[0]) > lcd_columns or len(message.split('\n')[1]) > lcd_columns
	
    if case:
	for i in range(len(message)-lcd_columns):
	    time.sleep(0.3)
	    lcd.move_left()

#def commWithServer(cardID):
    #nincs meg meg

lastRead = time.time()

lcdMsg('Erintsen kartyat\n a leolvasohoz!', 'white')

wasRead = False

while True:
    uid=port.read(16)


    if uid == '':
	if wasRead:
	    lcdMsg('Erintsen kartyat\n a leolvasohoz!', 'white')
	    wasRead = False
	if(time.time()-lastRead) > 60: 
	    lcdMsg('Erintsen kartyat\n a leolvasohoz!', 'none')
	continue
    else:
        print 'Found card with UID: ' + str(uid)
	lcdMsg('Kartya leolvasva\n' + str(uid), 'green')
	wasRead = True

	#kommunikacio a szerverrel

	lastRead = time.time()
