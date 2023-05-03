###!/usr/bin/env python 

import sys
import time

REGSEL = None
ENAB = None
BACKLIGHT = None
D4 = None
D5 = None
D6 = None
D7 = None
Data = [D4, D5, D6, D7]

LCD_CHR = True	   # Sending a Character to the LCD
LCD_CMD = False    # Sending a command to the LCD

LCD_WIDTH = None
LCD_HEIGHT = None

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st Line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line
LCD_LINE = [LCD_LINE_1, LCD_LINE_2, LCD_LINE_3, LCD_LINE_4]

E_PULSE = 0.0005
E_DELAY = 0.0005



#-----------------------------------------------
#
#  Function:  start
#
#  This function defines the size of the LCD 
#    being used and defaults to 16x2 if invalid 
#    sizes are passed in. 
#
#-----------------------------------------------   

def start(GPIO,rows, cols):
   global LCD_WIDTH
   global LCD_HEIGHT
   if(0 < cols < 21):
      LCD_WIDTH=cols
   else:
      LCD_WIDTH=16
   if(0 < rows < 5):
      LCD_HEIGHT=rows
   else:
      LCD_HEIGHT=2

#-----------------------------------------------
#
#  Function:  LCD
#
#  This function defines the pins used for the 
#    LCD, sets up those pins on the GPIO and 
#    updates the global variables to the current
#    pin values specified. 
#
#-----------------------------------------------   
      
def LCD(GPIO,RS,E,Da4,Da5,Da6,Da7,BKL):
   global REGSEL 
   REGSEL = RS
   global ENAB 
   ENAB= E
   global D4 
   D4= Da4
   global D5
   D5 = Da5
   global D6
   D6 = Da6
   global D7
   D7 = Da7
   global BACKLIGHT
   global Data
   BACKLIGHT = BKL
   Data = [D4,D5,D6,D7]
   GPIO.setwarnings(False)
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(REGSEL,GPIO.OUT)
   GPIO.setup(ENAB,GPIO.OUT)
   GPIO.setup(BACKLIGHT,GPIO.OUT)
   GPIO.setup(Data,GPIO.OUT)

   
   
#-----------------------------------------------
#
#  Function:  backlight
#
#  Enables the backlight if True or disables it  
#    if False is passed in. 
#
#-----------------------------------------------   

def backlight(GPIO,state):
   try:
      GPIO.output(BACKLIGHT,state)
   except InvalidValue:
      print("State = ",state,"which is invalid")
      GPIO.output(BACKLIGHT,False)
      
      
      
#-----------------------------------------------
#
#  Function:  lcd_string
#
#  Displays the string stored in "message" on  
#    the indicated line of the LCD. 
#
#-----------------------------------------------   

def lcd_string(GPIO,message,line):
   message = message.ljust(LCD_WIDTH," ")
   lcd_byte(GPIO,LCD_LINE[line-1], LCD_CMD)
   for i in range(len(message)):
      lcd_byte(GPIO,ord(message[i]),LCD_CHR)



#-----------------------------------------------
#
#  Function:  lcd_shifleft
#
#  Shifts the current contents of the display  
#    left by one character. 
#
#-----------------------------------------------   

def lcd_shiftleft(GPIO):
   lcd_byte(GPIO,0x18,LCD_CMD)
   time.sleep(E_DELAY)
   
   
   
#-----------------------------------------------
#
#  Function:  lcd_shiftright
#
#  Shifts the current contents of the display  
#    right by one character. 
#
#-----------------------------------------------      

def lcd_shiftright(GPIO):
   lcd_byte(GPIO,0x1C,LCD_CMD)
   time.sleep(E_DELAY)



#-----------------------------------------------
#
#  Function:  lcd_shutdown
#
#  Clears the display, turns off the backlight  
#    and disables the display when no longer 
#    needed.
#
#-----------------------------------------------   

def lcd_shutdown(GPIO):
   lcd_byte(GPIO,0x01,LCD_CMD)
   time.sleep(E_DELAY)
   lcd_byte(GPIO,0x08,LCD_CMD)
   time.sleep(E_DELAY)
   GPIO.output(BACKLIGHT,False)


   
#-----------------------------------------------
#
#  Function:  lcd_toggle_enable
#
#  Toggles the enable line so that the data can  
#    be written to the LCD register.
#
#-----------------------------------------------      
      
def lcd_toggle_enable(GPIO):
   time.sleep(E_DELAY)
   GPIO.output(ENAB, True)
   time.sleep(E_PULSE)
   GPIO.output(ENAB,False)
   time.sleep(E_DELAY)


   
#-----------------------------------------------
#
#  Function:  lcd_byte
#
#  Writes a single byte of data to the LCD  
#    register for display
#
#-----------------------------------------------     
  
def lcd_byte(GPIO,bits,mode):

   GPIO.output(REGSEL, mode)  # True for Character and False for Command
   
   # Clear the data lines
      
   GPIO.output(D4,False)
   GPIO.output(D5,False)
   GPIO.output(D6,False)
   GPIO.output(D7,False)
   
   # Load the Upper 4 bits onto the data lines
   
   if(bits&0x10==0x10):
      GPIO.output(D4,True)
   if(bits&0x20==0x20):
      GPIO.output(D5,True)
   if(bits&0x40==0x40):
      GPIO.output(D6,True)
   if(bits&0x80==0x80):
      GPIO.output(D7,True)

   #  Write the upper 4 bits to the LCD
      
   lcd_toggle_enable(GPIO)
   
   # Clear the data lines again
   
   GPIO.output(D4,False)
   GPIO.output(D5,False)
   GPIO.output(D6,False)
   GPIO.output(D7,False)
   
   #  Load the Lower 4 bits onto the data lines
   
   if(bits&0x01==0x01):
      GPIO.output(D4,True)
   if(bits&0x02==0x02):
      GPIO.output(D5,True)
   if(bits&0x04==0x04):
      GPIO.output(D6,True)
   if(bits&0x08==0x08):
      GPIO.output(D7,True)
      
   #  Write the lower 4 bits to the LCD
      
   lcd_toggle_enable(GPIO)
   
   
   
#-----------------------------------------------
#
#  Function:  lcd_init
#
#  Initializes the LCD display by setting the 
#    direction the text is written, turning off
#    the flashing cursor and clearing the 
#    display.
#
#-----------------------------------------------   
   
   
def lcd_init(GPIO):
   lcd_byte(GPIO,0x33,LCD_CMD)	# 110011 Initialize
   time.sleep(E_DELAY)
   lcd_byte(GPIO,0x32,LCD_CMD)	# 110010 Initialize
   time.sleep(E_DELAY)
   lcd_byte(GPIO,0x06,LCD_CMD)	# 000110 Cursor Move Direction
   time.sleep(E_DELAY)
   lcd_byte(GPIO,0x0C,LCD_CMD)	# 001100 Display On, Cursor Off, Blink off
   time.sleep(E_DELAY)
   lcd_byte(GPIO,0x28,LCD_CMD)	# 101000 Data length, number of lines, font size
   time.sleep(E_DELAY)
   lcd_byte(GPIO,0x01,LCD_CMD)	# 000001 Clear Display
   time.sleep(E_DELAY)
   GPIO.output(BACKLIGHT,True)

#-----------------------------------------------
#
#  Function:  Custom
#	Displays arrows
#  
#
#-----------------------------------------------   

LCD_CHARS=[0x40,0x48,0x50,0x58,0x60,0x68,0x70,0x78]

def lcd_custom(GPIO,charPos,charDef):
	lcd_byte(GPIO,LCD_CHARS[charPos],LCD_CMD)
	for line in charDef:
		lcd_byte(GPIO,line,LCD_CHR)

if __name__ == '__main__':
   try:
      import RPi.GPIO as GPIO
      start(GPIO,16,2)
      LCD(GPIO,21,20,16,12,25,18,4)
      GPIO.setwarnings(False)
      GPIO.setmode(GPIO.BCM)
      lcd_init(GPIO)
      time.sleep(2)
      lcd_shutdown(GPIO)
      GPIO.cleanup()
   except:
      pass      