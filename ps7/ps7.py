# Copyright 2025 James Bord

import sys;
import re;
import datetime;

import Events;
from Service import Service;
from Server import Server;

from typing import List;

def main():
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} <log filename>");
		return;

	report = open(sys.argv[1] + ".rpt", "w");
	log = open(sys.argv[1], "r");

	Server.setFilename(sys.argv[1]);
	Service.setFilename(sys.argv[1]);

	currentServer: Server | None = None;
	currentService: Service | None = None;
	eventdata: Events.EventData | None = None;

	currentServersServices: List[Service] = [];  # needed to store a servers services

	for linenum, line in enumerate(log, start = 1):
		# Some event driven logic. 
		event, eventdata = Events.parseLine(
			line, linenum, bool(currentServer) and not currentServer.isTerminated());
	
		if event == Events.SERVER_START:
			# Ouput previous server and all services
			if currentServer and not currentServer.isTerminated():
				currentServer.output(report);
				report.write("Services\n");
				for service in currentServersServices:
					service.output(report);
				report.write("\n");
				currentServersServices = [];

			# New Server
			currentServer = Server(eventdata.getLinenum(), eventdata.getDate(), eventdata.getTime());

		if event == Events.SERVER_TERMINATE:
			# Finish server, ouput with all services. 
			currentServer.terminate(eventdata.linenum, eventdata.date, eventdata.time);
			currentServer.output(report);
			report.write("Services\n");
			for service in currentServersServices:
				service.output(report);
			report.write("\n");
			currentServersServices = [];

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


	print("Complete.");
# main


if __name__ == '__main__':
	main();