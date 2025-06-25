# Copyright 2025 James Bord

class Service(object):
	"""Represents the necesary data to output a service"""
	def __init__(self, name: str, startline: int):
		super(Service, self).__init__()
		self._name = name;
		self._elapsedtime = -1;
		self._startline = startline;

	def terminate(self, endline: int, elapsedtime: int):
		self._endline = endline;
		self._elapsedtime = elapsedtime;

	programName = "";
	@classmethod
	def setFilename(self, name: str):
		Service.programName = name;

	def __str__(self):
		if self._elapsedtime != -1:
			return f"\t{self._name}\n" + \
				f"\t\t Start: {self._startline}({Service.programName})\n" + \
				f"\t\t Completed: {self._endline}({Service.programName})\n" + \
				f"\t\t Elapsed Time: {self._elapsedtime} ms\n";
		else:
			return f"\t{self._name}\n" + \
				f"\t\t Start: {self._startline}({Service.programName})\n" + \
				"\t\t Completed: Not Completed\n" + \
				"\t\t Elapsed Time:\n";

	def output(self, file):
		file.write(self.__str__());

	def isTerminated(self):
		return self._elapsedtime != -1;

	def getName(self): return self._name;
