from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
import argparse

class CustomTopology(Topo):
    def build(self):
        # creating the network topology
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(s1, s2)

        topos = {'MyTopo':(lambda:CustomTopology())}

def run_custom_topology():
    parser = argparse.ArgumentParser(description='Mininet')
    parser.add_argument('--config',type=str)
    parser.add_argument('--congestion_scheme',type=str)
    parser.add_argument('--link_loss',type=str)
    args=parser.parse_args()
    MyTopo = CustomTopology()
    net = Mininet(topo=MyTopo)
    s1 = net.get('s1')
    s2 = net.get('s2')
    link = net.linksBetween(s1, s2)[0]
    net.delLink(link)
    net.addLink(s1,s2,loss=args.link_loss)
    net.start()

    
    if (args.config=='a'):
        server_process = net['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt",shell=True)
        client_process = net['h1'].popen(f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 >h1_client.txt",shell=True)
        client_process.wait()

    elif (args.config=='b'):
        server_process = net['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt",shell=True)
        # we can also use this line if we want to take the congestion scheme from command line.
        # client_process = net['h1'].popen(f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -z {args.congestion_scheme} > h1_client_{args.congestion_scheme}.txt",shell=True)
        for scheme in ['vego','reno','cubic','bbr']:
            client_process = net['h1'].popen(f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -z {scheme} > h1_client_{scheme}.txt",shell=True)
        client_process.wait()

    elif (args.config=='c'):
        for h in ['h1','h2','h3']:
            server_process = net['h4'].popen(f"iperf -s -t 5 -i 0.5 -p 3000 > server_file_output.txt",shell=True)
            for scheme in ['vego','reno','cubic','bbr']: 
                client_process = net[h].popen(f"iperf -c 10.0.0.4 -t 5 -i 0.5 -p 3000 -z {scheme} > {h}_client_{scheme}.txt",shell=True)
            client_process.wait()
            server_process.wait()
    dumpNodeConnections(net.hosts)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run_custom_topology()
