import os
import commands
import re
import random

ul_pcap_sIP={'dp2':'11.1.4.121', 'dp3':'11.1.4.131', 'dp4':'11.1.4.141', 'dp5':'11.1.4.151', 'dp6':'11.1.4.161'}
ul_pcap_dIP={'dp2':'11.1.4.32', 'dp3':'11.1.4.33', 'dp4':'11.1.4.34', 'dp5':'11.1.4.35', 'dp6':'11.1.4.36'}

dl_pcap_sIP={'dp2':'192.168.96.22', 'dp3':'192.168.96.23', 'dp4':'192.168.96.24', 'dp5':'192.168.96.25', 'dp6':'192.168.96.21'}
dl_pcap_dIP={'dp2':'172.12.0.1', 'dp3':'172.13.0.1', 'dp4':'172.14.0.1', 'dp5':'172.15.0.1', 'dp6':'172.11.0.1'}


def create_rewrite_pcap_filename(direction='dl', dp='dp2'):
	return direction + '-' + dp + '-rewrite-' + str(random.randint(1,100000)) + '.pcap'

def create_split_pcap_filename(direction='dl', dp='dp2', sub_start=1, sub_end=1000):
	return direction + '-' + dp + '-split-' + str(sub_start) + '-' + str(sub_end) + '-' + str(random.randint(1,100000)) + '.pcap'


def create_ul_tcprewrite_command(ul_size='128', dp='dp2', eif0_IP='11.1.4.121', S1U_IP='11.1.4.32', eif0_mac="3C:FD:FE:A8:5F:8C", \
				S1U_mac="3C:FD:FE:BE:85:3C", output_file_path="/tmp/ul_output.pcap", **kwargs):
	size = ul_size
	input_file_path = "./pcap/10k-" + size + "-" + dp + ".eif0.pcap"
	return "tcprewrite -C --enet-smac=" + eif0_mac + " --enet-dmac=" + \
		S1U_mac + " --infile=" + input_file_path + " --outfile=" + \
		output_file_path + " --pnat=" + ul_pcap_sIP[dp] + ":" + \
		eif0_IP + "," + ul_pcap_dIP[dp] + ":" + S1U_IP


def create_dl_tcprewrite_command(dl_size='220', dp='dp2', eif1_IP='192.168.96.22', SGI_IP='172.12.0.1', eif1_mac="3C:FD:FE:A8:5F:8D", \
				SGI_mac="3C:FD:FE:BE:85:3D", output_file_path="/tmp/dl_output.pcap", **kwargs):
	size = dl_size
	input_file_path = "./pcap/10k-" + size + "-" + dp + ".eif1.pcap"
	return "tcprewrite -C --enet-smac=" + eif1_mac + " --enet-dmac=" + \
		SGI_mac + " --infile=" + input_file_path + " --outfile=" + \
		output_file_path + " --pnat=" + dl_pcap_sIP[dp] + ":" + \
		eif1_IP + "," + dl_pcap_dIP[dp] + ":" + SGI_IP


def create_editcap_command(sub_start=1, sub_end=1000, input_file_path="/tmp/input.pcap", output_file_path="/tmp/output.pcap"):
	return "editcap -F libpcap -r " + input_file_path + " " + output_file_path + " " + str(sub_start) + "-" + str(sub_end)




#output_file_path = "/tmp/" + create_rewrite_pcap_filename(direction='ul', dp='dp2')
#print(create_ul_tcprewrite_command(output_file_path=output_file_path))	

#output_file_path = "/tmp/" + create_rewrite_pcap_filename(direction='dl', dp='dp2')
#print(create_dl_tcprewrite_command(output_file_path=output_file_path))

#input_file_path = output_file_path
#output_file_path = "/tmp/" + create_split_pcap_filename(direction='dl', dp='dp2')
#print(create_editcap_command(input_file_path=input_file_path, output_file_path=output_file_path))

	
