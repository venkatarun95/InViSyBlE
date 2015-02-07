import cv2

from Computation import Computation
from GetBWFrame import GetBWFrame

class SIFTKeypoints(Computation):
	dependancies = [GetBWFrame]
	"""override: the computations that this depends on"""

	sift = cv2.SIFT()

	def run(self, params):
		"""override: Compute and return SIFT keypoints and their descriptors from the frame"""
		frame = params[0] #format: (frameData, frameId)
		kp, descrs = self.sift.detectAndCompute(frame[0], None)

		return (kp, descrs, frame[1])
		#return (cv2.drawKeypoints(frame[0],kp), frame[1])