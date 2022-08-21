#!/bin/bash

FIDATA=$PWD/../test-apps-dependencies/darknet_data
nsys profile --trace=cuda --export sqlite --output=darknet1img_tiny darknet detector test $FIDATA/coco.data $FIDATA/yolov3-tiny.cfg $FIDATA/yolov3-tiny.weights $FIDATA/street.png -ext_output -dont_show