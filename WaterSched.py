#!/bin/python
import time
import requests
import datetime
import math
from collections import deque

class WaterScheduler (object):
	def __init__ (self, numZones = 1, sensors = {}, timeSliceSize = 10):
		"""
			numZones must be greater than 0. Default is 1
			sensors is a dictionary of tuples listing the min and max values that can
			        be received from the sensors. The default is empty (no sensors)
			timeSliceSize defines the length of the smallest amount of time in minutes
					we care about using. The default is 10 minutes. So we will carry
					out watering only to the nearest 10 minute increment.
		
			All of these class variables can and should be used by update
		"""
		self.name = "default"

		with open ("wu_api_key.conf", "r") as f:
			self.api_key = f.readline().strip();
		#
		self.numZones = numZones
		self.zone = [] #track data per zone
		self.sensors = sensors #dictionary of sensor names and 
							   #acceptable range of values as a tuple
		self.timeSliceSize = timeSliceSize 
		self.timeSlices = 24 * 60 / timeSliceSize #for convenience so we don't have to calc every time
		self.wateringSchedule = [[0 for col in xrange(self.timeSlices)] for row in xrange(self.numZones)]
	def _getSunriseSunset (self):
		"""
			Using Wunderground API get sunrise time and sunset times
			http://api.wunderground.com/api/self.api_key/astronomy/q/IN/Notre_Dame.json

			Returns two tuples of the form (hour, minute) both ints

			Intended to be used by update
		"""
		data = requests.get('http://api.wunderground.com/api/'+self.api_key+'/astronomy/q/IN/Notre_Dame.json').json()
		sunrise = (int(data["sun_phase"]["sunrise"]["hour"]), int(data["sun_phase"]["sunrise"]["minute"]))
		sunset = (int(data["sun_phase"]["sunset"]["hour"]), int(data["sun_phase"]["sunset"]["minute"]))

		return sunrise, sunset

	def _getTimeSlice (self, hour, min):
		"""
			Return the index of the time slice based on the hour and minute
		"""
		return (hour * 60 + min) / self.timeSliceSize

	def _getRainData(self, window):
		"""
			Get data using Wunderground API
			 
			NOTE: window is in hours as a forecast
			current: http://api.wunderground.com/api/self.api_key/conditions/q/IN/Notre_Dame.json
			history: http://api.wunderground.com/api/self.api_key/history_YYYYMMDD/q/IN/Notre_Dame.json
			forecast: http://api.wunderground.com/api/self.api_key/hourly/q/IN/Notre_Dame.json

			Returned arrays can be empty

			Intended to be used by update
		"""
		chanceOfRain = [] #hourly chance up to window
		amountOfRain = [] #estimates of amount of rain in window
		
		if window > 0 and window <= 36:
			data = requests.get ('http://api.wunderground.com/api/'+self.api_key+'/hourly/q/IN/Notre_Dame.json').json()
			#print data["hourly_forecast"][1]["pop"]
			for hour in xrange(window):
				#pop = probability of precipitation
				chanceOfRain.append(float(data["hourly_forecast"][hour]["pop"]))
				#qpf = quantity of precipitation
				amountOfRain.append(float(data["hourly_forecast"][hour]["qpf"]["metric"]))
		elif window == 0:
			pass
	
		return chanceOfRain, amountOfRain
	def getSensorData (self, zone, sensorName, window):
		"""
			keys for sensor names should match. Used to get data for watering
			decisions

			data is expected to be kept under ./data

			zone indentifies the spike (XBee id?)
			sensorName identifies the data you're looking for (CMS, RMS, etc.)
			window indicates how much data you're looking for (how many lines to read
			from the end)

			Note that accessing this data should be wrapped up in the class to
			provide abstraction for the *actual* method of storage used. Add'l
			someone needs to translate from indices to XBee IDs, and I don't think
			it should be this module
		"""
		with open ("./data/" + zone + "-" + sensorName + ".txt") as f:
			data = deque(f, maxlen=window)

		return data

	
	def update (self):
		"""
			Use this to update self.wateringSchedule
			This method should be altered for different scheduling methods

			should not return anything
		"""
		pass

	def getNextZoneWatering (self, zone, threshold = 1):
		"""
			Depending on the current time, the selected zone, and the
			given threshold to cross before watering, find the next
			watering time and its duration.

			Returns two values: a tuple (hour, min) and an int

			return these two values as a tuple (beginWatering, duration)
		"""

		currentTime = datetime.datetime.time(datetime.datetime.now())
		currentTimeSlice = (currentTime.hour * 60 + currentTime.minute) / self.timeSliceSize
		#Find next grouping of values greater than or equal to threshold
		# in self.wateringSchedule for zone
		beginSlice = -1
		numSlices = 0
		for t in range(currentTimeSlice, self.timeSlices):
			if self.wateringSchedule[zone][t] >= threshold:
				if -1 == beginSlice:
					beginSlice = t
				
				numSlices += 1
			elif (self.wateringSchedule[zone][t] < threshold 
				  and -1 != beginSlice):
				break

		#calculate clock time of beginning and end
		beginWatering = 0
		duration = 0 #minutes

		if -1 != beginSlice:
			beginWatering = ((beginSlice * self.timeSliceSize) / 60, (beginSlice * self.timeSliceSize) % 60)
			duration = numSlices * self.timeSliceSize

		return beginWatering, duration
		

class dawnDuskScheduler (WaterScheduler):
	"""
		Water 20 minutes before sunrise and 2 minutes
		after sunset. Of course, we can control the time slice
		size, so we simply set our duration at the top
	"""
	def __init__ (self, numZones = 1, sensors = {}, timeSliceSize = 10):
		self.name = "dawn-dusk"
		super(dawnDuskScheduler, self).__init__(numZones, sensors, timeSliceSize)

	def update (self):
		duration = 20 / self.timeSliceSize
		sunrise,sunset = self._getSunriseSunset();
		sunRiseSlice = self._getTimeSlice(sunrise[0], sunrise[1])
		sunSetSlice = self._getTimeSlice(sunset[0], sunset[1])

		for z in range(self.numZones):
			for t in range(sunRiseSlice - duration, sunRiseSlice):
				self.wateringSchedule[z][t] = 1;

			for t in range(sunSetSlice, sunSetSlice + duration):
				self.wateringSchedule[z][t] = 1;

class sensorBasedScheduler (WaterScheduler):
	"""
		Could also be called the as-needed scheduler. The idea is that
		scheduling / watering is based on sensor inputs from spikes and
		weights.

		The following sensors are expected to be available on the garden
		spikes:

		Resistive moisture sensor - "RMS"
		Capacitive moisture sensor = "CMS"
		Photoresistor = "light"
		Analog temperatre sensor = "temp"

		If a sensor dictionary is not passed in (with the names and (min,max)
		tuple), then the default min and max will be used. Note that these
		default values simply correspond to the range of a 10 bit ADC (0,1023).
		The main reasoning behind allowing a sensor dictionary to be passed in
		is to allow calibrated values to be entered based on the use of voltage
		dividers and the *actual* range of possible values.

	"""
	def __init__ (self, numZones = 1, sensors = {}, timeSliceSize = 10):
		self.name = "sensor-based"
		if {} == sensors:
			sensors["RMS"] = (0,1023)
			sensors["CMS"] = (0,1023)
			sensors["temp"] = (0,1023)
			sensors["light"] = (0,1023)

		super(sensorBasedScheduler, self).__init__(numZones, sensors, timeSliceSize)

	def addWeights(self, weight = {}):
		"""
			Add weights for the sensors based on how much they contribute to the
			chance of watering in the next time slice. A weight is more than just
			a coefficient, it's a polynomial represented as:
			weight["sensor"] = [a0, a1, a2, ..., an] where each ai is a coefficient
			for the corresponding order in the polynomial. As you might have guessed,
			the role of x is played by the sensor value. Defining the weight in this
			way should provide enough flexibility to properly model the relation
			between the sensor and the chance of watering.

			By the way, I'm fairly certain there is something in numpy for this,
			but I don't have the time to investigate that at the moment 
		"""
		if {} == weight:
			for key in self.sensors:
				weight[key] = [0]
		self.weight = weight

	def update(self):
		#Get latest measurements
		for z in range(self.numZones):
			things = {}
			for key in sensors:
				things[key] = int(self.getSensorData(z,key,1).split(",")[0])
			
			self.zone[z] = things

		now = datetime.datetime.now()
		t = self._getTimeSlice(now.hour, now.minute)
		val = [0.0 for i in range(len(self.sensors))]
		for z in range(self.numZones):
			for i, key in enumerate(len(self.sensors)):
				for p,w in enumerate(self.weight[key]):
					val[i] += w * math.pow(self.zone[z][key],p) 
			self.wateringSchedule[z][t+1] = sum(val)

def advancedScheduler (WaterScheduler):
	"""
		Take EVERYTHING into account for watering!
	"""
	pass
