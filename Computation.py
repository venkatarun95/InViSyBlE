import Permission
import ErrorReporting

class Computation:
	dependancies = []
	def __call__(self, params, permissionHandle):
		if Permission.requestRunPermission(permissionHandle):
			return self.run(params)
		else:
			return None

	def run(params):
		ErrorReporting.reportProgramError("The abstract class should not be run")
		return None #should never reach here because of error reporter