Introduction
===========================
This is DPDK PacketGen remote control tools. It's made with Python. You can program your own code with this tools to control your DPDK PacketGen startup, stop, set rate or quit the PacketGen program remotely.--
 --
There is a enhanced tools for EPC testing. It will modify pcap file which locate at /pcap directory according to the input information and send it to PacketGen host for EPC performance testing.


****

## Requirement
###DPDK PacketGen host
- Target Hosts OS: Ubuntu
- Ansible host public key have to be inserted into /root/.ssh/known_hosts 
- Host can be access by root with SSH
- PacketGen configuration file should be ready for run
- PacketGen configuration file should be configured with just only using two port for packet transfer and recive.

###Ansible Host
-scoat
-ansible
-python
-wireshark-common/wireshark
-tcpreplay

## How To Use
