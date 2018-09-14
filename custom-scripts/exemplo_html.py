import SimpleHTTPServer
import SocketServer
import os.path, sys
import datetime
import os, platform, subprocess, re
import psutil


#Handle de http requests.
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	#Build the html file for every connection.
	def makeindex(self):
		
		s0 = "<!DOCTYPE html>  \
			<html> \
			<body> \
			<h1>DADOS DO SISTEMA</h1> "
				
		s_fim = "</body> \
			</html>"


		#Data e Hora

		now = datetime.datetime.now()
		s1 = "<h3>DATA E HORA</h3>"
		s2 = "<p>" + now.strftime("\n%Y-%m-%d %H:%M:%S") + "</p>"


		#Uptime

		def uptime():
 
			try:
				f = open( "/proc/uptime" )
				contents = f.read().split()
				f.close()
			except:
				return "Cannot open uptime file: /proc/uptime"
 
			total_seconds = float(contents[0])
 
			# Helper vars:
			MINUTE  = 60
    
 
    
			seconds = int( total_seconds % MINUTE )
			sec = int( total_seconds)
		
			string = str(sec) + " " + (seconds == 1 and "segundo" or "segundos" )
 
			return string;
     
 
		s3 = "<h3>UPTIME DO SISTEMA</h3>"

		s4 = "<p>" + uptime() + "</p>"

		#Modelo do Processador e Velocidade

		def get_processor_name():
			if platform.system() == "Windows":
				return platform.processor()
			elif platform.system() == "Darwin":
				os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
				command ="sysctl -n machdep.cpu.brand_string"
				return subprocess.check_output(command).strip()
			elif platform.system() == "Linux":
				command = "cat /proc/cpuinfo"
				all_info = subprocess.check_output(command, shell=True).strip()
				for line in all_info.split("\n"):
					if "model name" in line:
						return re.sub( ".*model name.*:", "", line,1)
			return ""

		s5 = "<h3>MODELO DO PROCESSADOR E VELOCIDADE</h3>"
		s6 = (get_processor_name())

		#Capacidade usada do processador

		string2 = str(psutil.cpu_percent()) + "%"

		s7 = "<h3>CAPACIDADE USADA DO PROCESSADOR</h3>"
		s8 = "<p>" + string2 + "</p>"


		#Quantidade de memoria RAM total e usada (MB)

		def getRAMinfo():
			
			p = os.popen('free')
			i = 0
			while 1:
				i = i + 1
				line = p.readline()
        
				if i==2:
					mem = "<p>TOTAL: " + (line.split()[1]) + " bytes</p>" + "<p>USADA: " + (line.split()[2]) + " bytes</p>"
					return mem
				
		s9 = "<h3>MEMORIA RAM</h3>"
		s10 = getRAMinfo()

		#Versao do sistema

		s11 = "<h3>VERSAO DO SISTEMA</h3>"
		s12 = "<p>" + (platform.platform()) + "</p>"

		#Lista de processos em execucao

		pids = psutil.pids()

		s122 = "<h3>LISTA DE PROCESSOS EM EXECUCAO</h3>"

		s13 = "<table> \
		<table border=1>\
			<thead>\
			<tr>\
			<th>PID</th> \
			<th>Nome do Processo</th> \
			</tr> \
		</thead>"

		s14 = "<td>  </td> "
		for pid in pids:
			process = psutil.Process(pid)
			s14 = s14 + " <tr> <td> %d </td> <td> %s </td> </tr>" % (pid, process.name())  
  
		final = s0 + s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 + s10 + s11 + s12 + s122 + s13 + s14
  
		f = open("index.html", "w")
		f.write(final)
		f.close()
		return
	
	#Method http GET.	
	def do_GET(self):
		self.makeindex()
		self.path = '/index.html'
		return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

#Start the webserver.
Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)
server.serve_forever()
