"""
Computation Module:
	If there has been sufficient change in scene and the frame is not blurry 
	return the frame. Else returns None.
"""

import cv2
import numpy as np
from scipy import ndimage
import time

from Computation import Computation
from GetFrame import GetFrame

class GetGoodFrame(Computation):
	dependancies = [GetFrame]

	"""The previous frame (to calculate differences with)"""
	prevFrame = None

	"""Threshold after shich sufficient change is assumed to have occured"""
	changeThreshold = 10
	"""The acceptable probability of exceeding the changeThreshold given as number of standard deviations"""
	probError = 2
	""""Estimated mean of normally distributed change per unit time"""
	meanChangeRate = 1 #some arbitrary value. Will converge to more sensible values
	""""Estimated variance of normally distributed change per unit time"""
	varChangeRate = 1 #some arbitrary value that will converge to sensible value as system evolves
	""""Time stamp of the last time the function was called"""
	prevAwakeTime = time.time()

	"""If set to True, the least 'blurry' frame will be used"""
	analyseBlurriness = True
	"""The least blurry frame as measured using average edge strength"""
	bestFrame = None
	"""Highest average edge strength in current lot"""
	bestBlurrinessScore = -1 #-ve infinity
	

	def run(self, params):
		"""override: If there has been sufficient change in scene and the frame is not blurry return the frame. Else returns None"""
		#print "Considering frame 932864", self.curChangeAmount, self.bestBlurrinessScore
		#frame = cv2.cvtColor(ndimage.gaussian_filter(params[0][0], sigma=5), cv2.COLOR_BGR2GRAY)
		frame1 = cv2.GaussianBlur(params[0][0], (3,3), 0)
		frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
	
		scale = 1
		delta = 0
		ddepth = cv2.CV_16S	
		grad_x = cv2.Sobel(frame1,ddepth,1,0,ksize = 3, scale = scale, delta = delta,borderType = cv2.BORDER_DEFAULT)
		#grad_x = cv2.Scharr(gray,ddepth,1,0)
		# Gradient-Y
		grad_y = cv2.Sobel(frame1,ddepth,0,1,ksize = 3, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)
		#grad_y = cv2.Scharr(gray,ddepth,0,1)
		abs_grad_x = cv2.convertScaleAbs(grad_x) # converting back to uint8
		abs_grad_y = cv2.convertScaleAbs(grad_y)
		frame1 = cv2.addWeighted(abs_grad_x,0.5,abs_grad_y,0.5,0)

		frame1 = cv2.threshold(frame1, 50, 255, cv2.THRESH_TOZERO)[1]
		
		if self.prevFrame == None:
			self.prevFrame = frame1
			return None
		
		meanDiff = np.mean(np.abs(frame1.flatten() - self.prevFrame.flatten()))
		print "Analysing frame 238456", meanDiff, self.meanChangeRate

		#Analyse meanDiff and pause for a while
		curTime = time.time()
		meanDiffPerUnitTime = meanDiff/(curTime - self.prevAwakeTime)
		self.prevAwakeTime = curTime

		self.varChangeRate = (self.varChangeRate + (meanDiffPerUnitTime - self.meanChangeRate)**2)/2
		self.meanChangeRate = (self.meanChangeRate + meanDiffPerUnitTime)/2
		if meanDiff < self.changeThreshold:
			if self.meanChangeRate - self.varChangeRate*self.probError < 0.001: #anyway most operating systems (esp. linux, windows is better) will not be able to sleep for less than 1ms
				return None
			time.sleep(self.changeThreshold/(self.meanChangeRate - self.varChangeRate*self.probError))
			return None


		if self.analyseBlurriness:
			#edgeStrength = np.mean(ndimage.sobel(frame, axis=0, mode='constant'))
			#edgeStrength += np.mean(ndimage.sobel(frame, axis=1, mode='constant'))
			edgeStrength = np.mean(frame1)
			if edgeStrength >= self.bestBlurrinessScore:
				self.bestBlurrinessScore = edgeStrength
				self.bestFrame = params[0]

		self.bestBlurrinessScore = -1
		self.curChangeAmount = 0
		self.prevFrame = frame1
		print "Frame accepted 42243"
		return params[0]

