# Copyright 2025 James Bord

class Service(object):
	"""Represents the necesary data to output a service"""
	def __init__(self, name: str, starttime: int):
		super(Service, self).__init__()
		self.name = name;
		self.elapsedtime = -1;
		self.starttime = starttime;

	def complete(endtime: int):
		self.endtime = endtime;
		self.elapsedtime = endtime - starttime;

	programName = "";
	@classmethod
	def setProgramName(name):
		Service.programName = name;

	def __str__(self):
		if elapsedtime != -1:
			return "\t" + self.name + "(" + Service.programName + ")" + "\n" + \
				"\t\tCompleted: " + self.endtime + "(" + Service.programName + ")" + "\n" + \
				"\t\tElapsed Time: " + self.elapsedtime + " ms\n";

