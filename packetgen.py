import re		
import commands
import json
import time


class packetgen(object):
	lua_config_1 = """echo -e 'package.path = package.path ..";?.lua;test/?.lua;app/?.lua;../?.lua"\nrequire "Pktgen";\nfunction main()\n        """
	lua_config_2 = """\nend\nmain();\n' | socat - TCP4:"""

	def __init__(self, ip="127.0.0.1", home_directory="/root/packetgen", config_file="my_default", if0_pcap='pcap/large.pcap', if1_pcap='pcap/large.pcap'):
		self.ip = ip
		#print("if0_pcap = " + if0_pcap)
		#print("if1_pcap = " + if1_pcap)
		inventory = '[local_host:vars]\nansible_connection=ssh\nansible_user=root\nansible_ssh_pass=P@ssw0rd\n\n[local_host]\n' + ip
		returncode, output = commands.getstatusoutput('echo -e ' + '"' + inventory + '" > inventory')
		returncode, output = commands.getstatusoutput('ansible-playbook init_packetgen.yml --extra-vars "default_file=' + config_file + ' if0_pcap=' + if0_pcap + ' if1_pcap=' + if1_pcap + ' myhome=' + home_directory  + '"')
		#print(output)
		if returncode != 0:
			raise Exception("Something Error on Ansible Playbook Process")

		time.sleep(7)

	def start_running(self):
		#start_lua_config = self.lua_config_1 + 'pktgen.start("0"..",".."1");' + self.lua_config_2 + self.ip + ":" + "22022"
		print("Start PacketGen {ip}".format(ip = self.ip))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.start("0"..",".."1");' + self.lua_config_2 + self.ip + ":" + "22022")
		
	def stop_running(self):
		#stop_lua_config = self.lua_config_1 + 'pktgen.stop("0"..",".."1");' + self.lua_config_2 + self.ip + ":" + "22022"
		print("Stop PacketGen {ip}".format(ip = self.ip))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.stop("0"..",".."1");' + self.lua_config_2 + self.ip + ":" + "22022")

	def set_if0_rate(self, rate=0.1):
		#set_lua_config = self.lua_config_1 + 'pktgen.set("0", "rate", "' + str(rate) + '");' + self.lua_config_2 + self.ip + ":" + "22022"
		print("Set if0 rate to {rate} on PacketGen {ip}".format(ip = self.ip, rate = rate))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.set("0", "rate", "' + str(rate) + '");' + self.lua_config_2 + self.ip + ":" + "22022")

	def set_if1_rate(self, rate=0.1):
		#set_lua_config = self.lua_config_1 + 'pktgen.set("0", "rate", "' + str(rate) + '");' + self.lua_config_2 + self.ip + ":" + "22022"
		print("Set if1 rate to {rate} on PacketGen {ip}".format(ip = self.ip, rate = rate))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.set("1", "rate", "' + str(rate) + '");' + self.lua_config_2 + self.ip + ":" + "22022")

	def quit_running(self):
		print("Quit PacketGen {ip}".format(ip = self.ip))
		returncode, output = commands.getstatusoutput(self.lua_config_1 + 'pktgen.quit();' + self.lua_config_2 + self.ip + ":" + "22022")





