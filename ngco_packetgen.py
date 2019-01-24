import packetgen
import pcapmodify
import time
import commands

def create_ngco_packetgen(info):
	#packet_info = info['packet_info']
	#pg_info = info['pg_info']
	#dp_info = info['dp_info']

	#output_file_path = "/tmp/" + pcapmodify.create_rewrite_pcap_filename(direction='dl', dp=packet_info['dp'])
	#print(pcapmodify.create_dl_tcprewrite_command(size=packet_info['size'], dp=packet_info['dp'], eif1_IP=pg_info['eif1_IP'], \
	#					SGI_IP=dp_info['SGI_IP'], eif1_mac=pg_info['eif1_mac'], SGI_mac=dp_info['SGI_mac'], \
	#					output_file_path=output_file_path))		

	temp = info['packet_info'].copy()
	temp.update(info['pg_info'])
	temp.update(info['dp_info'])
	dl_tcprewrite_output_file_path = "/tmp/" + pcapmodify.create_rewrite_pcap_filename(direction='dl', dp=info['packet_info']['dp'])
	dl_tcprewrite_command = pcapmodify.create_dl_tcprewrite_command(output_file_path=dl_tcprewrite_output_file_path, **temp)	
	#print(dl_tcprewrite_command)
	
	ul_tcprewrite_output_file_path = "/tmp/" + pcapmodify.create_rewrite_pcap_filename(direction='ul', dp=info['packet_info']['dp'])
	ul_tcprewrite_command = pcapmodify.create_ul_tcprewrite_command(output_file_path=ul_tcprewrite_output_file_path, **temp)		
	#print(ul_tcprewrite_command)

	dl_editcp_output_file_path = "/tmp/" + pcapmodify.create_split_pcap_filename(direction='dl', dp=info['packet_info']['dp'], \
									sub_start=info['packet_info']['sub_start'], \
									sub_end=info['packet_info']['sub_end'])
	dl_editcp_command = pcapmodify.create_editcap_command(sub_start=info['packet_info']['sub_start'], sub_end=info['packet_info']['sub_end'], \
						input_file_path=dl_tcprewrite_output_file_path, output_file_path=dl_editcp_output_file_path)
	#print(dl_editcp_command)

	ul_editcp_output_file_path = "/tmp/" + pcapmodify.create_split_pcap_filename(direction='ul', dp=info['packet_info']['dp'], \
									sub_start=info['packet_info']['sub_start'], \
									sub_end=info['packet_info']['sub_end'])
	ul_editcp_command = pcapmodify.create_editcap_command(sub_start=info['packet_info']['sub_start'], sub_end=info['packet_info']['sub_end'], \
						input_file_path=ul_tcprewrite_output_file_path, output_file_path=ul_editcp_output_file_path)
	#print(ul_editcp_command)

	
	returncode, output = commands.getstatusoutput(dl_tcprewrite_command)
	if returncode != 0:
		raise Exception("downlink tcprewrite command error, ", output)
	returncode, output = commands.getstatusoutput(ul_tcprewrite_command)
	if returncode != 0:
		raise Exception("uplink tcprewrite command error, ", output)
	returncode, output = commands.getstatusoutput(dl_editcp_command)
	if returncode != 0:
		raise Exception("downlink editcp command error, ", output)
	returncode, output = commands.getstatusoutput(ul_editcp_command)
	if returncode != 0:
		raise Exception("uplink editcp command error, ", output)

	#dl_output_file = info['packet_info']['dl_size'] + ".pcap"
	#ul_output_file = info['packet_info']['ul_size'] + ".pcap"
	returncode, output = commands.getstatusoutput("rsync -avh " + dl_editcp_output_file_path  + " root@" + info['pg_info']['ip'] + ":/tmp/")
	if returncode != 0:
		raise Exception("Raise Error when copy file" + dl_editcp_output_file_path + " to " + info['pg_info']['ip'] + ", ", output)

	returncode, output = commands.getstatusoutput("rsync -avh " + ul_editcp_output_file_path  + " root@" + info['pg_info']['ip'] + ":/tmp/")
	if returncode != 0:
		raise Exception("Raise Error when copy file" + ul_editcp_output_file_path + " to " + info['pg_info']['ip'] + ", ", output)


	pg = packetgen.packetgen(ip=info['pg_info']['ip'], config_file=info['pg_info']['config_file'], \
				if0_pcap=ul_editcp_output_file_path, if1_pcap=dl_editcp_output_file_path)
	
	return pg

#---------------- Example -------------------
'''
info_list = []

#packet_info specify information of pcap file which locate at ./pcap. It will be pushed to PacketGen host after splited.
#sub_start and sub_end specify the range of packet(One subscriber corresponds to one packet) which will be get from the specified pcap file.
packet_info = {'dp':'dp2', 'dl_size':'220', 'ul_size':'128', 'sub_start':1, 'sub_end':1000}

#pg_info specify the net port and configuration information of packetgen
#config_file is the packetgen configuration file name without .cfg. Which locate at /root/{{ home_directory }}/pktgen-dpdk/cfg. It should be configured properly first.
pg_info = {'ip':"10.5.95.76", 'home_directory':"/root/packetgen", 'config_file':"my_default", \
		'eif0_IP':'11.1.4.121', 'eif0_mac':"3C:FD:FE:A8:5F:8C", \
		'eif1_IP':'192.168.96.22', 'eif1_mac':"3C:FD:FE:A8:5F:8D"}

#dp_info specify the net port information of data plane host
dp_info = {'S1U_IP':'11.1.4.32', 'S1U_mac':"3C:FD:FE:BE:85:3C", 'SGI_IP':'172.12.0.1', 'SGI_mac':"3C:FD:FE:BE:85:3D"}

info_list.append({'pg_info':pg_info, 'dp_info':dp_info, 'packet_info':packet_info})


hostIP = "10.5.95.76"

pg = create_ngco_packetgen(info_list[0])

pg.set_if0_rate(70)
pg.set_if1_rate(50)
time.sleep(1)
pg.start_running()
time.sleep(20)
pg.stop_running()
pg.quit_running()
'''
