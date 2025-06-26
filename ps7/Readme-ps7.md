# PS7: Kronos Log Parsing

## Contact
Name:             James Bord
Section:          P CE2 011
Time to Complete: ~6 hours


## Description
PS7 reads through the boot log of a Khronos InTouch time clock and picks out the salient events. It then catalogs those events in a custom report. 

### Features
This python implementation of PS7 is built off an "event based" model. The log file is parsed by line using the classic python `for line in file` approach. Each line is passed into Event.parseLine along with it's line number and a boolean that indicates whether there is an active server. This function then checks the line against multiple regexes and if it matches one returns the appropriate event code, either SERVER_START, SERVER_TERMINATE, SERVICE_START, or SERVICE_TERMINATE. If the line fits into one of these events an Events.EventData object is created with the salient line number, name and time data for the event to be used by main. If it doesn't match any of these event types an invalid event code is returned and ignored by main.

### Approach
On a SERVER_START event a new object of type Server.Server is created, and the previous server is ouputted to the log file. 

On a SERVER_TERMINATE event the `terminate` method of the current Server.Server object is called. This method will flag the server as successfully booted and set it's boot time length. 

Every Server object has a list of services it starts on boot. On a SERVICE_START event the name of the service is extracted from the current EventData and the service within the server with that name is flagged as having been started. 

on a SERVICE_TERMINATE event the service within the current server of the appropriate name is flagged as having sucessfully terminated. 

Whenever a server outputs itself to a file, either when a new server starts or at the end of the file it goes through it's list of services and outputs each one. These are always the same 24 services. If any service hasn't been completed it will be output as such, but also added to a list of incomplete services at the end of the server's service log. 

### Regex
The first regex seen is a short one of simple use. `([^\\\/]+)$` is passed to re.search and captures all the characters from the back of the string up until the first slash or backslash from the back. This allows the filename to be taken from the filepath of the log file so that the filename can be used in the report cleanly. Both slash and backslash are allowed as delimiters so that both UNIX and DOS filepaths will function as expected. 

The other 4 regular expresions used are in the Events.parseLine function. 

`([\d|-]+) ([\d|:]+): \(log\.c\.166\) server started` is the regex that generates a SERVER_START event if it is matched to. It captures the date as a string by taking all the digits and dashes at the start of the line up to the first space, then it takes the time by taking the next group of characters comprising of digits and colons. After a colon and a space it reads over the characters `(log.c.166)` to the words server started. If a line matches this pattern it is the start of a server. 

`([\d|-]+) ([\d|:]+).*oejs\.AbstractConnector:Started SelectChannelConnector.*` is the regex used to generate a SERVER_TERMINATE event. It caputres the date and time much like the previous regex, but searches specifically for the string `oejs.AbstractConnector:Started SelectChannelConnector`, which only appears in servers that boot sucessfully. .* is used to ignore all characters between the time and the specific string in question and all the characters after, as the string is very specific and there's no risk of it appearing anywhere else in the log. 

`Starting Service\.\s+(\S+)\s+` is used to instantiate a SERVICE_START event and to caputure the service name. All services start in the log with the string `Starting Service.`. The regex then skips over whitespace characters and caputres the first group of non-whitespace characters and uses that as the service name. 

`Service started successfully\.\s+(\S+)\s+[\d|\.]+\s+\((\d+)` instantiates a SERVICE_TERMINATE event and caputres the name and time delay. `Service started successfully.` is the string all lines indicating the completion of a boot service begin with. `\s+(\S+)\s+` skips whitespace and captures the first none whitespace character group, which will again be the process name. It then skips another group of 1 or more whitespace. `[\d|\.]+\s+\(` skips over a digit with decimal points (usually 1.0 in the log) and then a group of whitespace and an open parenthesis. `(\d+)` then captures the millisecond time delay in the service boot. 

### Issues
The provided example reports have one service for which the data is always wrong and a copy of another specific service's data. This was rather confusing albiet surpassable. 

### Extra Credit
To ouput the boot header the entire report was output to a read/write tempfile. The actual report file had the header complete with number of boots and number of lines parsed written to it and then the tempfile was rewound and copied (line by line for safety) into the actual report. 

The services were handled as a list of Service.Service objects within each instance of the Server.Server class. The rest of the logic for handling the services is detailed above. 

## Acknowledgements
https://regex101.com/ used to test and refactor RegEx expressions.