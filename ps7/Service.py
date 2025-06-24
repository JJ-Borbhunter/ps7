# Copyright 2025 James Bord

class Service(object):
	"""Represents the necesary data to output a service"""
	def __init__(self, name: str, startline: int):
		super(Service, self).__init__()
		self.name = name;
		self.elapsedtime = -1;
		self.startline = startline;

	def complete(self, endline: int, elapsedtime: int):
		self.endline = endline;
		self.elapsedtime = elapsedtime;

	programName = "";
	@classmethod
	def setProgramName(name):
		Service.programName = name;

	def __str__(self):
		if elapsedtime != -1:
			return "\t" + self.name + "(" + Service.programName + ")" + "\n" + \
				"\t\tCompleted: " + self.endline + "(" + Service.programName + ")" + "\n" + \
				"\t\tElapsed Time: " + self.elapsedtime + " ms\n";
		else:
			return "\t" + self.name + "(" + Service.programName + ")" + "\n" + \
				"\t\tCompleted: Not Completed\n" + \
				"\t\tElapsed Time:\n";
