# CS433 Assignment-2 

This repository contains the code and documentation for CS433 Assignment-2. The assignment involves implementing a Mininet topology, running iperf clients and servers with different congestion control schemes, and analyzing throughput.

## Files and Directories:

- **Question1.py**: Python script defining the Mininet topology and solution to part1.
- **plotting_file.gp**: Matplotlib script to generate throughput graphs for various configuration(need to change the read data file for different host(default h1))
- **CS433 Assignment-2.pdf**: Report containing the screenshots, results and graphs.

## Instructions:

1. Run the part1 question using `Question1.py` which will create a mininet network topology and solution of part1.
2. Run the part2 question using `Question2.py`.
3. Running part2 in config=a will create a file name 'h1_client.txt' which will contain the data regarding time vs data transfer and bandwidth.
4. Running the part2 in config=b will create 4 file which will contains all four congestion scheme we need to show and contain the data regarding time vs data transfer and bandwidth.
5. Running the part2 in config=c will create 12 file 3hosts and 4 congestion scheme for each of them with the similar data information.
6. we can also set the congestion_scheme and link loss on command line.
7. Congestion_scheme CLI code need to be uncommented from Question2 config=b code. I have used loop to generate all congestion scheme data easily.
8. Example: sudo python3 Question2.py --config=b --congestion_scheme=reno --link_loss=3%

## References:
1. https://github.com/mininet/mininet/blob/master/examples/linuxrouter.py
2. https://iperf.fr/
3. http://mininet.org/walkthrough/
   
