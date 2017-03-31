#!/bin/python
import time

class WaterScheduler (object):
	def __init__ (self, numZones, sensors = [], timeSliceSize = 10):
		self.numZones = numZones
		self.zone = [] #track data per zone
		self.sensors = sensors #array of sensor names and 
							   #acceptable range of values as a tuple
		self.timeSlices = 24 * 60 / timeSliceSize
		self.zoneWateringSchedule = [[0 for col in xrange(self.timeSlices)] for row in xrange(self.numZones)]
	def _getSunriseSunset (self):
		"""
			Using Wunderground API get sunrise time and sunset times
		
			Intended to be used by update
		"""
		sunrise = 0;
		sunset = 0
		return (sunrise, sunset)

	def _getRainData(self, window):
		"""
			Get data using Wunderground API
			window can be negative, in which case we will not use
			chanceOfRain and instead look at amount of rain in the
			past up to window into the past

			Intended to be used by update
		"""
		chanceOfRain = [] #hourly chance up to window
		amountOfRain = [] #estimates of amount of rain in window
		return (chanceOfRain, amountOfRain)
	
	def update (self):
		"""
			Use this to update self.zoneWateringSchedule
			This method should be altered for different scheduling methods

			should not return anything
		"""
		pass

	def getNextZoneWatering (self, zone, threshold = 1):
		"""
			Depending on the current time, the selected zone, and the
			given threshold to cross before watering, find the next
			watering time and its duration.

			return these two values as a tuple (beginWatering, duration)
		"""
		currentTime = 
		currentTimeSlice = currentTime
		#Find next grouping of values greater than or equal to threshold
		# in self.zoneWateringSchedule for zone

		#calculate clock time of beginning and end
		beginWatering = 0
		duration = 5 #minutes
		return (beginWatering, duration)