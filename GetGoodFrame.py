"""
Computation Module:
	If there has been sufficient change in scene and the frame is not blurry 
	return the frame. Else returns None.
"""

import cv2
import numpy as np
from scipy import ndimage

from Computation import Computation
from GetFrame import GetFrame

class GetGoodFrame(Computation):
	dependancies = [GetFrame]

	"""The previous frame (to calculate differences with)"""
	prevFrame = None

	"""Threshold after shich sufficient change is assumed to have occured"""
	changeThreshold = 500
	"""The current amount of change that has gone unprocessed"""
	curChangeAmount = 0
	
	"""If set to True, the least 'blurry' frame will be used"""
	analyseBlurriness = True
	"""The least blurry frame as measured using average edge strength"""
	bestFrame = None
	"""Highest average edge strength in current lot"""
	bestBlurrinessScore = -1 #-ve infinity
	

	def run(self, params):
		"""override: If there has been sufficient change in scene and the frame is not blurry return the frame. Else returns None"""
		print "Considering frame 932864", self.curChangeAmount, self.bestBlurrinessScore
		frame = ndimage.gaussian_filter(params[0][0], sigma=5)
		if self.prevFrame == None:
			self.prevFrame = frame
			return None
		
		meanDiff = np.mean(frame.flatten() - self.prevFrame.flatten())
		self.prevFrame = frame
		self.curChangeAmount += meanDiff

		if self.analyseBlurriness:
			edgeStrength = np.mean(ndimage.sobel(frame, axis=0, mode='constant'))
			edgeStrength += np.mean(ndimage.sobel(frame, axis=1, mode='constant'))
			
			if edgeStrength >= self.bestBlurrinessScore:
				self.bestBlurrinessScore = edgeStrength
				self.bestFrame = params[0]

		if self.curChangeAmount < self.changeThreshold:
			return None

		self.bestBlurrinessScore = -1
		self.curChangeAmount = 0
		print "Frame accepted 42243"
		return params[0]

