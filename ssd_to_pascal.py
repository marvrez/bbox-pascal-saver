import os
from os import listdir
from os.path import isfile, join
from detector import Detector
from pascal_writer import PascalWriter
from PIL import Image, ImageDraw
import numpy

visualize_detections = True

def draw_detection(xmin, ymin, xmax, ymax, name, conf):
    color = {"red" : (255,50,50), "green" : (0,255,0), "tower" : (245,245,245)} 
    draw.rectangle([xmin, ymin, xmax, ymax], outline=color[name])
    draw.text([xmin, ymin], name + ": " + str(conf), (0, 0, 255))

# Configurations for neural network
gpu_id = 0
image_resize  = 300
data_folder   = "data/"
model_def     = data_folder + "deploy.prototxt"
model_weights = data_folder + "old.caffemodel"
labelmap_file = data_folder + "labelmap.prototxt"

# Configurations for input images
image_dir = "../data/ascend/new_training_data/"
xml_dir = "../data/ascend/new_training_data_xml/"
image_files = [f for f in listdir(image_dir) if isfile(join(image_dir, f))]

detector = Detector(gpu_id, model_def, model_weights, image_resize, labelmap_file)

for image_file in image_files:
    filename = os.path.splitext(os.path.basename(image_file))[0]
    result = detector.detect(image_dir + image_file)
    print image_file,":", result

    img = Image.open(image_dir + image_file)
    if visualize_detections:
        draw = ImageDraw.Draw(img)

    writer = PascalWriter(image_dir, os.path.basename(image_file), numpy.array(img).shape)
    for item in result:
        xmin, ymin, xmax, ymax = item[0], item[1], item[2], item[3]
        name, conf = item[-1], item[-2]
        if visualize_detections:
            draw_detection(xmin, ymin, xmax, ymax, name, conf)
        writer.add_bbox(xmin, ymin, xmax , ymax, name)
    writer.save(xml_dir + filename + ".xml")

    if visualize_detections:
        img.save("output/" + filename + "_t.jpg")
