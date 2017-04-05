#!/bin/python
import time
import requests
import datetime

class WaterScheduler (object):
	def __init__ (self, numZones = 1, sensors = [], timeSliceSize = 10):
		"""
			numZones must be greater than 0. Default is 1
			sensors is an array of tuples listing the min and max values that can
			        be received from the sensors. The default is empty (no sensors)
			timeSliceSize defines the length of the smallest amount of time in minutes
					we care about using. The default is 10 minutes. So we will carry
					out watering only to the nearest 10 minute increment.
		
			All of these class variables can and should be used by update
		"""

		with open ("wu_api_key.conf", "r") as f:
			self.api_key = f.readline().strip();
		#
		self.numZones = numZones
		self.zone = [] #track data per zone
		self.sensors = sensors #array of sensor names and 
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
		