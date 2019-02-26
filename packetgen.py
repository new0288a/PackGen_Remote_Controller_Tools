import re		
import commands
import json
import time


class packetgen(object):
	#lua_config_1 = """echo -e 'package.path = package.path ..";?.lua;test/?.lua;app/?.lua;../?.lua"\nrequire "Pktgen";\nfunction main()\n        """
	lua_config_1 = """echo 'package.path = package.path ..";?.lua;test/?.lua;app/?.lua;../?.lua"\nrequire "Pktgen";\nfunction main()\n        """
	lua_config_2 = """\nend\nmain();\n' | socat - TCP4:"""

	def __init__(self, ip="127.0.0.1", port="22022", home_directory="/root/packetgen", env_file="../prepare_env.sh", config_file="my_default", if0_pcap='pcap/large.pcap', if1_pcap='pcap/large.pcap', **kwargs):
		self.ip = ip
		self.port = port
		#print("if0_pcap = " + if0_pcap)
		#print("if1_pcap = " + if1_pcap)

		#If packetgen instance is not running, start-up packetgen instance
		returncode, output = commands.getstatusoutput('ssh root@' + ip + ' netstat -tlunap | awk "{print $4}" | grep ' + port)
		if returncode != 0:
			print("packetgen instance({ip}:{port}) is not running, start-up packetgen instance.".format(ip = ip, port = port))
			inventory = '[local_host:vars]\nansible_connection=ssh\nansible_user=root\nansible_ssh_pass=P@ssw0rd\n\n[local_host]\n' + ip
			#returncode, output = commands.getstatusoutput('echo -e ' + '"' + inventory + '" > inventory')
			returncode, output = commands.getstatusoutput('echo ' + '"' + inventory + '" > inventory')
			returncode, output = commands.getstatusoutput('ansible-playbook init_packetgen.yml --extra-vars "default_file=' + config_file + ' if0_pcap=' + if0_pcap + ' if1_pcap=' + if1_pcap + ' myhome=' + home_directory  + ' host_ip=' + ip.replace(".", "_") + ' host_port=' + port  + ' env_file=' + env_file + '"')
			#print(output)
			if returncode != 0:
				print(output)
				raise Exception("Something Error on Ansible Playbook Process")
			time.sleep(7)

	def start_running(self):
		#start_lua_config = self.lua_config_1 + 'pktgen.start("0"..",".."1");' + self.lua_config_2 + self.ip + ":" + "22022"
		print("Start PacketGen {ip}:{port}".format(ip = self.ip, port = self.port))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.start("0"..",".."1");' + self.lua_config_2 + self.ip + ":" + self.port)
		
	def stop_running(self):
		#stop_lua_config = self.lua_config_1 + 'pktgen.stop("0"..",".."1");' + self.lua_config_2 + self.ip + ":" + "22022"
		print("Stop PacketGen {ip}:{port}".format(ip = self.ip, port = self.port))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.stop("0"..",".."1");' + self.lua_config_2 + self.ip + ":" + self.port)

	def set_if0_rate(self, rate=0.1):
		#set_lua_config = self.lua_config_1 + 'pktgen.set("0", "rate", "' + str(rate) + '");' + self.lua_config_2 + self.ip + ":" + "22022"
		print("Set if0 rate to {rate} on PacketGen {ip}:{port}".format(ip = self.ip, rate = rate, port = self.port))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.set("0", "rate", "' + str(rate) + '");' + self.lua_config_2 + self.ip + ":" + self.port)

	def set_if1_rate(self, rate=0.1):
		#set_lua_config = self.lua_config_1 + 'pktgen.set("0", "rate", "' + str(rate) + '");' + self.lua_config_2 + self.ip + ":" + "22022"
		print("Set if1 rate to {rate} on PacketGen {ip}:{port}".format(ip = self.ip, rate = rate, port = self.port))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.set("1", "rate", "' + str(rate) + '");' + self.lua_config_2 + self.ip + ":" + self.port)

	def quit_running(self):
		print("Quit PacketGen {ip}:{port}".format(ip = self.ip, port = self.port))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.quit();' + self.lua_config_2 + self.ip + ":" + self.port)

	def send_lua(self, file_location):
		print("Send user define lua to {ip}:{port}: ".format(ip = self.ip, port = self.port) + file_location)
		returncode, output = commands.getstatusoutput("cat " + file_location + " | socat - TCP4:" + self.ip + ":" + self.port)

	def show_file(self, file_location):
		print("Show host({ip}) file: ".format(ip = self.ip) + file_location)
		print(commands.getstatusoutput("ssh root@{ip} cat {file}".format(ip = self.ip, file = file_location))[1])

