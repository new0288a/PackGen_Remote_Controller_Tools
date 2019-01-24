import ngco_packetgen
import time

#---------------- Example -------------------

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

pg = ngco_packetgen.create_ngco_packetgen(info_list[0])

pg.set_if0_rate(70)
pg.set_if1_rate(50)
time.sleep(1)
pg.start_running()
time.sleep(20)
pg.stop_running()
pg.quit_running()

              
