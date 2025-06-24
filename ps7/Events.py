# Copyright 2025 James Bord

import re;


SERVER_START = 0;
SERVER_TERMINATE = 1;
SERVICE_START = 2;
SERVICE_TERMINATE = 3;

class EventData:
    def __init__(self, linenum = 0, date: str = "", time: str = ""):
        self.linenum = linenum;
        self.time = time;
        self.date = date;

    def getDate(self): return self.date;
    def getTime(self): return self.time;
    def getLinenum(self): return self.linenum;

def parseLine(line: str, linenum: int, isServer: bool) -> tuple[int, EventData]:
    serverStartedRegex = re.compile(r"([\d|-]+) ([\d|:]+): \(log\.c\.166\) server started");
    serverTeminatedRegex = re.compile(r"([\d|-]+) ([\d|:]+).*oejs\.AbstractConnector:Started SelectChannelConnector.*");
    serviceStartRegex = re.compile(r"Service started\. ")

    match = re.match(serverStartedRegex, line);
    if match:
        return SERVER_START, EventData(linenum, match.group(1), match.group(2));

    match = re.match(serverTeminatedRegex, line);
    if match:
        return SERVER_TERMINATE, EventData(linenum, match.group(1), match.group(2));

    if isServer:


    return (-1, None);