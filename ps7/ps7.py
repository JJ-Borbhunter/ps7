# Copyright 2025 James Bord

import sys;
import re;
import datetime;

import Events;
from Service import Service;
from Server import Server;


def main():
	serviceNameRegex = re.compile(r"Starting Service.  (\w+) [\d|\.]*");
	serviceCompleteRegex = re.compile(r"Service started successfully.  (\w+) [\d|\.]*");

	report = open("report.rpt", "w");
	log = open(sys.argv[1], "r");

	Server.setFilename(sys.argv[1]);

	currentServer: Server | None = None;
	currentService: Service | None = None;
	eventdata: Events.EventData | None = None;

	for linenum, line in enumerate(log, start = 1):
		event, eventdata = Events.parseLine(line, linenum);
	
		if event == Events.SERVER_START:
			if currentServer and not currentServer.terminated:
				currentServer.output(report);
	
			currentServer = Server(eventdata.linenum, eventdata.date, eventdata.time);

		if event == Events.SERVER_TERMINATE:
			currentServer.terminate(eventdata.linenum, eventdata.date, eventdata.time);
			currentServer.output(report);


	print("Complete.");
# main


if __name__ == '__main__':
	main();