from time import sleep
from pathlib import Path

def compile(src, target):
	with open(src) as f:
		src = f.read()


	result = """{
	"name": "Simply Dark",
	"colors": {
		"editor.background": "#1c1c1c",
		"editor.foreground": "#d1d1d1",
		"activityBarBadge.background": "#202528",
		"sideBarTitle.foreground": "#bbbbbb"
	},
	"tokenColors": [\n"""

	indent = '\t'
	double_indent = '\t\t'
	triple_indent = '\t\t\t'

	c = []

	for line in src.split('\n'):
		if '//' in line:
			line = line.split('//')[0]
		if line.strip() == '':
			continue
		if line.startswith('\t'):
			c[-1].append(line[1:])
		else:
			c.append([line])

	for styles, *selectors in c:
		result += double_indent + '{\n' + triple_indent + '"scope": [' + ', '.join(['"' + i + '"' for i in selectors]) + '],\n' + triple_indent + '"settings": {'
		for style in styles.split(' '):
			if style in ('bold', 'italic', 'underline', 'strikethrough'):
				result += f'"fontStyle": "{style}", '
			else:
				result += f'"foreground": "{style}", '
		result = result[:-2] # Remove extra comma and space
		result += '},\n' + double_indent + '},\n'
	
	result += indent + ']\n' + '}\n'
	
	with open(target, 'w') as f:
		f.write(result)

previous_time_modified = None
try:
	while True:
		sleep(1)
		time_modified = Path('simply-dark-color-theme.gtheme').stat().st_mtime
		if  time_modified != previous_time_modified:
			previous_time_modified = time_modified
			print('Updating Simply Dark-color-theme.json')
			compile('simply-dark-color-theme.gtheme', 'Simply Dark-color-theme.json')
except KeyboardInterrupt:
	print('\nPython script stopped')
