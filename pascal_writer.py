import sys
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs

XML_EXT = '.xml'
ENCODE_METHOD = 'utf-8'

class PascalWriter:
    def __init__(self, foldername, filename, img_size):
        self.foldername = foldername
        self.filename = filename
        self.img_size = img_size
        self.bboxes = []

    """
    Return a pretty-printed XML string for the Element.
    """
    def prettify(self, elem):
        rough_string = ElementTree.tostring(elem, ENCODE_METHOD)
        root = etree.fromstring(rough_string)
        return etree.tostring(root, pretty_print=True, encoding=ENCODE_METHOD).replace("  ".encode(), "\t".encode())
    
    """
        Creates and returns the newly created XML root
    """
    def create_xml(self):
        if self.filename is None or \
                self.foldername is None or \
                self.img_size is None:
            return None

        top = Element('annotation')

        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        size_part = SubElement(top, 'size')
        width  = SubElement(size_part, 'width')
        height = SubElement(size_part, 'height')
        depth  = SubElement(size_part, 'depth')
        height.text = str(self.img_size[0])
        width.text  = str(self.img_size[1])
        depth.text  = str(self.img_size[2]) if len(self.img_size) == 3 else '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def add_bbox(self, xmin, ymin, xmax, ymax, name):
        bbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bbox['name'] = name
        self.bboxes.append(bbox)

    def store_bboxes(self, top):
        for bbox in self.bboxes:
            object_item = SubElement(top, 'object')
            name = SubElement(object_item, 'name')
            name.text = bbox['name']
            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = SubElement(object_item, 'truncated')
            if int(bbox['ymax']) == int(self.img_size[0]) or (int(bbox['ymin'])== 1):
                truncated.text = "1" # max == height or min
            elif (int(bbox['xmax'])==int(self.img_size[1])) or (int(bbox['xmin'])== 1):
                truncated.text = "1" # max == width or min
            else:
                truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = str(0)
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(bbox['xmin'])
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(bbox['ymin'])
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(bbox['xmax'])
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(bbox['ymax'])

    def save(self, out_filename=None):
        root = self.create_xml()
        self.store_bboxes(root)
        out_filename = self.filename + XML_EXT if out_filename is None else out_filename
        out_file = codecs.open(out_filename, 'w', encoding=ENCODE_METHOD)

        result = self.prettify(root)
        out_file.write(result.decode('utf8'))
        out_file.close()
