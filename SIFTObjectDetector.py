import cv2
import numpy as np
import os

from Computation import Computation
from GetBWFrame import GetBWFrame
from SIFTKeypoints import SIFTKeypoints

classifier = None
"""Classifier based on kNN method. Refer: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_ml/py_knn/py_knn_understanding/py_knn_understanding.html#knn-understanding"""
labels = []
"""String labels corresponding to the label ids returned by classifier"""
noKeypoints = []
"""The number of keypoints for each object"""

def loadDatabase(dirName):
	print "Loading images from the object database..."
	files = os.listdir(dirName)
	sift = cv2.SIFT()
	Id = 0

	objKeyptDescr = [] #np.ndarray(shape=(0, 128), dtype=np.float32)
	"""Format: List of descriptors"""
	labelIds = [] #np.ndarray(shape=(0), dtype=np.int)
	"""Label ids for the descriptors"""
	global labels, noKeypoints

	for name in files:
		(shortname, extension) = os.path.splitext(name)
		if extension in ['.jpg', '.png', '.jpeg']:
			print "Loading ", shortname, "..."
			img = cv2.imread(os.path.join(dirName, name))#, cv2.IMREAD_GRAYSCALE)
			#cv2.imshow(shortname,img)
			kp, descrs = sift.detectAndCompute(img, None)
			for d in descrs:
				objKeyptDescr += [d]#np.append(objKeyptDescr, d)
				labelIds += [Id]#np.append(labelIds, Id)
			labels += [shortname]
			noKeypoints += [len(descrs)]
			Id += 1

	global classifier
	classifier = cv2.KNearest()
	classifier.train(np.array(objKeyptDescr),np.array(labelIds))

class SIFTObjectDetector(Computation):
	dependancies = [GetBWFrame, SIFTKeypoints]
	"""override: the computations that this depends on"""

	keypointMatchThreshold = 0.7
	"""For a match to be considered a match, the distance to nearest neighbor should be less than keypointMatchThreshold*(distance to second nearest neighbor)"""
	objectMatchThreshold = 0.1
	"""For an object to be considered detected, number of matches should be more than objectMatchThreshold*(total no of keypoints on object=noKeypoints[objId])"""

	def run(self, params):
		"""override: Compute the SIFT keypoints, plot them in the image and return it"""
		sift = cv2.SIFT()
		frame = params[0] #format: (frameData, frameId)
		kp, descrs = params[1][0], params[1][1] #sift.detectAndCompute(frame[0], None)

		candidates = {}
		for descr in descrs:
			descr = np.array([descr])
			ret, results, neighbours, dist = classifier.find_nearest(descr, 2)

			if dist[0][0] < self.keypointMatchThreshold*dist[0][1]: #good match
				n = int(neighbours[0][0])
				if n in candidates:
					candidates[n] += 1#np.exp(-d/100.0)
				else:
					candidates[n] = 1#np.exp(-d/100.0)

		global noKeypoints
		detected = []
		for c in candidates:
			if candidates[c] > self.objectMatchThreshold*noKeypoints[c]:
				detected += [(labels[c], candidates[c])]

		return detected#labels[detected]