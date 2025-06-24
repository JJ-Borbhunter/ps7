# Copyright 2025 James Bord

import re;


SERVER_START = 0;
SERVER_TERMINATE = 1;
SERVICE_START = 2;
SERVICE_TERMINATE = 3;

class EventData:
    def __init__(self, linenum = 0, time = 0):
        self.linenum = linenum;
        self.time = time;

def parseLine(line: str, linenum: int) -> tuple[int, EventData]:
    serverStartedRegex = re.compile(r".*\(log\.c\.166\) server started");
    serverTeminatedRegex = re.compile(r".*oejs\.AbstractConnector:Started SelectChannelConnector.*");

    if re.match(serverStartedRegex, line):
        return SERVER_START, EventData(linenum);

    if re.match(serverTeminatedRegex, line):
        return SERVER_TERMINATE, EventData(linenum);

    return (-1, None);