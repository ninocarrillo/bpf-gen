import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin

def InitBPF(this):
	this['Taps'] = firwin(
		this['tap count'],
		[ this['low cutoff'], this['high cutoff'] ],
		pass_zero='bandpass',
		fs=this['sample rate']
	)
	return this
	
def GenInt16ArrayC(name, array, column_width):
	result = '\n'
	result += f'const __prog__ int16_t __attribute__((space(prog))) {name}[{len(array)}] = '
	result += '{ '
	y = len(array)
	for x in range(y):
		if x % column_width == 0:
			result += ' \\\n     '
		result += f' {int(np.rint(array[x]))}'
		if x < (y-1):
			result += ','
	result += ' };'
	return result

if len(sys.argv) != 5:
		print("Not enough arguments. Usage: python3 bpf-gen.py <sample rate> <low cutoff> <high cutoff> <tap count>")
		sys.exit(-1)

filter = {}
filter['sample rate'] = float(sys.argv[1])
filter['low cutoff'] = float(sys.argv[2])
filter['high cutoff'] = float(sys.argv[3])
filter['tap count'] = int(sys.argv[4])

filter = InitBPF(filter)

plt.figure()
plt.plot(filter['Taps'])
plt.title(f'BPF {filter["low cutoff"]} - {filter["high cutoff"]}')
plt.grid()
plt.show()


#generate a new director for the reports
run_number = 0
print('trying to make a new directory')
while True:
	run_number = run_number + 1
	dirname = f'./run{run_number}/'
	try:
		os.mkdir(dirname)
	except:
		print(dirname + ' exists')
		continue
	print(f'made new directory {dirname}')
	break

# Generate and save report file
report_file_name = f'run{run_number}_report.txt'
try:
	report_file = open(dirname + report_file_name, 'w+')
except:
	print('Unable to create report file.')
with report_file:
	report_file.write('# Command line: ')
	for argument in sys.argv:
		report_file.write(f'{argument} ')

	report_file.write('\n\n# Bandpass Filter\n')
	report_file.write('\n')
	report_file.write(GenInt16ArrayC(f'BandpassFilter', filter['Taps'] * 32768, 10))
	report_file.write('\n')
	report_file.close()
	print(f'wrote {dirname + report_file_name}')
