# Copyright 2025 James Bord

import re;


SERVER_START = 0;
SERVER_TERMINATE = 1;
SERVICE_START = 2;
SERVICE_TERMINATE = 3;

class EventData:
    def __init__(self, linenum = 0, date: str = "", time: str = "", name: str = ""):
        self._linenum = linenum;
        self._time = time;
        self._date = date;
        self._name = name;

    def getDate(self): return self._date;
    def getTime(self): return self._time;
    def getLinenum(self): return self._linenum;
    def getName(self): return self._name;


def parseLine(line: str, linenum: int, isServer: bool) -> (int, EventData):
    serverStartedRegex = re.compile(r"([\d|-]+) ([\d|:]+): \(log\.c\.166\) server started");
    serverTeminatedRegex = re.compile(r"([\d|-]+) ([\d|:]+).*oejs\.AbstractConnector:Started SelectChannelConnector.*");
    serviceStartRegex = re.compile(r"Starting Service\.\s+(\S+)\s+");
    serviceTerminatedRegex = re.compile(r"Service started successfully\.\s+(\S+)\s+[\d|\.]+\s+\((\d+)");

    match = re.match(serverStartedRegex, line);
    if match:
        return SERVER_START, EventData(linenum, date=match.group(1), time=match.group(2));

    match = re.match(serverTeminatedRegex, line);
    if match:
        return SERVER_TERMINATE, EventData(linenum, date=match.group(1), time=match.group(2));

    if isServer:
        match = re.match(serviceStartRegex, line);
        if match:
            return SERVICE_START, EventData(linenum, name=match.group(1));

        match = re.match(serviceTerminatedRegex, line);
        if match:
            return SERVICE_TERMINATE, EventData(linenum, name=match.group(1), time=match.group(2));

    return (-1, None);
