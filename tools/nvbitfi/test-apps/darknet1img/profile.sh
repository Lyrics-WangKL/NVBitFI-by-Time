#!/bin/bash

FIDATA=$PWD/../test-apps-dependencies/darknet_data
nsys profile --trace=cuda --export sqlite --output=darknet1img darknet detector test $FIDATA/kitti.data $FIDATA/yolov3-kitti.cfg $FIDATA/yolov3-kitti_last.weights $FIDATA/street.png -ext_output -dont_show