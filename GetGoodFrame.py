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
	
	"""If set to True, frames that are 'too blurry' will be ignored"""
	analyseBlurriness = True
	"""Avg. edge strength (moving exponential average). Used to decide if frame is too blurry"""
	avgEdgeStrength = 0
	"""If current edge strength is less than this fraction of the moving average, it will be considered too blurry for processing"""
	blurrinessThreshold = 0.8

	def run(self, params):
		"""override: If there has been sufficient change in scene and the frame is not blurry return the frame. Else returns None"""
		print "Considering frame 932864", self.curChangeAmount, self.avgEdgeStrength
		frame = ndimage.gaussian_filter(params[0][0], sigma=5)
		if self.prevFrame == None:
			self.prevFrame = frame
			return None
		
		meanDiff = np.mean(frame.flatten() - self.prevFrame.flatten())
		self.prevFrame = frame
		self.curChangeAmount += meanDiff
		if self.curChangeAmount < self.changeThreshold:
			return None

		if self.analyseBlurriness:

			edgeStrength = np.mean(ndimage.sobel(frame, axis=0, mode='constant'))
			edgeStrength += np.mean(ndimage.sobel(frame, axis=1, mode='constant'))
			if edgeStrength < self.blurrinessThreshold*self.avgEdgeStrength:
				self.avgEdgeStrength += edgeStrength
				self.avgEdgeStrength /= 2
				return None
			
			self.avgEdgeStrength += edgeStrength
			self.avgEdgeStrength /= 2

		self.curChangeAmount = 0
		print "Frame accepted 42243"
		return params[0]

