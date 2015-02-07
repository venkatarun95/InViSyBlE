import cv2

from Computation import Computation
from GetBWFrame import GetBWFrame

class FaceDetector(Computation):
	dependancies = [GetBWFrame]
	"""override: the computations that this depends on"""

	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	"""The Haar based face detector"""

	def run(self, params):
		"""override: Find the face and return a rectangle"""
		grayFrame = params[0][0]
		faces = self.face_cascade.detectMultiScale(grayFrame, 1.3, 5)
		return faces
