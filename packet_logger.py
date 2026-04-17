from pox.core import core
import pox.openflow.libopenflow_01 as of
from datetime import datetime

log = core.getLogger()

class PacketLogger(object):

    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}
        self.packet_count = 0

        self.log_file = "/home/aaron/Desktop/packet_logger_sdn/packet_logs.txt"

        with open(self.log_file, "w") as f:
            f.write("===== SDN PACKET LOGGER =====\n\n")

        connection.addListeners(self)

    def write_log(self, text):
        with open(self.log_file, "a") as f:
            f.write(text + "\n")

    def _handle_PacketIn(self, event):

        packet = event.parsed
        if not packet.parsed:
            return

        self.packet_count += 1

        src_mac = str(packet.src)
        dst_mac = str(packet.dst)
        in_port = event.port

        protocol = "OTHER"

        if packet.find('arp'):
            protocol = "ARP"
        elif packet.find('icmp'):
            protocol = "ICMP"
        elif packet.find('tcp'):
            protocol = "TCP"
        elif packet.find('udp'):
            protocol = "UDP"

        ip_pkt = packet.find('ipv4')

        if ip_pkt:
            src_ip = str(ip_pkt.srcip)
            dst_ip = str(ip_pkt.dstip)

            if src_ip == "10.0.0.3" and dst_ip == "10.0.0.1":
                log.info("BLOCKED: h3 → h1")

                drop_msg = of.ofp_flow_mod()
                drop_msg.priority = 100
                drop_msg.match.dl_type = 0x0800
                drop_msg.match.nw_src = ip_pkt.srcip
                drop_msg.match.nw_dst = ip_pkt.dstip
                event.connection.send(drop_msg)

                return

        self.mac_to_port[src_mac] = in_port

        if dst_mac in self.mac_to_port:
            out_port = self.mac_to_port[dst_mac]
        else:
            out_port = of.OFPP_FLOOD

        log_text = f"""
Packet #{self.packet_count}
Time: {datetime.now()}
Protocol: {protocol}
Source MAC: {src_mac}
Destination MAC: {dst_mac}
"""

        print(log_text)
        self.write_log(log_text)

        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(msg)

def launch():
    def start_switch(event):
        PacketLogger(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
