#! /usr/bin/python3

import serial
import time

wattage = 0
inc = 25

load_enabled = 0

def error_msg():
	print('Unrecognized command')
	#print('Valid options are:')
	#print('on - activate load')
	#print('off - deactivate load')
	#print('exit - quit application')
	
def aps_print(text):
	print(text)
	ser.write(bytes(text,"utf-8"))
	time.sleep(.03)
	
def setWatt(value):
	global wattage
	global load_enabled
	
	if load_enabled == 0:
		print("Load not enabled, command ignored")
		return
	
	wattage	= float(value)
	print("Setting wattage to " + str(wattage) + " W")
	print("Please wait for command to finish")
	#print(wattage)
	aps_print('MEAS:VOLT?;')
	voltage = ser.read(8)
	#print(float(voltage))
	current = float(value) / float(voltage)
	aps_print('CC:A ' + str(current) + ';')
	time.sleep(1)
	aps_print('MEAS:POW?;')
	power = ser.read(8)
	#print(float(power))
	scale = float(value) / float(power)
	current = current * scale
	aps_print('CC:A ' + str(current) + ';')
	
def help():
	print("Commands:")
	print("on\tTurn load on")
	print("off\tTurn load off")
	print("watt=XX\tSet load to XX W")
	print("\tor simply enter a number")
	print("inc=XX\tSet increment to XX W")
	print("<enter>\tIncrement wattage by [inc] W")
	print("\t[inc] is 25 by default")
	print("help\tDisplay help")
	print("exit\tTurn load off and exit application")

ser = serial.Serial('/dev/com1', 9600)


print()
print("APS 3B12 Control Script")
print("Connected to: " + ser.name)
print()
help()
print()

aps_print('REM;')
aps_print('CC:A 0;')
aps_print('LOAD 0;')
aps_print('LOC;')

while(1):

	# For each command:
	#	1. Set 3B12 to Remote
	#	2. Perform operation
	#	3. Set 3B12 to Local

	textIn = input("> ").split('=')
	command = textIn[0].strip(' ')

	aps_print('REM;')
	
	if len(textIn[0]) == 0:
		setWatt(wattage + inc)
	elif len(textIn) == 1:
		# No-parameter commands
		if(command == 'on'):
			print("Load turning on...")
			load_enabled = 1
			aps_print('LOAD 1;')
		elif(command == 'off'):
			print("Load turning off...")
			load_enabled = 0
			wattage = 0
			aps_print('CC:A 0;')
			aps_print('LOAD 0;')
		elif(command == 'readV'):
			aps_print('MEAS:VOLT?;')
			voltage = ser.read(8)
			print(voltage),
		elif(command == 'help'):
			help()
		elif(command == 'exit'):
			print("Exiting...")
			aps_print('CC:A 0;')
			aps_print('LOAD 0;')
			aps_print('LOC;')
			exit()
		elif(command.isdigit()):
			setWatt(command)
		else:
			error_msg()
	elif len(textIn) == 2:
		# One-parameter commands
		value = textIn[1].strip(' ')
		if(command == 'amp'):
			#if(int(value) < 4):
			aps_print('CC:A ' + str(value) + ';')
			#else:
				#print('Maximum current is currently set to 4A')
				#aps_print('CC:A 4;');
		if(command == 'watt'):
			setWatt(value)
		if(command == 'inc'):
			print("Increment value set to " + str(float(value)) + " W")
			inc = float(value)
	else:
		# Multi-parameter commands
		pass

	aps_print('LOC;')



