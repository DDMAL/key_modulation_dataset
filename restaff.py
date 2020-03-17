import sys

def add_staff_association(lines):
    for line in lines:
        line = line.strip()
        if line.startswith('*staff'):
            print('*staff4\t*staff3\t*staff2\t*staff1\t*')
        else:
            print(line)

if __name__ == '__main__':
	f = sys.argv[1]
	with open(f) as fd:
		lines = fd.readlines()
	add_staff_association(lines)
