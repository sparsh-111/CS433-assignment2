import matplotlib.pyplot as plt

# Read data from the file
data_file = 'h1_client_vego.txt'  
with open(data_file, 'r') as file:
    lines = file.readlines()

# Extract time and throughput from each line
time_values = []
throughput_values = []
for line in lines[6:15]:  # Skip the first 6 lines 
    values = line.split()
    val = values[2].split('-')
    time_values.append(float(val[0]))
    throughput_values.append(float(values[6]))
    
# Plot the data
plt.plot(time_values, throughput_values, label='vego_h1_Throughput')
plt.title('Throughput Over Time (iperf)')
plt.xlabel('Time (seconds)')
plt.ylabel('Throughput (Gbits/sec)')
plt.legend()
plt.grid(True)
data_file = 'h1_client_reno.txt'  # Replace with the actual file name
with open(data_file, 'r') as file:
    lines = file.readlines()

time_values = []
throughput_values = []
for line in lines[6:15]:
    values = line.split()
    val = values[2].split('-')
    time_values.append(float(val[0]))
    throughput_values.append(float(values[6]))
    print(time_values,throughput_values)
  
plt.plot(time_values, throughput_values, label='reno_h1_Throughput')
data_file = 'h1_client_cubic.txt' 
with open(data_file, 'r') as file:
    lines = file.readlines()


time_values = []
throughput_values = []
for line in lines[6:15]: 
    values = line.split()
    val = values[2].split('-')
    time_values.append(float(val[0]))
    throughput_values.append(float(values[6]))


plt.plot(time_values, throughput_values, label='cubic_h1_Throughput')
data_file = 'h1_client_bbr.txt'  
with open(data_file, 'r') as file:
    lines = file.readlines()

time_values = []
throughput_values = []
for line in lines[6:15]: 
    values = line.split()
    val = values[2].split('-')
    time_values.append(float(val[0]))
    throughput_values.append(float(values[6]))


plt.plot(time_values, throughput_values, label='bbr_h1_Throughput')
plt.show()
