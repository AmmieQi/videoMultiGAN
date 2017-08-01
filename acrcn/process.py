import os
import numpy as np
from os.path import join, isfile
import sys
from subprocess import call
from PIL import Image

folders = ["boxing", "handclapping", "handwaving", "jogging", "running", "walking"]
direc = "/media/hdd/hdd/prannayk/action_reaction/"

for folder in folders : 
	path = direc + folder
	filelist = [f for f in os.listdir(path) if isfile(join(path, f))]
	for file in filelist:
		filename = file.split("/")[-1].split(".")[0]
		call(["mkdir",join(path, filename)])
		os.system("ffmpeg -i %s/%s.avi -vf fps=5 -s 40x32 -f image2 %s/%s/%s-"%(path, filename, path, filename, filename) + "%03d.png ")
		os.system("mv %s/%s-* %s/"%(path, filename, filename))
		print("Done with %s"%(filename))
		path_file = direc + folder + "/" + filename
		images =[f for f in os.listdir(path_file) if isfile(join(path_file, f))]
		images = images[:30]
		frames = np.zeros([30, 32, 40, 3])
		for i,img in enumerate(images) : 
			im = np.array(Image.open("%s/%s/%s"%(path, filename, img)).getdata())
			print(im.shape)
			im = (im / 255. ).reshape([32,40, 3])
			print(im)
			frames[i] = im
		np.save("%s/video_%s.npy"%(direc, filename), frames)
		os.system("rm -rf %s/%s")
