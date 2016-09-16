#https://learn.adafruit.com/character-lcd-with-raspberry-pi-or-beaglebone-black/wiring
#LCD git library: https://github.com/adafruit/Adafruit_Python_CharLCD
#RFID reader git library: https://github.com/adafruit/Adafruit_Python_PN532 
#kartya uid: f14a92ed

import binascii
import sys
import time

import Adafruit_CharLCD as LCD
import Adafruit_PN532 as PN532

#nfc chip comm pins(SPI)
nfc_CS   = 18 #SCL
nfc_MOSI = 23 #MOSI
nfc_MISO = 24 #MISO
nfc_SCLK = 25 #SCK

#create an instance of the pn532 class
pn532 = PN532.PN532(cs=nfc_CS, sclk=nfc_SCLK, mosi=nfc_MOSI, miso=nfc_MISO)

pn532.begin()

#get the firmware version of the chip and print it out
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards. 
pn532.SAM_configuration()

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
	uid = pn532.read_passive_target() #read card (wheather it is there or not)

	if uid is None:
		if wasRead:
			lcdMsg('Erintsen kartyat\n a leolvasohoz!', 'white')
			wasRead = False
		if(time.time()-lastRead) > 60: 
			lcdMsg('Erintsen kartyat\n a leolvasohoz!', 'none')
		continue

	print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))

	if binascii.hexlify(uid) == '01020304' and not wasRead:
		lcdMsg('Access granted!', 'green')
	else:
		lcdMsg('Hozzaferes megtagadva!', 'red')
		time.sleep(0.5)
		lcdMsg('Hozzaferes megtagadva!', 'red')

	#commWithServer(binascii.hexlify(uid))

	wasRead = True
	#lcdMsg('Kartya leolvasva', 'green')
	time.sleep(2)

	lastRead = time.time()

	time.sleep(0.5)
