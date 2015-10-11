"""
Computation Module:
	If there has been sufficient change in scene and the frame is not blurry 
	return the frame. Else returns None.
"""

import cv
import cv2
import numpy as np
from scipy import ndimage
import time

from Computation import Computation
from GetFrame import GetFrame

class GetGoodFrame(Computation):
	dependancies = [GetFrame]

	"""The previous frame (to calculate differences with)"""
	prevFrameRunningAvg = None

	"""Threshold after shich sufficient change is assumed to have occured"""
	changeThreshold = 3
	"""Time to sleep (in sec) in case no significant change is detected"""
	sleepTime = 0.5
	"""Image blur amount along (x,y) axis."""
	blurAmt = (3,3)
	"""Alpha for calculating running average of image"""
	imgRunningAvgAlpha = 0.3

	def run(self, params):
		"""override: If there has been sufficient change in scene and the frame is not blurry return the frame. Else returns None"""
		# To get rid of camera artefacts
		frame1 = cv2.GaussianBlur(params[0][0], self.blurAmt, 0)
		frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

		frame1 = cv.fromarray(frame1)

		if self.prevFrameRunningAvg == None:
			self.prevFrameRunningAvg = cv.CreateImage(cv.GetSize(frame1),32,1) # image to store running avg

		cv.RunningAvg( frame1, self.prevFrameRunningAvg, self.imgRunningAvgAlpha, None )

		meanDiff = np.mean(np.abs(np.asarray(frame1[:,:]).flatten() - np.asarray(self.prevFrameRunningAvg[:,:]).flatten()))

		# To study change levels
		# print "Mean Difference: ", meanDiff

		if meanDiff < self.changeThreshold:
			time.sleep(self.sleepTime)
			return None

		return params[0]

