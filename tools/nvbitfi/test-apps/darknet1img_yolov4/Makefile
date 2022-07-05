test:
	./darknet1img_yolov4.sh
golden:
	./darknet1img_yolov4.sh >golden_stdout.txt 2>golden_stderr.txt
clobber:
	rm -f golden* *_regcount.p stdout* stderr*

.PHONY: clean

clean:
	rm -rf $(OBJS) $(EXEC) $(LIBNAMESO) $(APPNAMESO)
