import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "/Users/shubhambhardwaj/Downloads/osm files/chicago_illinois.osm"  # Replace this with your osm file
SAMPLE_FILE = "/Users/shubhambhardwaj/Downloads/osm files/chicago_illinois_sample.osm"

k = 1000 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    events,root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')
    c=0
    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        print c
        if (c< 500000000000):
            if c % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))
        else:
            break
        c = c + 100000

    output.write('</osm>')