class Scheduler:
	#Priority information goes here
	computationList = {}
	computationResults = {}
	finalComputationList = []#computations whose results are actually required

	def updateComputationList(self, computationList):
		self.computationList = {}
		self.finalComputationList = []
		for c in computationList:
			self.computationList[c] = c()
			self.finalComputationList += [c]

	def compute(self):
		"""Given a list of computations (derived classes of Computation), perform them keeping in mind real time and priority considerations"""
		self.computationResults = {}
		res = []
		for c in self.finalComputationList:
			res += [self.__compute__(c)]
		return res

	def __compute__(self, cType):
		if cType in self.computationResults:
			return self.computationResults[cType]

		if not cType in self.computationList:
			#print cType, self.computationList
			self.computationList[cType] = cType() #if it is not here, add it

		params = []
		for d in self.computationList[cType].dependancies:
			res = self.__compute__(d)
			params += [res]
			if res == None:
				self.computationResults[cType] = None
				return None
		res = self.computationList[cType](params, None)
		self.computationResults[cType] = res
		return res