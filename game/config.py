# Set of functions for items.xml, bioms.xml, network.xml files parsing
from lxml import etree

def load_items(file):
    items = {'colors' : {}}

    data = etree.parse(file)
    root = data.getroot()

    for child in root.iterchildren('list'):
        type = child.get("type")

        if type in ['objects', 'monsters']:
            obj = items[type] = {}
            for item in child.iterchildren():
                id = int(item.get('id'))
                obj[item.text] = id
                items['colors'][id] = item.get('color')
        elif type == 'walkable_objects':
            obj = items[type] = []
            for item in child.iterchildren():
                obj.append(items['objects'][item.text])

    items['default'] = items['objects'][root.find('default').text]
    return items

def load_bioms(file, items):
    bioms = {}

    data = etree.parse(file)
    root = data.getroot().find('bioms')

    for item in root.findall('item'):
        item_id = int(item.get('id'))
        b = bioms[item_id] = {}
        bioms[item.get('name')] = item_id
        b['default'] = items['objects'][item.find('default').text]

        for item_list in item.findall('list'):
            type = item_list.get('type')
            item_array = []
            if type == 'objects':
                val = 0.0
                for objects_item in item_list.iterchildren('item'):
                    next_val = float(objects_item.get('value'))
                    item_array.append(((val, next_val), items[type][objects_item.text]))
                    val = next_val
            elif type == 'monsters':
                for monsters_item in item_list.iterchildren('item'):
                    item_array.append((float(monsters_item.get('prob')), items[type][monsters_item.text]))
            b[type] = item_array if item_array else None

    root = data.getroot().find('humidity').find('list')
    bioms_values = []
    val = 0.0
    for item in root.iterchildren('item'):
        next_val = float(item.get('value'))
        bioms_values.append(((val, next_val), bioms[item.text]))
        val = next_val
    bioms['humidity'] = bioms_values
    return bioms

def load_network(file):
    network = {}

    data = etree.parse(file)
    root = data.getroot()   

    # parse adddr
    addr = root.find('addr')
    network['addr'] = (addr.text, int(addr.get('port')))

    for list in root.findall('list'):
        type = list.get('type')
        n = network[type] = {}
        if type == 'protocol':
            for item in list.iterchildren():
                type = item.get('type')
                n[type] = {}
                for field in item.iterchildren():
                    n[type][field.text] = int(field.get('bytes'))
        elif type == 'requests':
            for item in list.iterchildren():
                n[int(item.get('id'))] = item.text
    return network

if __name__ == '__main__':
    path = './configs'

    items = load_items(path+'/items.xml')
    bioms = load_bioms(path+'/bioms.xml', items)
    network = load_network(path+'/network.xml')

    for type in ['objects', 'monsters']:
        for item in items[type]:
            print '%s: (%s), id: (%d)' % (type, item, items[type][item])

    print items['colors']

    print 'walkable_objects:', items['walkable_objects']

    print 'default:', items['default'] 

    print 'humidity:', bioms['humidity']
    print 'bioms:', bioms
    print 'network:', network