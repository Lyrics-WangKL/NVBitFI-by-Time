#!/bin/bash

FIDATA=$PWD/../test-apps-dependencies/darknet_data
./darknet detector test $FIDATA/coco.data $FIDATA/yolov3-tiny.cfg $FIDATA/yolov3-tiny.weights $FIDATA/street.png -ext_output -dont_show