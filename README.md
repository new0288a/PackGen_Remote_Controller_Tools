Introduction
===========================
This is DPDK PacketGen remote control tools. It's made with Python. You can program your own code with this tools to control your DPDK PacketGen startup, stop, set rate or quit the PacketGen program remotely.

There is a enhanced tools for EPC testing. It will modify pcap file which locate at /pcap directory according to the input information and send it to PacketGen host for EPC performance testing.



## Requirement
#### DPDK PacketGen host
- Target Hosts OS: Ubuntu
- Ansible host public key have to be inserted into /root/.ssh/known_hosts 
- Host can be access by root with SSH
- PacketGen configuration file should be ready for run
- PacketGen configuration file should be configured with just only using two port for packet transfer and receive.

#### Ansible Host
install below software
- socat
- ansible
- python
- wireshark-common(ubuntu)/wireshark(Centos)
- tcpreplay


## packetgen Library
### packetgen - Basic PacketGen control tools
___Source Code: ./packetgen.py___<br>
The packetgen module define a packetgen object to simply control Packetgen software on remote host.

### packetgen class
```
class packetgen(self, ip="127.0.0.1", home_directory="/root/packetgen", env_file="~/.profile", config_file="my_default", if0_pcap='pcap/large.pcap', if1_pcap='pcap/large.pcap')
```

Construct a new packetgen object, to startup the remote **"ip"** PacketGen software with  **"config_file"** located at **"home_directory" /pktgen-dpdk/cfg"**. And using **"if0_pcap"** and **"if1_pcap"** pcap file as the source by modifing **"config_file"**. Before PacketGen instance startup, Command "source **env_file**" should be run first<br>

packetgen class provide the following method:

> **start.running()**<br>
start transfer packet from both if0 and if1<br>

> **stop.running()**<br>
stop transfer packet from both if0 and if1<br>

> **set_if0_rate(rate)**<br>
set the if0 transfer rate to "rate"<br>

> **set_if1_rate(rate)**<br>
set the if1 transfer rate to "rate"<br>

> **quit_running()**<br>
kill the packetgen software<br>

> **send_lua("file_location")**<br>
send user define lua to packetgen<br>

> **show_file("file")**<br>
show file content from remote packetgen<br>

#### Example
Here is a example of using packetgen class to startup packetgen, control packet transfer and quit the packetgen program. 
```
import time
import packetgen

pg = packetgen.packetgen(ip="10.5.95.76", config_file="my_default", if0_pcap="/tmp/pcap/dp3-dl-1-64.pcap", if1_pcap="/tmp/pcap/dp3-ul-1-64.pcap")

pg.set_if1_rate(0.2)
pg.start_running()
time.sleep(10)
pg.stop_running()
time.sleep(5)
pg.quit_running()
```
## ngco_packetgen Library
### ngco_packetgen - PacketGen control tools for EPC performance testing
___Source Code: ./ngco_packetgen.py___<br>
The ngco_packetgen module define a function to create a packetgen object with modified pcap file **(source file locate at ./pcap)** for EPC performance testing

### create_ngco_packetgen function
```
def create_ngco_packetgen(info)
```

It will return a packetgen object. Before retrun, specified pcap file which come from ./pcap will be modified to meet the EPC testing environment and then be sent to packetgen host. Two line with pcap location in specified **"config_file"** on packetgen host will be replaced by the modified pcap location<br>

The input attribute **"info"** is a object of **dict** constructed of three main parts

***packet_info***<br>
**type:** dict<br>
It is contained the information of selected pcap file
> **dp:** specify which data plane pcap file will be used<br>

> **dl_size:** specify which size pcap file on downlink will be used<br>

> **ul_size:** specify which size pcap file on uplink will be used<br>

> **sub_start:** specify the start index of range for spliting the pcap file<br>

> **sub_end:** specify the end index of range for spliting the pcap file<br>

***pg_info***<br>
**type:** dict<br>
It is contained the information of packetgen remote host
> **ip:** specify the remote packetgen IP<br>

> **home_directory:** specify the path of packetgen root directory<br>

> **env_file:** specify the path of env file which should be run first before packetgen running. It will look like as below<br>
```

echo 1024 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
echo 1024 > /sys/devices/system/node/node1/hugepages/hugepages-2048kB/nr_hugepages

export RTE_SDK=/root/pkt-test/dpdk
export RTE_TARGET=x86_64-native-linuxapp-gcc
export PKTGEN_DIR=/root/pkt-test/pktgen-dpdk

TZ='Asia/Taipei'; export TZ


```
> **config_file:** specify the packetgen configuration file name without .cfg. Which locate at **{{ home_directory }}/pktgen-dpdk/cfg**. It should be configured properly first.<br>

> **eif0_IP:** specify source IP of packet in uplink pcap file<br>

> **eif1_IP:** specify source IP of packet in downlink pcap file<br>

> **eif0_mac:** specify source MAC address of packet in uplink pcap file<br>

> **eif1_mac:** specify source MAC address of packet in uplink pcap file<br>

***dp_info***<br>
**type:** dict<br>
It is contained the information of EPC data-plane host
> **S1U_IP:** specify the distination IP of packet in uplink pcap file<br>

> **SGI_IP:** specify the distination IP of packet in downlink pcap file<br>

> **S1U_mac:** specify the distination MAC address of packet in uplink pcap file<br>

> **SGI_IP:** specify the distination MAC address of packet in downlink pcap file<br>

#### Example
Here is a example of using ngco_packetgen function to create packetgen object, and then startup packetgen, control packet transfer and quit the packetgen program.
```
import time
import ngco_packetgen

info_list = []

#packet_info specify information of pcap file which locate at ./pcap. It will be pushed to PacketGen host after splited.
#sub_start and sub_end specify the range of packet(One subscriber corresponds to one packet) which will be get from the specified pcap file.
packet_info = {'dp':'dp2', 'dl_size':'220', 'ul_size':'128', 'sub_start':1, 'sub_end':1000}

#pg_info specify the net port and configuration information of packetgen
#config_file is the packetgen configuration file name without .cfg. Which locate at /root/{{ home_directory }}/pktgen-dpdk/cfg. It should be configured properly first.
pg_info = {'ip':"10.5.94.251", 'port':'22022', 'home_directory':"/root/pkt-test", 'env_file':'~/.profile','config_file':"ngco-rack3-5dp-1280dp2", \
                'eif0_IP':'11.1.4.121', 'eif0_mac':"3C:FD:FE:A8:5F:8C", \
                'eif1_IP':'192.168.96.22', 'eif1_mac':"3C:FD:FE:A8:5F:8D"}

#dp_info specify the net port information of data plane host
dp_info = {'S1U_IP':'11.1.4.32', 'S1U_mac':"3C:FD:FE:BE:85:3C", 'SGI_IP':'172.12.0.1', 'SGI_mac':"3C:FD:FE:BE:85:3D"}

info_list.append({'pg_info':pg_info, 'dp_info':dp_info, 'packet_info':packet_info})



dp2 = ngco_packetgen.create_ngco_packetgen(info_list[0])
dp2.set_if0_rate(70)
dp2.set_if1_rate(50)
time.sleep(1)
dp2.start_running()
dp2.send_lua("./test.lua")
time.sleep(20)
dp2.stop_running()
dp2.quit_running()
dp2.show_file('/tmp/test.txt')

```





