import pyautogui as py
import time
import tkinter as tk
from tkinter import messagebox

# RDC screen size
# {1536, 864}

# Variables
active_faults = 0
pre_scan = False
completion_scan = False
scan_timer = 0
errorSet = 0
faultsPresent = 0
report_finished = 0
#add else return clear faults


# General Functions
def clicks_button(image, confidence):
	coord_x, coord_y = py.locateCenterOnScreen(image, confidence=confidence)
	py.click(coord_x, coord_y)
	return


def create_report():

	create = None

	while create is None:

		try:
			clicks_button('create_report.png', .9)
			print('Created report')
			time.sleep(2)
			break

		except TypeError:
			create = None
	return


def minimize_report():

	current = None

	while current is None:

		try:
			report_current = py.locateCenterOnScreen('report_current.png')
			gds_not_current = py.locateCenterOnScreen('gds_not_current.png')
			gds2_current = py.locateCenterOnScreen('gds_current.png')
			report_not_current = py.locateCenterOnScreen('report_not_current.png')
			if report_current and gds_not_current is not None:
				py.click(report_current)
				print('Report minimized')
				break

			elif gds2_current and report_not_current is not None:
				print('GDS2 Current')
				break

			elif gds2_current or gds_not_current is not None:
				py.click(gds2_current or gds_not_current)
			else:
				raise TypeError

		except TypeError:
			current = None
	return


def clear_faults():

	faults = None

	while faults is None:

		try:
			clicks_button('clear_dtcs.png', .9)
			print('Clicked Clear All DTC')

			addall = None

			while addall is None:

				try:
					clicks_button('add_all.png', .8)
					print('Clicked Add All')

					okfromadd = None

					while okfromadd is None:

						try:
							clicks_button('ok_after_all.png', .9)
							print('Confirmed Add')
							time.sleep(.5)

							okclear = None

							while okclear is None:

								try:
									clicks_button('ok_to_confirm.png', .8)
									print('Clearing all DTCS')
									break

								except TypeError:

									try:
										clicks_button('ok_no_comm_error.png', .8)
										print('Clearing all DTCS Exception')
										break

									except TypeError:
										okclear = None
									else:
										return

						except TypeError:
							okfromadd = None
						else:
							return

				except TypeError:
					addall = None
				else:
					return

		except TypeError:
			faults = None
		else:
			return

	return


def close_GDS2():

	global report_finished
	looking_for_back = None

	while looking_for_back is None:

		try:
			clicks_button('back_button.png', .9)
			print('Backing out')
			time.sleep(2)
			break

		except TypeError:
			looking_for_back = None

	homeButton = None

	while homeButton is None:

		try:
			clicks_button('home_button.png', .9)
			print('Clicked Home')
			break

		except TypeError:
			homeButton = None

	closeapp = None

	while closeapp is None:

		try:
			clicks_button('close_application.png', .8)
			print('GDS2 is now closed.  Exiting AutoReport')
			py.alert("Please Copy faults and close the report, Click Ok when finished")
			report_finished = 1
			break
			

		except TypeError:
			closeapp = None
	return


def all_modules_scanned():

	print('Scanning modules now')

	global module_scanned, module_range, scan_timer
	timer = 0
	scan_count = 5
	module_range = 0

	start = time.time()

	print('Scan Count: ' + str(scan_count))

	while module_range != scan_count - 1:

		for module_range in range(scan_count):

			try:
				py.click(1460, 277)
				module_scanned = py.locateCenterOnScreen('module_not_scanned_two.png', confidence=.7)
				module_scanned_redundant = py.locateCenterOnScreen('module_not_scanned.png', confidence=.7)
				py.scroll(-3000)

				if module_scanned and module_scanned_redundant is not None:
					module_range -= 1
					print(module_scanned)
					print('Scan Count in not None: ' + str(scan_count))
					print('Module Range in not None: ' + str(module_range))
					timer += 1  # sets up for second time scanning the faults
					time.sleep(module_range)

				elif module_scanned and module_scanned_redundant is None:
					print('Scan Count in None: ' + str(scan_count))
					print('Module Range in None: ' + str(module_range))

				continue

			except:

				print('Searching for unscanned modules')

				if module_range == scan_count:
					break

				else:
					time.sleep(1)

	end = time.time()

	print('Starting Timer')
	print('Scan Count: ' + str(scan_count))
	print('Module Range: ' + str(module_range))

	#if timer < 8:
	#	timer = 10
	#print(timer)
	timer_two = end - start
	#print(timer_two)
	scan_timer = timer + timer_two
	print(scan_timer)
	#time.sleep(scan_timer)

	print('All modules scanned once')

	py.scroll(3000)

	return scan_timer


def faults_found():

	global active_faults

	if active_faults > 3:

		print('Found and clearing faults')

		create_report()
		minimize_report()
		time.sleep(2)
		clear_faults()
		active_faults = 0
		return

	return


def faults_found_prescan():

	global active_faults

	if active_faults > 3:

		print('Found Faults')

		create_report()
		minimize_report()
		time.sleep(2)
		close_GDS2()
		return

	return


def faults_found_after_clear():

	global active_faults, faultsPresent

	if active_faults > 3:

		print('Faults Still Remain')

		faultsPresent = 1

		return


def no_faults_found():

	global active_faults

	if active_faults > 3:

		print('No Faults found')

		create_report()
		minimize_report()
		close_GDS2()

	return


def no_faults_found_after_clear():

	global active_faults

	if active_faults > 3:

		create_report()

		print('No Faults found')

		close_GDS2()

	return

#call different function, not sys.exit()
def close_GDS2_after_error():

	global errorSet
	backButton = None

	while backButton is None:

		try:
			clicks_button('back_button.png', .9)
			time.sleep(2)
			print('Pressed Back Button')
			break

		except TypeError:
			backButton = None

	closeApplication = None

	while closeApplication is None:

		try:
			clicks_button('close_application.png', .8)
			print('Closed GDS2')
			errorSet = 1
			print('errorSet = 1')
			break

		except TypeError:
			closeApplication = None
	return

	


# Program

def preScanSelection():

	# Variables
	global active_faults, scan_timer, errorSet
	tries = 0
	secondTry = 0
	activescan = None
	enterdtcscan = None
	vehiclediagnostics = None
	confirmedVehicle = None
	selectDevice = None
	diagHome = None
	maximize = None
	#zoom = None
	opening = None

	# Functions
	def noCommPopUp(message):

		global errorSet
		root = tk.Tk()
		root.withdraw()

		msg = tk.messagebox.askyesno("Communication Error", message)

		if msg == True:
			return

		else:
			errorSet = 1
			close_GDS2_after_error()
			return


	# Program
	print('Running PreScan Selection.  Faults will not be cleared')

	while opening is None:
		try:
			gds_x, gds_y = py.locateCenterOnScreen('gds2_icon.png', confidence=.8)
			gds2_icon = gds_x, gds_y
			py.click(gds2_icon, clicks=2, interval=.15)
			print('GDS2 Opened')
			break

		except TypeError:
			try:
				py.click('gds2_icon.png', clicks=2, interval=.15)
				print('GDS2 Opened Exception')
				break

			except TypeError:
				py.click(1460, 277)
				print('Waiting')
				opening = None


	while maximize is None:
		try:
			up_x, up_y = py.locateCenterOnScreen('gds2_left_corner.png', confidence=.7)
			right_click = up_x, up_y
			py.click(right_click, button='right')

			maxi = None

			while maxi is None:
				try:
					clicks_button('maximize_screen.png', .9)
					print("Maximized")
					time.sleep(1)
					py.moveTo(1460, 277)
					break

				except:
					maxi = None

			break

		except:
			maximize = None

	while diagHome is None:
		try:
			clicks_button('diagnostics_main.png', 1)
			print('Diagnostics')
			break

		except TypeError:
			try:
				clicks_button('diagnostics_main.png', .9)
				print('Diagnostics Exception')
				break

			except TypeError:
				time.sleep(1.0)
				print('Please wait...')
				diagHome = None

	while selectDevice is None:
		try:
			clicks_button('astech_highlighted.png', .8)
			print('Selected asTech')
			time.sleep(0.5)
			clicks_button('continue_after_device.png', .9)
			print('Clicked Continue')
			break

		except TypeError:
			try:
				py.click(1460, 277)
				clicks_button('astech_not_highlighted.png', .9)
				print('Selected exception asTech')
				time.sleep(0.5)
				clicks_button('continue_after_device.png', .9)
				print('Clicked Continue')
				break

			except TypeError:
				print('Please wait...')
				time.sleep(1.0)
				selectDevice = None

	time.sleep(2)

	while confirmedVehicle is None:
		try:
			verify_enter = py.locateCenterOnScreen('enter_after_vehicle_selection_highlighted.png', None)
			verify_vehicle = py.locateCenterOnScreen('enter_verification_green.png', None)
			red_verify = py.locateCenterOnScreen('red_device.png', confidence=.8)
			if verify_enter and verify_vehicle is not None and red_verify is None:
				clicks_button('enter_after_vehicle_selection_highlighted.png', .9)
				print('Clicked Enter')

				warningok = None

				while warningok is None:
					try:
						clicks_button('ok_off_warning.png', .9)
						print('Clicked OK')
						break

					except TypeError:
						time.sleep(.05)
						warningok = None
			else:
				raise TypeError

			break

		except TypeError:
			try:
				verify_vehicle = py.locateCenterOnScreen('enter_verification_green.png', None)
				verify_enter_exception = py.locateCenterOnScreen('enter_after_vehicle_selection.png', None)
				red_verify = py.locateCenterOnScreen('red_device.png', confidence=.8)
				if verify_vehicle and verify_enter_exception is not None and red_verify is None:
					clicks_button('enter_after_vehicle_selection.png', .9)
					print('Clicked Enter Exception')

					warningok = None

					while warningok is None:
						try:
							clicks_button('ok_off_warning.png', .9)
							break

						except TypeError:
							time.sleep(.05)
							warningok = None
				else:
					raise TypeError
			
				break

			except TypeError:
				try:
					verify_exception_two = py.locateCenterOnScreen('enter_verification_green.png', None)
					verify_enter_exception_two = py.locateCenterOnScreen('enter_after_vehicle_selection_highlighted.png', None)
					red_verify = py.locateCenterOnScreen('red_device.png', confidence=.8)
					if verify_exception_two and verify_enter_exception_two is not None and red_verify is None:

						clicks_button('enter_after_vehicle_selection_highlighted.png', None)
						print('Clicked Enter Exception Two')

						warningok = None

						while warningok is None:
							try:
								clicks_button('ok_off_warning.png', .9)
								print('Clicked OK in Exception Two')
								break

							except TypeError:
								time.sleep(.05)
								warningok = None
					else:
						raise TypeError
					
					break

				except TypeError:
					try:
						if errorSet == 1:
							break
						else:
							clicks_button('ok_no_comm_error.png', .9)
							print('No Communication Error')
							time.sleep(10)
							tries += 1

					except TypeError:
						if tries == 1:
							print('On second try')
							secondTry = 1
							tries = 0
							time.sleep(5)
							print('Trying one more time')

						elif secondTry == 1:
							print('On third try')
							close_GDS2_after_error()

						else:
							print('Verifying Communication')
							if errorSet == 1:
								break
							else:
								time.sleep(1.0)
								confirmedVehicle = None
	
	
	if errorSet == 1:
		print('Ended prescan with error')

	else:
		while vehiclediagnostics is None:
			try:
				clicks_button('vehicle_diagnostics_not_highlighted.png', 1)
				print('Entering Complete Vehicle Mode')
				break

			except TypeError:
				try:
					clicks_button('vehicle_diagnostics_not_highlighted.png', .9)
					print('Entered Complete Vehicle Mode with Exception')
					break

				except TypeError:
					print('Waiting')
					time.sleep(1.0)
					vehiclediagnostics = None

		while enterdtcscan is None:
			try:
				clicks_button('vehicle_dtc_info_highlighted.png', 1)
				print('Scanning Now Active')
				break

			except TypeError:
				try:
					clicks_button('vehicle_dtc_info_highlighted.png', .9)
					print('Scanning off Exception')
					break

				except TypeError:
					print('Waiting')
					time.sleep(1.0)
					enterdtcscan = None

		time.sleep(3)

		while activescan is None:
			try:
				redundant_scan = py.locateCenterOnScreen('create_report.png')
				refresh_found = py.locateCenterOnScreen('refresh_button.png', confidence=1)

				if redundant_scan and refresh_found is not None:
					py.moveTo('refresh_button.png')
					print('On Scanning Screen')
					break

				else:
					raise TypeError
				break

			except TypeError:
				try:
					refresh_exception = py.locateCenterOnScreen('refresh_button.png', confidence=.9)
					redundant_scan = py.locateCenterOnScreen('create_report.png', confidence=.9)

					if refresh_exception and redundant_scan is not None:
						py.moveTo(refresh_exception)
						print('On Scanning Screen from Exception')
						break

					else:
						raise TypeError

					break

				except TypeError:
					try:
						clicks_button('enter_option.png', .8)
						print('Accepted Option')

					except TypeError:
						activescan = None

		all_modules_scanned()

		print('Timer up')

		for active_faults in range(5):
			try:
				py.click(800, 300)

				fault_present_one = py.locateCenterOnScreen('fault_present.png', confidence=.7)

				py.scroll(-3000)

				fault_present_redundent = py.locateCenterOnScreen('fault_present.png', confidence=.7)

				if fault_present_one or fault_present_redundent is not None:
					faults_found_prescan()
					print('faults found')
				else:
					py.scroll(3000)
					no_faults_found()
					print('no faults found')

			except:
				print('except')
				if active_faults == 4:
					break

				else:
					print(active_faults)
					print('here')

		return


def completionScanSelection():

	# Variables
	global active_faults, scan_timer, errorSet
	tries = 0
	secondTry = 0
	activescan = None
	selectDevice = None
	diagHome = None
	maximize = None
	#zoom = None
	opening = None
	confirmedVehicle = None
	vehiclediagnostics = None
	enterdtcscan = None

	# Functions
	def noCommPopUp(message):

		root = tk.Tk()
		root.withdraw()
		global errorSet

		msg = tk.messagebox.askyesno("Communication Error", message)

		if msg == True:
			return

		else:
			errorSet = 1
			close_GDS2_after_error()
			return

	# Actual Scanning
	print('Running Completion Scan Selection.  Faults will be cleared.')

	while opening is None:
		try:
			gds_x, gds_y = py.locateCenterOnScreen('gds2_icon.png', confidence=.8)
			py.click(py.moveTo(gds_x, gds_y), clicks=2, interval=.15)
			print('GDS2 Opened')
			break

		except TypeError:
			try:
				py.click('gds2_icon.png', clicks=2, interval=.15)
				print('GDS2 Opened Exception')
				break

			except TypeError:
				py.click(800, 300)
				print('Waiting')
				opening = None


	while maximize is None:
		try:
			up_x, up_y = py.locateCenterOnScreen('gds2_left_corner.png', confidence=.7)
			right_click = up_x, up_y
			py.click(right_click, button='right')

			maxi = None

			while maxi is None:
				try:
					clicks_button('maximize_screen.png', .9)
					print("Maximized")
					time.sleep(1)
					py.moveTo(1460, 277)
					break

				except:
					maxi = None

			break

		except:
			maximize = None


	while diagHome is None:
		try:
			clicks_button('diagnostics_main.png', 1)
			print('Diagnostics')
			break

		except TypeError:
			try:
				clicks_button('diagnostics_main.png', .9)
				print('Diagnostics Exception')
				break

			except TypeError:
				time.sleep(1.0)
				print('Please wait...')
				diagHome = None


	while selectDevice is None:
		try:
			clicks_button('astech_highlighted.png', .8)
			print('Selected asTech')
			time.sleep(0.5)
			clicks_button('continue_after_device.png', .9)
			print('Clicked Continue')
			break

		except TypeError:
			try:
				clicks_button('astech_not_highlighted.png', .9)
				print('Selected exception astech')
				time.sleep(0.5)
				clicks_button('continue_after_device.png', .9)
				print('Clicked Continue')
				break

			except TypeError:
				print('Please wait...')
				py.click(1460, 277)
				time.sleep(1.0)
				selectDevice = None

	time.sleep(3)

	while confirmedVehicle is None:
		try:
			verify_enter = py.locateCenterOnScreen('enter_after_vehicle_selection_highlighted.png', None)
			verify_vehicle = py.locateCenterOnScreen('enter_verification_green.png', None)
			red_verify = py.locateCenterOnScreen('red_device.png', confidence=.8)
			if verify_enter and verify_vehicle is not None and red_verify is None:
				clicks_button('enter_after_vehicle_selection_highlighted.png', .9)
				print('Clicked Enter')
				warningok = None
				while warningok is None:
					try:
						clicks_button('ok_off_warning.png', .9)
						print('Clicked OK')
						break
					except TypeError:
						time.sleep(.05)
						warningok = None
			else:
				raise TypeError

			break

		except TypeError:
			try:
				verify_vehicle = py.locateCenterOnScreen('enter_verification_green.png', None)
				verify_enter_exception = py.locateCenterOnScreen('enter_after_vehicle_selection.png', None)
				red_verify = py.locateCenterOnScreen('red_device.png', confidence=.8)

				if verify_vehicle and verify_enter_exception is not None and red_verify is None:
					clicks_button('enter_after_vehicle_selection.png', .9)
					print('Clicked Enter Exception')
					warningok = None
					while warningok is None:
						try:
							clicks_button('ok_off_warning.png', .9)
							break
						except TypeError:
							time.sleep(.05)
							warningok = None
				else:
					raise TypeError
			
				break

			except TypeError:
				try:
					clicks_button('enter_selection_highlighted_two.png', 1)
					print('Clicked Enter Exception Two')
					warningok = None
					while warningok is None:
						try:
							clicks_button('ok_off_warning.png', .9)
							print('Clicked OK in Exception Two')
							break
						except TypeError:
							time.sleep(.05)
							warningok = None
					break

				except TypeError:
					try:
						if errorSet == 1:
							break
						else:
							clicks_button('ok_no_comm_error.png', .9)
							print('No Communication Error')
							time.sleep(5)
							tries += 1

					except TypeError:
						if tries == 1:
							print('On second try')
							secondTry = 1
							tries = 0
							time.sleep(5)
							print('Trying one more time')

						elif secondTry == 1:
							print('On third try')
							close_GDS2_after_error()

						else:
							print('Verifying Communication')
							if errorSet == 1:
								break
							else:
								time.sleep(1.0)
								confirmedVehicle = None


	if errorSet == 1:
		print('Ended prescan with error')

	else:
		while vehiclediagnostics is None:
			try:
				clicks_button('vehicle_diagnostics_not_highlighted.png', 1)
				print('Entering Complete Vehicle Mode')
				break

			except TypeError:
				try:
					clicks_button('vehicle_diagnostics_not_highlighted.png', .9)
					print('Entered Complete Vehicle Mode with Exception')
					break

				except TypeError:
					print('Waiting')
					time.sleep(1.0)
					vehiclediagnostics = None

		while enterdtcscan is None:
			try:
				clicks_button('vehicle_dtc_info_highlighted.png', 1)
				print('Scanning Now Active')
				break

			except TypeError:
				try:
					clicks_button('vehicle_dtc_info_highlighted.png', .9)
					print('Scanning off Exception')
					break

				except TypeError:
					print('Waiting')
					time.sleep(1.0)
					enterdtcscan = None

		time.sleep(3)

		while activescan is None:
			try:
				redundant_scan = py.locateCenterOnScreen('create_report.png')
				refresh_found = py.locateCenterOnScreen('refresh_button.png', confidence=1)
				if redundant_scan and refresh_found is not None:
					py.moveTo('refresh_button.png')
					print('On Scanning Screen')
					break
				else:
					raise TypeError 
				break

			except TypeError:
				try:
					refresh_exception = py.locateCenterOnScreen('refresh_button.png', confidence=.9)
					redundant_scan = py.locateCenterOnScreen('create_report.png', confidence=.9)
					if refresh_exception and redundant_scan is not None:
						py.moveTo(refresh_exception)
						print('On Scanning Screen from Exception')
						break
					else:
						raise TypeError
					break

				except TypeError:
					try:
						clicks_button('enter_option.png', .8)
						print('Accepted Option')

					except TypeError:
						activescan = None

		all_modules_scanned()

		print('Timer up')

		for active_faults in range(5):
			try:
				py.click(800, 300)

				fault_present_one = py.locateCenterOnScreen('fault_present.png', confidence=.7)

				py.scroll(-3000)

				fault_present_redundent = py.locateCenterOnScreen('fault_present.png', confidence=.7)

				if fault_present_one or fault_present_redundent is not None:
					faults_found()

				else:
					py.scroll(3000)
					no_faults_found()

			except:
				if active_faults == 4:
					break

				else:
					print(active_faults)
		# catch clearing errors better
		while activescan is None:
			try:
				redundant_scan = py.locateCenterOnScreen('create_report.png')
				refresh_found = py.locateCenterOnScreen('refresh_button.png', confidence=1)
				if redundant_scan and refresh_found is not None:
					py.moveTo('refresh_button.png')
					print('On Scanning Screen')
					break
				else:
					continue
			except TypeError:
				try:
					refresh_exception = py.locateCenterOnScreen('refresh_button.png', confidence=.9)
					redundant_scan = py.locateCenterOnScreen('create_report.png', confidence=.9)
					if refresh_exception and redundant_scan is not None:
						py.moveTo(refresh_exception)
						print('On Scanning Screen from Exception')
						break
					else:
						continue

				except TypeError:
					try:
						clicks_button('ok_off_warning.png', 1)
						print('There were errors clearing faults')
						py.alert('There was errors clearing faults')
						break

					except TypeError:
						activescan = None

		print(scan_timer)
		time.sleep(scan_timer)

		print('Second Timer Up')

		for active_faults in range(5):
			try:
				py.click(800, 300)

				fault_present_one = py.locateCenterOnScreen('fault_present.png', confidence=.7)

				py.scroll(3000)

				fault_present_redundent = py.locateCenterOnScreen('fault_present.png', confidence=.7)

				if fault_present_one or fault_present_redundent is not None:
					faults_found_after_clear()
					break
				else:
					py.scroll(-3000)
					no_faults_found_after_clear()

			except:
				print('Scanning For Faults')
				if active_faults == 4:
					break

				else:
					print(active_faults)

		return


#Verify Screensize is correct to prevent errors, return error to db, not sys.exit()
screen_x, screen_y = py.size()
if screen_x == 1536 and screen_y == 864:
	print('Screen Size Acceptable')
else:
	print('Unable to run techAssist')
	

# Selection for pre-scan or not



##Take all out when server/db controlled

#root = tk.Tk()
#root.withdraw()

#time_started = time.time()

#msg = tk.messagebox.askquestion("Scan Type", "Is this a Pre-Scan", type='yesnocancel')

#if msg == 'yes':
#	time.sleep(2)
#	preScanSelection()  # prescan function
#
#elif msg == 'no':
#	time.sleep(2)
#	completionScanSelection()  # completion scan function
#
#elif msg == 'cancel':
#	sys.exit(-1)

#if pre_scan == True:
#	preScanSelection()
#elif completion_scan == True:
#	completionScanSelection()
#else:
#	sys.exit(-1)
#time_ended = time.time()
#total_scan_time = time_ended - time_started
#print(total_scan_time)

#sys.exit(-1)
