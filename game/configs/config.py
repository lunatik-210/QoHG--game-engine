from lxml import etree

items = load_items('items.xml')
bioms = load_bioms('bioms.xml', items)
network = load_network('network.xml')

def load_items(file):
	items = {}

	data = etree.parse(file)
	root = data.getroot()

	for child in root.findall('list'):
		type = child.get("type")
		if type in ['objects', 'monsters']:
			o = items[type] = {}
			for it in child.iterchildren():
				o[it.text] = { 'id'    : int(it.get('id')), 
					  		   'color' : it.get('color')   }
		elif type == 'walkable_objects':
			o = items[type] = []
			for it in child.iterchildren():
				o.append(items['objects'][it.text]['id'])
	items['default'] = items['objects'][root.find('default').text]['id']
	return items

def load_bioms(file, items):
	bioms = {}

	data = etree.parse(file)
	root = data.getroot()

	for item in root.findall('item'):
		b = bioms[item.get('name')] = {'id' : int(item.get('id'))}
		b['default'] = items['objects'][item.find('default').text]['id']
		for list in item.findall('list'):
			type = list.get('type')
			item_array = []
			if type == 'objects':
				val = 0.0
				for item in list.iterchildren('item'):
					next_val = float(item.get('value'))
					item_array.append(((val, val+next_val), items[type][item.text]['id']))
					val += next_val
			elif type == 'monsters':
				for item in list.iterchildren('item'):
					item_array.append((float(item.get('prob')), items[type][item.text]['id']))
			b[type] = item_array if item_array else None
	return bioms

def load_network(file):
	network = {}

	data = etree.parse(file)
	root = data.getroot()	

	return network

if __name__ == '__main__':
	print bioms
	for type in ['objects', 'monsters']:
		for item in items[type]:
			print '%s: (%s), color: (%s), id: (%d)' % (type, item, 
					items[type][item]['color'], 
					items[type][item]['id'])

	print 'walkable_objects:', items['walkable_objects']

	print 'default:', items['default'] 

	for biom in bioms:
		print biom
		print '--', bioms[biom]['objects']
		print '--', bioms[biom]['monsters']
		print '--', bioms[biom]['default']