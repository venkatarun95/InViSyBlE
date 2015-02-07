import cv2
import numpy as np

from Computation import Computation
from GetFrame import GetFrame

class GetBWFrame(Computation):
	dependancies = [GetFrame]
	def run(self, params):
		"""override: Convert current frame to black and white. Given argument contains (frame, frameId). Warning: Currently assumes input is BGR"""
		params = params[0]
		assert(type(params[0]) is np.ndarray)
		return (cv2.cvtColor(params[0], cv2.COLOR_BGR2GRAY), params[1])