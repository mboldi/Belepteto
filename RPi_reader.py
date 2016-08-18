#https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/python-code
#LCD git library: https://github.com/adafruit/Adafruit_Python_CharLCD
#RFID reader git library: https://github.com/adafruit/Adafruit_Python_PN532 

import Adafruit_CharLCD as LCD
import binascii
import sys

import Adafruit_PN532 as PN532

#nfc chip comm pins(SPI)
nfc_CS   = 18
nfc_MOSI = 23
nfc_MISO = 24
nfc_SCLK = 25

#create an instance of the pn532 class
pn532 = PN532.PN532(cs=spi_CS, sclk=spi_SCLK, mosi=spi_MOSI, miso=spi_MISO)

pn532.begin()

#get the firmware version of the chip and print it out
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards. (nem tudom, hogy ez kell-e nekunk)
pn532.SAM_configuration()

# CharLCD pin configuration:
lcd_rs    = 27  
lcd_en    = 22
lcd_d4    = 25
lcd_d5    = 24
lcd_d6    = 23
lcd_d7    = 18
lcd_red   = 4
lcd_green = 17
lcd_blue  = 7

#CharLCD rows abd coloumns config
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_red, lcd_green, lcd_blue)


def lcdScrollMsg(message, color):
	if color == 'blue':
		lcd.set_color(0.0, 0.0, 1.0) #blue background color
	elif color == 'green':
		lcd.set_color(0.0, 1.0, 0.0) #green background color

	lcd.clear()
	for i in range(lcd_columns-len(message)):
		time.sleep(0.5)
		lcd.move_left()

def commWithServer(cardID):
	#nincs meg meg

def recieveDataFromServer():
	#nem tudom, hogy ez egyaltalan kell-e, vagy ahogy elkuldi az id-t azon a fuggvenyen belul a server valaszol is neki

lcdScrollMsg('Kérem érintse a kártyát a leolvasóhoz', 'blue')

while True:
	uid = pn532.read_passive_target() #read card (wheather it is there or not)

	if uid is None:
		continue

	print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))

	commWithServer(binascii.hexlify(uid))

	recieveDataFromServer()

	lcdScrollMsg('Kártya leolvasva', 'green')
