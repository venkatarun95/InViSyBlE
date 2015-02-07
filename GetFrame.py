import cv2

from Computation import Computation

class GetFrame(Computation):
	dependancies = []

	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		self.frameId = 0

	def __del__(self):
		assert(self.cap.isOpened())
		self.cap.release()

	def run(self, params):
		"""override: Called by __call__ of Computation. Return the frame given by frameId
		Keyword arguments:
		params -- a type(frameId, rememberType)

		Returns -- tuple (frame, frameId)

		Not True:
		##frameId - numerical identifier returned by this function. If 0, current frame is returned
		##rememberType - 0 = delete frame after returning it, 1 = remember this frame (only if frameId = 0)
		"""
		#assert(params[0] == 0) #other functions are not implemented yet
		#assert(params[1] == 0)
		if self.cap.isOpened():
			ret, frame = self.cap.read()
			self.frameId += 1
			return (frame, self.frameId)
		else:
			ErrorReporting.reportProgramError("Unable to read frame. The capture device is not opened")
