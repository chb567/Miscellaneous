#!/usr/bin/python
#
# HD44780 LCD Script for Cubieboard/SUNXI_GPIO compatible devices
# Adapted by chb567
# 04.12.2014
# Used http://www.linuxnico.fr/index.php?title=LCD_20x4 for reference
#
# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)
# 4 : RS
# 5 : R/W		     - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V
# 16: LCD Backlight GND
 
#import
import SUNXI_GPIO as GPIO
import time

"""
from SUNXI_GPIO_dummy.dummy import dummy
GPIO = dummy()
# Nur Funktionstest
GPIO.test() 
"""
 
# Define GPIO to LCD mapping
LCD_RS = 99
LCD_E  = 101
LCD_D4 = 103
LCD_D5 = 104
LCD_D6 = 106
LCD_D7 = 108
 
# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = 1
LCD_CMD = 0
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

# Timing constants
E_PULSE = 0.00003
E_DELAY = 0.00002

"""
#Alignment options 
options = {"left" : "ljust", \
	"right" : "rjust", \
	"centre" : "center",}
"""		


class HD44780:
	#functions
	def __INIT__(self):
		print "\n"
		print "INIT Called"
		print "GPIO setup"
		self.gpio_setup()
		# Initialise display
		print "LCD Init"
		self.lcd_init()
		print "Initialization complete!"
		print "\n"
		self.lcd_byte(0xFF,LCD_CHR)
		time.sleep(2)

	def gpio_setup(self):
		print "GPIO setup Called"
		GPIO.init()
		print "GPIO init() done"

		GPIO.setcfg(97, GPIO.OUT)
		#print "1"
		GPIO.setcfg(LCD_E, GPIO.OUT)  # E

		GPIO.setcfg(LCD_RS, GPIO.OUT) # RS
		GPIO.output(LCD_RS, 0) # RS

		GPIO.setcfg(LCD_D4, GPIO.OUT) # DB4
		GPIO.setcfg(LCD_D5, GPIO.OUT) # DB5
		GPIO.setcfg(LCD_D6, GPIO.OUT) # DB6
		GPIO.setcfg(LCD_D7, GPIO.OUT) # DB7
		#print "2"
		GPIO.output(97, 0)
		#print "3"
		self.lcd_nullify()
		#print "4"
	 	time.sleep(0.5)
		#print "5"
		GPIO.output(97, 1)

	def lcd_nullify(self):
		print "Nullify Called"
		GPIO.output(LCD_E, 0)  # E
		GPIO.output(LCD_RS, 0) # RS
		self.rst_data()

	def lcd_init(self):
		time.sleep(0.02)
		print "lcd init called"
		# Initialise display
		self.lcd_nullify()
		GPIO.output(LCD_D4, 1)
		GPIO.output(LCD_D5, 1)
		self.enable()
		time.sleep(0.005)
		self.enable()
		time.sleep(0.005)
		self.enable()
		time.sleep(0.0001)

		self.lcd_byte(0x02,LCD_CMD)
		self.lcd_byte(0x28,LCD_CMD)
		self.lcd_byte(0x08,LCD_CMD)
		self.lcd_byte(0x01,LCD_CMD)
		self.lcd_byte(0x01,LCD_CMD)
		self.lcd_byte(0x0C,LCD_CMD)
#		self.lcd_byte(0x40,LCD_CMD)

		"""
		self.lcd_byte(0x33,LCD_CMD)
		self.lcd_byte(0x32,LCD_CMD)
		self.lcd_byte(0x28,LCD_CMD)
		self.lcd_byte(0x0C,LCD_CMD)
		self.lcd_byte(0x06,LCD_CMD)
		self.lcd_byte(0x01,LCD_CMD)
		"""

#	def lcd_string(self, message, alignment="left"):
	def lcd_string(self, message, alignment="left"):
		print "LCD string called. Message: " + str(message)
		# Send string to display
#		textalign = options[alignment]()
#		message = str("message.")+str(textalign)+str("(LCD_WIDTH," ")")
#		message = message.alignment(LCD_WIDTH," ") 

		if alignment == "left":
			message = message.ljust(LCD_WIDTH," ") 
		elif alignment == "right":
			message = message.rjust(LCD_WIDTH," ") 
		elif alignment == "centre":
			message = message.center(LCD_WIDTH," ") 
		else:
			print "Text Aligner Screwed up!"

		print message

		for i in range(LCD_WIDTH):
			if message[i] == '\n':
#              			self.lcd_byte(0xC0, LCD_CMD) # next line try turning \n into a new lcd_string, then its automatically put into the next row
				print "Figure out how to do newline dammit!!!"
	          	else:
				self.lcd_byte(ord(message[i]),LCD_CHR)


	def enable(self):
		print "Enable Toggled"
		# Toggle 'Enable' pin
		time.sleep(E_DELAY)
		GPIO.output(LCD_E, 1)
		time.sleep(E_PULSE)
		GPIO.output(LCD_E, 0)
		time.sleep(E_DELAY)

	def rst_data(self):
		print "Data lines resetted"
		GPIO.output(LCD_D4, 0)
		GPIO.output(LCD_D5, 0)
		GPIO.output(LCD_D6, 0)
		GPIO.output(LCD_D7, 0)


	def lcd_byte(self, bits, mode):
		print "Send byte called! Byte: " + str(hex(bits))
		# Send byte to data pins
		# bits = data
		# mode = True  for character
		#        False for command

		GPIO.output(LCD_RS, mode) # RS

		# Send High bits
		self.rst_data()
		if bits&0x10==0x10:
			GPIO.output(LCD_D4, 1)
		if bits&0x20==0x20:
			GPIO.output(LCD_D5, 1)
		if bits&0x40==0x40:
			GPIO.output(LCD_D6, 1)
		if bits&0x80==0x80:
			GPIO.output(LCD_D7, 1)
		self.enable()   

		# Send Low bits
		self.rst_data()
		if bits&0x01==0x01:
			GPIO.output(LCD_D4, 1)
		if bits&0x02==0x02:
			GPIO.output(LCD_D5, 1)
		if bits&0x04==0x04:
			GPIO.output(LCD_D6, 1)
		if bits&0x08==0x08:
			GPIO.output(LCD_D7, 1)
		self.enable()
		time.sleep(0.001)

	def main(self):
		print "Main Called"
		# Main program block
		# Send some test
		
		self.lcd_byte(LCD_LINE_1, LCD_CMD)
		self.lcd_string("Not-Rasbperry Pi")
		self.lcd_byte(LCD_LINE_2, LCD_CMD)
		self.lcd_string("Model B")
		time.sleep(1)
		# Send some text
		self.lcd_byte(LCD_LINE_1, LCD_CMD)
		self.lcd_string("Raspberrypi-spy")
		time.sleep(0.5)
		self.lcd_byte(LCD_LINE_2, LCD_CMD)
		self.lcd_string(".co.uk")
		time.sleep(1)


if __name__ == '__main__':
	"""
	print "Does this even work?!"
	time.sleep(2)
	"""
	lcd = HD44780()
	lcd.__INIT__()

#	lcd.main()

	lcd.lcd_init()
	lcd.lcd_byte(LCD_LINE_3, LCD_CMD)
	lcd.lcd_string("HI")
	lcd.lcd_byte(LCD_LINE_3, LCD_CMD)
	lcd.lcd_string("Ho")
	lcd.lcd_init()

	lcd.lcd_byte(LCD_LINE_1, LCD_CMD)
	lcd.lcd_string("1")
	lcd.lcd_byte(LCD_LINE_2, LCD_CMD)
	lcd.lcd_string("2")
	lcd.lcd_byte(LCD_LINE_3, LCD_CMD)
	lcd.lcd_string("3")
	lcd.lcd_byte(LCD_LINE_4, LCD_CMD)
	lcd.lcd_string("4")
	lcd.lcd_init()
	lcd.lcd_byte(LCD_LINE_1, LCD_CMD)
	lcd.lcd_string("DONE\n")
	lcd.lcd_byte(LCD_LINE_2, LCD_CMD)
	lcd.lcd_string("secondline")
	
	x=int(0)
	increment = 0.05
	while True:
		lcd.lcd_byte(LCD_LINE_3, LCD_CMD)
		lcd.lcd_string(str(x))
		x=x+increment
		time.sleep(increment)
