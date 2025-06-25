# Copyright 2025 James Bord

class Service(object):
	"""Represents the necesary data to output a service"""
	def __init__(self, name: str, startline: int):
		super(Service, self).__init__()
		self.name = name;
		self.elapsedtime = -1;
		self.startline = startline;

	def terminate(self, endline: int, elapsedtime: int):
		self.endline = endline;
		self.elapsedtime = elapsedtime;

	programName = "";
	@classmethod
	def setFilename(self, name: str):
		Service.programName = name;

	def __str__(self):
		if self.elapsedtime != -1:
			return f"\t{self.name}\n" + \
				f"\t\t Start: {self.startline}({Service.programName})\n" + \
				f"\t\t Completed: {self.endline}({Service.programName})\n" + \
				f"\t\t Elapsed Time: {self.elapsedtime} ms\n";
		else:
			return f"\t{self.name}\n" + \
				f"\t\t Start: {self.startline}({Service.programName})\n" + \
				"\t\t Completed: Not Completed\n" + \
				"\t\t Elapsed Time:\n";

	def output(self, file):
		file.write(self.__str__());

	def isTerminated(self):
		return self.elapsedtime != -1;
