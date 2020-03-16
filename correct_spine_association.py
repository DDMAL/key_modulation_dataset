import sys
import re
import pdb

def add_staff_association(lines):
	ignore_lines = ['**', '*-', '*', '==', '=', '!']
	for line in lines:
		line = line.strip()
		staff_regexp = re.compile((
			r'^\*staff([0-9]+).*'
			r'\*staff([0-9]+).*'
			r'\*staff([0-9]+).*'
			r'\*staff([0-9]+).*$'))
		m = staff_regexp.match(line)
		if m:
			print(line)
			staff_indexes = [int(s) for s in m.groups()]
			current_staff = staff_indexes[0]
			# print(staff_indexes)
			continue
		for ignores in ignore_lines:
			if line.startswith(ignores):
				print(line)
				break
		else:
			# pdb.set_trace()
			spines = line.split('\t')[:-1] # Ignore the last column (annotation)
			dur = re.compile(r'^([0-9]+).*$')
			durations = [dur.match(s) for s in spines]
			durations = [int(x.groups(0)[0]) if x else 0 for x in durations]
			shortest_duration = max(durations)
			current_staff_duration = durations[staff_indexes.index(current_staff)]
			if shortest_duration != current_staff_duration:
				shortest_duration_index = durations.index(shortest_duration)
				shortest_duration_staff = staff_indexes[shortest_duration_index]
				print('*\t*\t*\t*\t*staff{}'.format(shortest_duration_staff))
				current_staff = shortest_duration_staff
			print(line)
			# print(shortest_duration_staff)

if __name__ == '__main__':
	f = sys.argv[1]
	with open(f) as fd:
		lines = fd.readlines()
	add_staff_association(lines)
