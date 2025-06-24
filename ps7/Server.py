class Server:

	filename: str = "";

	def __init__(self, linenum: int, starttime: int):
		self.terminated: bool = False;
		self.linenum = linenum;
		self.starttime = starttime;
		pass;

	def output(self, file):
		file.write("=== Device Boot ===\n");
		file.write(f"{self.linenum}({Server.filename}): Boot Start\n");
	
		if (self.terminated):
			file.write(f"{self.endlinenum}({Server.filename}): Boot Completed\n");
		else:
			file.write(f"**** Incomplete boot ****\n");

		file.write("\n");
	
	def terminate(self, linenum: int, endtime: int):
		self.terminated = True;
		self.elapsedtime = endtime - self.starttime;
		self.endlinenum = linenum;

	@classmethod
	def setFilename(self, name: str):
		Server.filename = name;

# Server