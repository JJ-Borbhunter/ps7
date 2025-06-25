# Copyright 2025 James Bord

import sys;
import re;
import datetime;
import tempfile;

import Events;
from Service import Service;
from Server import Server;

from typing import List;

def main():
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} <log filename>");
		return;

	# Filename from command line
	FILENAME = sys.argv[1];

	# Tempfile so we can copy it into the final report after the boot record has been written
	reportTemp = tempfile.TemporaryFile("w+");
	report = open(FILENAME + ".rpt", "w");
	log = open(FILENAME, "r");

	# Static class variables so that servers and services can log themselves properly
	Server.setFilename(FILENAME);
	Service.setFilename(FILENAME);

	currentServer: Server | None = None;
	currentService: Service | None = None;
	eventdata: Events.EventData | None = None;

	# counter ints for boot log
	TotalServersStarted = 0;
	TotalServersTerminated = 0;

	currentServersServices: List[Service] = [];  # needed to store a servers services

	for linenum, line in enumerate(log, start = 1):
		# Some event driven logic. 
		event, eventdata = Events.parseLine(
			line, linenum, bool(currentServer) and not currentServer.isTerminated());
	
		if event == Events.SERVER_START:
			# Ouput previous server and all services
			if currentServer and not currentServer.isTerminated():
				currentServer.output(reportTemp);
				reportTemp.write("Services\n");
				for service in currentServersServices:
					service.output(reportTemp);
				reportTemp.write("\n");
				currentServersServices = [];

			# New Server
			currentServer = Server(eventdata.getLinenum(), eventdata.getDate(), eventdata.getTime());

			# Count servers started
			TotalServersStarted += 1;

		if event == Events.SERVER_TERMINATE:
			# Finish server, ouput with all services. 
			currentServer.terminate(eventdata.linenum, eventdata.date, eventdata.time);
			currentServer.output(reportTemp);
			reportTemp.write("Services\n");
			for service in currentServersServices:
				service.output(reportTemp);
			reportTemp.write("\n");
			currentServersServices = [];

			# count terminations
			TotalServersTerminated += 1;

		if event == Events.SERVICE_START:
			# Add failed service if necesary
			if currentService and not currentService.isTerminated():
				currentServersServices.append(currentService);

			# new service
			currentService = Service(eventdata.getName(), eventdata.getLinenum());

		if event == Events.SERVICE_TERMINATE:
			# terminate service and append to server's services
			currentService.terminate(eventdata.getLinenum(), int(eventdata.getTime()));
			currentServersServices.append(currentService);


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

	print("Complete.");
# main


if __name__ == '__main__':
	main();