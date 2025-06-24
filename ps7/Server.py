
import re;

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
			file.write(f"\tBoot Time: {self.elapsedtime}000ms \n");
		else:
			file.write(f"**** Incomplete boot **** \n");

		file.write("\n");
	
	def terminate(self, linenum: int, enddate: str, endtime: str):
		self.terminated = True;
		self.endlinenum = linenum;
		self.endtime = endtime;
		self.enddate = enddate;

		timeRegex = re.compile(r"(\d)+:(\d)+:(\d+)");
		startMatch = re.match(timeRegex, self.starttime);
		start = 3600 * int(startMatch.group(1)) + \
			60 * int(startMatch.group(2)) + \
			int(startMatch.group(3));
		
		endMatch = re.match(timeRegex, self.endtime);
		end = 3600 * int(endMatch.group(1)) + \
			60 * int(endMatch.group(2)) + \
			int(endMatch.group(3));
		self.elapsedtime = end - start;

	@classmethod
	def setFilename(self, name: str):
		Server.filename = name;

# Server