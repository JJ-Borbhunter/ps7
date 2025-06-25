# Copyright 2025 James Bord

import sys;
import re;
import datetime;
import tempfile;

from typing import List;

import Events;
from Service import Service;
from Server import Server;

def main():
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} <log filename>");
		return;

	# Filename from command line
	filenameRegex = re.compile(r"([^\\\/]+)$");
	FILENAME = re.search(filenameRegex, sys.argv[1]).group(1);
	print("Parsing " + FILENAME + " into " + FILENAME + ".rpt");

	# Tempfile so we can copy it into the final report after the boot record has been written
	reportTemp = tempfile.TemporaryFile("w+");
	report = open(sys.argv[1] + ".rpt", "w");

	# has to be the actual original file lol
	log = open(sys.argv[1], "r");

	# Static class variables so that servers and services can log themselves properly
	Server.setFilename(FILENAME);
	Service.setFilename(FILENAME);

	# Object representing previous happenings
	# None exception included for first happening. 
	currentServer: Server | None = None;
	eventdata: Events.EventData | None = None;

	# counter ints for boot log
	TotalServersStarted = 0;
	TotalServersTerminated = 0;


	for linenum, line in enumerate(log, start = 1):
		# Some event driven logic. 
		event, eventdata = Events.parseLine(line, linenum, bool(currentServer));
	
		if event == Events.SERVER_START:
			# Ouput previous server and all services
			if currentServer:
				currentServer.output(reportTemp);
				del currentServer;
				currentServer = None;
			# New Server
			currentServer = Server(eventdata.getLinenum(), eventdata.getDate(), eventdata.getTime());

			# Count servers started
			TotalServersStarted += 1;

		if event == Events.SERVER_TERMINATE:
			# Finish server, ouput with all services. 
			currentServer.terminate(eventdata.getLinenum(), eventdata.getDate(), eventdata.getTime());
			currentServer.output(reportTemp);
			del currentServer;
			currentServer = None;

			# count terminations
			TotalServersTerminated += 1;

		if event == Events.SERVICE_START:
			# new service
			currentServer.addService(Service(eventdata.getName(), eventdata.getLinenum()));

		if event == Events.SERVICE_TERMINATE:
			# terminate service and append to server's services
			currentServer.terminateService(eventdata.getName(), eventdata.getLinenum(), int(eventdata.getTime()));


	# Prefix to report
	report.write("Device Boot Report\n\n");
	report.write(f"InTouch log file: {FILENAME}\n");
	report.write(f"Lines Scanned: {linenum}\n\n");
	report.write(
		f"Device boot count: initiated = {TotalServersStarted}, " \
		f"completed: {TotalServersTerminated}\n\n\n");

	# Copy from tempfile
	reportTemp.seek(0);
	for line in reportTemp:
		report.write(line);

	reportTemp.close();
	report.close();
	log.close();
	print("Complete.");
# main



if __name__ == '__main__':
	main();
