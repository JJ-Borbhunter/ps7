# Copyright 2025 James Bord

import re;
from datetime import datetime;

class Server:

	filename: str = "";

	def __init__(self, linenum: int, startdate: str, starttime: str):
		self.terminated: bool = False;
		self.linenum = linenum;
		self.startdate = startdate;
		self.starttime = starttime;
		pass;

	def output(self, file):
		file.write("=== Device boot ===\n");
		file.write(
			f"{self.linenum}({Server.filename}): {self.startdate} {self.starttime} Boot Start\n");
	
		if (self.terminated):
			file.write(
				f"{self.endlinenum}({Server.filename}): {self.enddate} {self.endtime} Boot Completed\n");
			file.write(f"\tBoot Time: {self.elapsedtime}ms \n");
		else:
			file.write(f"**** Incomplete boot **** \n");

		file.write("\n");
	
	def terminate(self, linenum: int, enddate: str, endtime: str):
		self.terminated = True;
		self.endlinenum = linenum;
		self.endtime = endtime;
		self.enddate = enddate;

		start = datetime.strptime(self.starttime, "%H:%M:%S");
		end = datetime.strptime(self.endtime, "%H:%M:%S");
		elapsed = end - start;

		self.elapsedtime = int(elapsed.total_seconds() * 1000);

	def isTerminated(self): return self.terminated;

	@classmethod
	def setFilename(self, name: str):
		Server.filename = name;

# Server