from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel


def run_topology():
    """
    Simple SDN topology:
    3 hosts + 1 switch + POX controller
    """

    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    print("*** Adding Controller")
    c0 = net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633
    )

    print("*** Adding Hosts")
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')

    print("*** Adding Switch")
    s1 = net.addSwitch('s1', protocols='OpenFlow10')

    print("*** Creating Links")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    print("*** Starting Network")
    net.start()

    print("\n*** Network Ready ***")
    print("Hosts available: h1, h2, h3")
    print("Try commands like:")
    print("  h1 ping h2")
    print("  h1 python3 -m http.server 80")
    print("  h2 curl 10.0.0.1")
    print("  exit\n")

    CLI(net)

    print("*** Stopping Network")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run_topology()
