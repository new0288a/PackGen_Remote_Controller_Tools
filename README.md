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
- scoat
- ansible
- python
- wireshark-common/wireshark
- tcpreplay


## packetgen Library
### packetgen - Basic PacketGen Control tools
___Source Code: ./packetgen.py___<br>
The packetgen module define a packetgen object to simply control Packetgen software on remote host.

### packetgen class
```
**class** packetgen(self, ip="127.0.0.1", home_directory="/root/packetgen", config_file="my_default", if0_pcap='pcap/large.pcap', if1_pcap='pcap/large.pcap')<br>
```

Construct a new packetgen object, to startup the remote **"ip"** PacketGen software with **"config_file" **located at **"home_directory" /pktgen-dpdk/cfg"**. And using **"if0_pcap" **and **"if1_pcap" **pcap file as the source by modifing **"config_file"**.<br>

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

#### Example
Here is a example of using packetgen class to startup packetgen, control packet transfer and quit the packetgen program. 
```
pg = packetgen(ip="10.5.95.76", config_file="my_default", if0_pcap="/tmp/pcap/dp3-dl-1-64.pcap", if1_pcap="/tmp/pcap/dp3-ul-1-64.pcap")
pg.set_if1_rate(0.2)
pg.start_running()
time.sleep(10)
pg.stop_running()
time.sleep(5)
pg.quit_running()
```





