# Copyright 2025 James Bord

class Service(object):
	"""Represents the necesary data to output a service"""
	def __init__(self, name: str):
		super(Service, self).__init__()
		self._name = name;
		self._elapsedtime = -1;
		self._startline = -1;

	def start(self, startline: int):
		self._startline = startline;

	def terminate(self, endline: int, elapsedtime: int):
		self._endline = endline;
		self._elapsedtime = elapsedtime;

	programName = "";
	@classmethod
	def setFilename(self, name: str):
		Service.programName = name;

	def __str__(self):
		returner: str = f"\t{self._name}\n" ;
		if self._startline != -1:
			returner += f"\t\t Start: {self._startline}({Service.programName})\n";
		else:
			returner += f"\t\t Start: Not started({Service.programName})\n";

		if self._elapsedtime != -1:
			returner += f"\t\t Completed: {self._endline}({Service.programName})\n";
			returner += f"\t\t Elapsed Time: {self._elapsedtime} ms\n";
		else:
			returner += f"\t\t Completed: Not completed({Service.programName})\n";
			returner += "\t\t Elapsed Time: \n";
		return returner;

	def output(self, file):
		file.write(self.__str__());

	def isTerminated(self):
		return self._elapsedtime != -1;

	def getName(self): return self._name;
