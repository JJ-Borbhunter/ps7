# Copyright 2025 James Bord

import re;
from datetime import datetime;
from typing import List;

from Service import Service;

class Server:

	filename: str = "";

	def __init__(self, linenum: int, startdate: str, starttime: str):
		self._terminated: bool = False;
		self._linenum = linenum;
		self._startdate = startdate;
		self._starttime = starttime;
		self._services: List[Service] = [];
		pass;

	def output(self, file):
		file.write("=== Device boot ===\n");
		file.write(
			f"{self._linenum}({Server.filename}): {self._startdate} {self._starttime} Boot Start\n");
	
		if (self._terminated):
			file.write(
				f"{self._endlinenum}({Server.filename}): {self._enddate} {self._endtime} Boot Completed\n");
			file.write(f"\tBoot Time: {self._elapsedtime}ms \n");
			print(f"complete boot with   {len(self._services)} services");
		else:
			file.write(f"**** Incomplete boot **** \n");
			print(f"incomplete boot with {len(self._services)} services");

		file.write("\n");

		fails = False;
		if len(self._services) > 0:
			file.write("Services\n");
			for service in self._services:
				service.output(file);
				if not service.isTerminated():
					fails = True;
			file.write("\n");

		if fails:
			file.write("\t*** Services not successfully started: ");
			i = False;
			for service in self._services:
				if i: file.write(", ");
				file.write(service.getName());
				i = True;
			file.write("\n\n");
	
	def terminate(self, linenum: int, enddate: str, endtime: str):
		self._terminated = True;
		self._endlinenum = linenum;
		self._endtime = endtime;
		self._enddate = enddate;

		start = datetime.strptime(self._starttime, "%H:%M:%S");
		end = datetime.strptime(self._endtime, "%H:%M:%S");
		elapsed = end - start;

		self._elapsedtime = int(elapsed.total_seconds() * 1000);

	def isTerminated(self): return self._terminated;

	@classmethod
	def setFilename(self, name: str):
		Server.filename = name;

	def addService(self, s: Service):
		print(f"Append service to {self._terminated}");
		self._services.append(s);

	def terminateService(self, name: str, endline: int, elapsedtime: int):
		if len(self._services) < 1: return;
		service = next((s for s in self._services if s.getName() == name), None);
		if service: service.terminate(endline, elapsedtime);


# Server