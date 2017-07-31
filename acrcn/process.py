import os
import numpy as np
from os.path import join, isfile
import sys
from subprocess import call
from PIL import Image

folders = ["boxing", "handclapping", "handwaving", "jogging", "running", "walking"]
direc = "/media/hdd/hdd/prannayk/action_reaction/"

for folder in folders[:1] : 
	path = direc + folder
	filelist = [f for f in os.listdir(path) if isfile(join(path, f))]
	for file in filelist[:10]:
		filename = file.split("/")[-1].split(".")[0]
		call(["mkdir",join(path, filename)])
		os.system("ffmpeg -i %s/%s.avi -vf fps=5 -f image2 %s/%s/%s-"%(path, filename, path, filename, filename) + "%03d.png ")
		os.system("mv %s/%s-* %s/"%(path, filename, filename))
		print("Done with %s"%(filename))
		path_file = direc + folder + "/" + filename
		images =[f for f in os.listdir(path_file) if isfile(join(path_file, f))]
		images = images[:30]
		frames = np.zeros([30, 84, 64])
		for i,img in enumerate(images) : 
			im = (np.array(Image("%s/%s"%(path, filename)).getdata()) / 255. ).resize([84,64, 3])
			frames[i] = im
		np.save("%s/%s/video.npy"%(path, filename))
