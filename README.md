# SSD-pascal-saver
Script that saves the outputs from the SSD-network in PASCAL-VOC format which can later be used for retraining the network. The script requires the model definition and weights file of an SSD-network and will use those to do object detections, and then save these detections in PASCAL-VOC format.

## Dependencies
  * [Python3](https://www.python.org/download/releases/3.0/)
  * [lxml](http://lxml.de/)
  * [Caffe](http://caffe.berkeleyvision.org/)
