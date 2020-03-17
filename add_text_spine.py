import sys

def add_empty_text_spine(lines):
	for line in lines:
		if line.startswith('**'):
			line = line.replace('\n', '\t**text')
		elif line.startswith('*-'):
			line = line.replace('\n', '\t*-')
		elif line.startswith('*'):
			line = line.replace('\n', '\t*')
		elif line.startswith('=='):
			line = line.replace('\n', '\t==')
		elif line.startswith('='):
			line = line.replace('\n', '\t={}'.format(line[1]))
		elif line.startswith('!'):
			line = line.replace('\n', '')
		else:
			line = line.replace('\n', '\t.')
		print(line)

if __name__ == '__main__':
	f = sys.argv[1]
	with open(f) as fd:
		lines = fd.readlines()
	add_empty_text_spine(lines)
