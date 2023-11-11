from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSController

class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    "A LinuxRouter connecting three IP subnets"

    def build(self, **_opts):
        s1, s2, s3 = [ self.addSwitch( s ) for s in ( 's1', 's2', 's3' ) ]
        subnet1 = '10.0.0.0/24'
        subnet3 = '10.2.0.0/24'
        subnet2 = '10.1.0.0/24'
        ra = self.addNode('ra', cls=LinuxRouter, ip='10.0.0.1/24')
        h1 = self.addHost('h1', ip='10.0.0.100/24', defaultRoute='via 10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.101/24', defaultRoute='via 10.0.0.1')

        rb = self.addNode('rb', cls=LinuxRouter, ip='10.1.0.1/24')
        h3 = self.addHost('h3', ip='10.1.0.100/24', defaultRoute='via 10.1.0.1')
        h4 = self.addHost('h4', ip='10.1.0.101/24', defaultRoute='via 10.1.0.1')

        rc = self.addNode('rc', cls=LinuxRouter, ip='10.2.0.1/24')
        h5 = self.addHost('h5', ip='10.2.0.100/24', defaultRoute='via 10.2.0.1')
        h6 = self.addHost('h6', ip='10.2.0.101/24', defaultRoute='via 10.2.0.1')

        # Adding connections
        self.addLink(s1, ra, intfName2='ra-eth1', params2={'ip': '10.0.0.1/24'})
        self.addLink(s2, rb, intfName2='rb-eth1', params2={'ip': '10.1.0.1/24'})
        self.addLink(s3, rc, intfName2='rc-eth1', params2={'ip': '10.2.0.1/24'})
        self.addLink(ra, rb, intfName1='r1', intfName2='r2', params1={'ip': '10.0.2.1/24'}, params2={'ip': '10.0.2.2/24'})
        self.addLink(rb, rc, intfName1='r3', intfName2='r4', params1={'ip': '10.1.2.1/24'}, params2={'ip': '10.1.2.2/24'})
        self.addLink(ra, rc, intfName1='r5', intfName2='r6', params1={'ip': '10.2.2.1/24'}, params2={'ip': '10.2.2.2/24'})
        for h, s in [ (h1, s1), (h2, s1), (h3, s2),(h4,s2),(h5,s3),(h6,s3) ]:
            self.addLink( h, s )


if __name__ == '__main__':
    setLogLevel('info')
    topo = NetworkTopo()
    net = Mininet(topo=topo, controller=OVSController, waitConnected=True)
    #for changing the path to h1->ra->rb->rc->h6 change the ip route of ra to subnet3 via 10.0.2.2 and ip route of rc to subnet1 via 10.1.2.1

    # Add static routes on ra, rb,and rc
    info(net['ra'].cmd('ip route add 10.1.0.0/24 via 10.0.2.2'))
    info(net['ra'].cmd('ip route add 10.2.0.0/24 via 10.2.2.2'))
    info(net['rb'].cmd('ip route add 10.0.0.0/24 via 10.0.2.1'))
    info(net['rb'].cmd('ip route add 10.2.0.0/24 via 10.1.2.2'))
    info(net['rc'].cmd('ip route add 10.0.0.0/24 via 10.2.2.1'))
    info(net['rc'].cmd('ip route add 10.1.0.0/24 via 10.1.2.1'))
    
 
    net.start()
    info('* Routing Tables:\n')
    for router in ['ra', 'rb', 'rc']:
        info(net[router].cmd('route'))
    CLI(net)
    net.stop()
