import sys
import re
import pdb

def printrow(kern_spines, text_spines):
	full_row = kern_spines + text_spines
	print('\t'.join(full_row))

def add_staff_association(lines):
	for line in lines:
		is_staff_indexes = False
		line = line.strip()
		if line.startswith('!'):
			print(line)
			continue
		########################
		#### Get *staffX indexes
		########################
		staff_regexp = re.compile((
			#r'^\*staff([0-9]+).*'
			#r'\*staff([0-9]+).*'
			r'\*staff([0-9]+).*'
			r'\*staff([0-9]+).*$'))
		is_staff_indexes = staff_regexp.match(line)
		if is_staff_indexes:
			staff_indexes = [int(s) for s in is_staff_indexes.groups()]
			current_staff = staff_indexes[0]
		#####################
		#### Separate columns
		#####################
		spines = line.split('\t')
		kern_spines = spines[:-1]
		text_spines = [spines[-1] for _ in range(len(kern_spines))]
		# Write the right staff number in annotation columns
		if is_staff_indexes:
			text_spines = ['*staff{}'.format(i) for i in staff_indexes]
			printrow(kern_spines, text_spines)
			continue
		# Lines with * or = are written as they are
		elif line.startswith('*') or line.startswith('='):
			printrow(kern_spines, text_spines)
			continue
		#####################################################
		#### Now we decide where to put a specific annotation
		#####################################################
		dur = re.compile(r'^([0-9]+).*$')
		durations = [dur.match(s) for s in spines]
		durations = [int(x.groups(0)[0]) if x else 0 for x in durations]
		shortest_duration = max(durations)
		current_staff_index = staff_indexes.index(current_staff)
		current_staff_duration = durations[current_staff_index]
		if shortest_duration != current_staff_duration:
			shortest_duration_index = durations.index(shortest_duration)
			shortest_duration_staff = staff_indexes[shortest_duration_index]
			current_staff = shortest_duration_staff
			current_staff_index = staff_indexes.index(current_staff)
		text_spines = [t if idx == current_staff_index else '.' for idx, t in enumerate(text_spines)]
		printrow(kern_spines, text_spines)

if __name__ == '__main__':
	f = sys.argv[1]
	with open(f) as fd:
		lines = fd.readlines()
	add_staff_association(lines)
