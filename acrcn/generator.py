from PIL import Image
import numpy as np

print("Loading keyed vectors")
with open("/media/hdd/hdd/prannayk/temp.vec") as fil:
	lines = fil.readlines()
dictionary = dict()
for line in lines:
	t = line.split()
 	dictionary.update({t[0] : np.array(map(lambda x: float(x), t[1:])) })
print("Loaded and created word dictionary")

def video_loader():
	path = "/media/hdd/hdd/prannayk/action_reaction/"
	files = [f for f in os.listdir(path) if os.isfile(os.join(path, f))]
	lf = len(files)


def rot_generator(batch_size, frames):
	batch1in, batch1_labels = video_next_batch(batch_size)
	batch1 = batch1in.reshape([batch_size, 28,28])
	batch2 = batch1in.reshape([batch_size, 28,28])
	batch = np.zeros([batch_size, 64, 64,9])
	batch_gen = np.zeros([batch_size, 64, 64,3*frames])
	batch_labels = np.zeros([batch_size, 13])
	batch_labels[:,:10] += batch1_labels
	text_labels = np.zeros([batch_size, 5])
	for i in range(batch_size):
		t = np.random.randint(0,32 // (frames+2) + 1)
		l = np.random.randint(0,256,[3]).astype(float) / 255
		batch_labels[i,10:] = l
		random = np.random.randint(0,4)
		rot = np.random.normal(0,5)
		if t == 0:
			text_labels[i] = np.array([rot,-1,1,1,-1])
			text_labels[i][-1] *= random
			text_labels[i][-2] *= random
			for r in range(3):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate(r*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch[i,2+(random*r):30+(random*r),2+(random*r):30+(random*r),j+(3*r)] = batch2[i]*l[j]
			for r in range(frames):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate((j+3)*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch_gen[i, 10+(random*r):38+(random*r),10+(random*r):38+(random*r),j+(3*r)] = batch2[i]*l[j]
		elif t==1 :
			text_labels[i] = np.array([rot, 1,-1,-1,1])
			text_labels[i][-1] *= random
			text_labels[i][-2] *= random
			for r in range(3):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate(r*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch[i,34-(random*r):62-(random*r),34-(random*r):62-(random*r),j+(3*r)] = batch2[i]*l[j]
			for r in range(frames):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate((j+3)*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch_gen[i, 26-(random*r):54-(random*r),26-(random*r):54-(random*r),j+(3*r)] = batch2[i]*l[j]
		elif t==2 :
			text_labels[i] = np.array([rot, -1,-1,1,1])
			text_labels[i][-1] *= random
			text_labels[i][-2] *= random
			for r in range(3):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate(r*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch[i,34-(random*r):62-(random*r),2+(random*r):30+(random*r),j+(3*r)] = batch2[i]*l[j]
			for r in range(frames):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate((j+3)*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch_gen[i, 26-(random*r):54-(random*r),10+(random*r):38+(random*r),j+(3*r)] = batch2[i]*l[j]
		else :
			text_labels[i] = np.array([rot, 1,1,-1,-1])
			text_labels[i][-1] *= random
			text_labels[i][-2] *= random
			for r in range(3):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate(r*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch[i,2+(random*r):30+(random*r),34-(random*r):62-(random*r),j+(3*r)] = batch2[i]*l[j]
			for r in range(frames):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate((j+3)*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch_gen[i, 10+(random*r):38+(random*r),26-(random*r):54-(random*r),j+(3*r)] = batch2[i]*l[j]
	return batch, batch_gen, batch_labels, # text_labels

word_len = 14

def sentence_proc(one_hot, rot):
	num_dict = {
		0 : "zero",
		1 : "one",
		2 : "two",
		3 : "three",
		4 : "four",
		5 : "five",
		6 : "six",
		7 : "seven",
		8 : "eight",
		9 : "nine"
	}
	for i in range(len(one_hot)):
		if one_hot[i] == 1:
			string1 = num_dict[i]
	if rot > 0 : 
		string2 = "clockwise"
	else :
		string2 = "anti clockwise"
	return string1, string2

def convert_embedding(sentence):
	global dictionary
	embed = np.array(map(lambda x: dictionary[x], sentence.split()))
	t = np.zeros([word_len,300])
	t[:len(embed)] = embed
	del embed
	return t


def rot_text_generator(batch_size, frames):
	global word_len
	batch1in, batch1_labels = mnist.train.next_batch(batch_size)
	batch1 = batch1in.reshape([batch_size, 28,28])
	batch2 = batch1in.reshape([batch_size, 28,28])
	batch = np.zeros([batch_size, 64, 64,9])
	batch_gen = np.zeros([batch_size, 64, 64,3*frames])
	batch_labels = np.zeros([batch_size, 13])
	batch_labels[:,:10] += batch1_labels
	text_labels = np.zeros([batch_size, word_len, 300])
	for i in range(batch_size):
		t = np.random.randint(0,32 // (frames+2) + 1)
		l = np.random.randint(0,256,[3]).astype(float) / 255
		batch_labels[i,10:] = l
		random = np.random.randint(0,4)
		rot = np.random.normal(0,5)
		if t == 0:
			sentence = "the digit %s is moving to the left downwards while it rotates %s"%(sentence_proc(batch1_labels[i], rot))
			text_labels[i] = convert_embedding(sentence)
			# text_labels[i] = np.array([rot,-1,1,1,-1])
			# text_labels[i][-1] *= random
			# text_labels[i][-2] *= random
			for r in range(3):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate(r*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch[i,2+(random*r):30+(random*r),2+(random*r):30+(random*r),j+(3*r)] = batch2[i]*l[j]
			for r in range(frames):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate((j+3)*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch_gen[i, 10+(random*r):38+(random*r),10+(random*r):38+(random*r),j+(3*r)] = batch2[i]*l[j]
		elif t==1 :
			sentence = "the digit %s is moving to the right downwards while it rotates %s"%(sentence_proc(batch1_labels[i], rot))
			text_labels[i] = convert_embedding(sentence)
			# text_labels[i] = np.array([rot, 1,-1,-1,1])
			# text_labels[i][-1] *= random
			# text_labels[i][-2] *= random
			for r in range(3):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate(r*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch[i,34-(random*r):62-(random*r),34-(random*r):62-(random*r),j+(3*r)] = batch2[i]*l[j]
			for r in range(frames):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate((j+3)*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch_gen[i, 26-(random*r):54-(random*r),26-(random*r):54-(random*r),j+(3*r)] = batch2[i]*l[j]
		elif t==2 :
			sentence = "the digit %s is moving to the right upwards while it rotates %s"%(sentence_proc(batch1_labels[i], rot))
			text_labels[i] = convert_embedding(sentence)
			# text_labels[i] = np.array([rot, -1,-1,1,1])
			# text_labels[i][-1] *= random
			# text_labels[i][-2] *= random
			for r in range(3):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate(r*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch[i,34-(random*r):62-(random*r),2+(random*r):30+(random*r),j+(3*r)] = batch2[i]*l[j]
			for r in range(frames):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate((j+3)*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch_gen[i, 26-(random*r):54-(random*r),10+(random*r):38+(random*r),j+(3*r)] = batch2[i]*l[j]
		else :
			sentence = "the digit %s is moving to the right upwards while it rotates %s"%(sentence_proc(batch1_labels[i], rot))
			text_labels[i] = convert_embedding(sentence)
			# text_labels[i] = np.array([rot, 1,1,-1,-1])
			# text_labels[i][-1] *= random
			# text_labels[i][-2] *= random
			for r in range(3):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate(r*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch[i,2+(random*r):30+(random*r),34-(random*r):62-(random*r),j+(3*r)] = batch2[i]*l[j]
			for r in range(frames):
				batch2[i] = (np.array(Image.fromarray(batch1[i] * 255.).rotate((j+3)*rot, Image.BILINEAR).getdata()) / 255.).reshape(28,28)
				for j in range(3):
					batch_gen[i, 10+(random*r):38+(random*r),26-(random*r):54-(random*r),j+(3*r)] = batch2[i]*l[j]
	return batch, batch_gen, batch_labels, text_labels
def text_generator(batch_size):
	batch1, batch1_labels = mnist.train.next_batch(batch_size)
	batch1 = batch1.reshape([batch_size, 28,28])
	batch = np.zeros([batch_size, 64, 64,6])
	batch_gen = np.zeros([batch_size, 64, 64,3*frames])
	batch_labels = np.zeros([batch_size, 13])
	batch_labels[:,:10] += batch1_labels
	# text_labels = np.zeros([batch_size, 15])
	for i in range(batch_size):
		t = np.random.randint(0,32 // (frames+2) + 1)
		l = np.random.randint(0,256,[3]).astype(float) / 255
		batch_labels[i,10:] = l
		random = np.random.randint(0,5)
		if t == 0:
			# text_labels[i] = np.array([-1,1,1,-1])
			# text_labels[i][-1] *= random
			# text_labels[i][-2] *= random
			for r in range(2):
				for j in range(3):
					batch[i,2+(random*r):30+(random*r),2+(random*r):30+(random*r),j+(3*r)] = batch1[i]*l[j]
			for r in range(frames):
				for j in range(3):
					batch_gen[i, 10+(random*r):38+(random*r),10+(random*r):38+(random*r),j+(3*r)] = batch1[i]*l[j]
		elif t==1 :
			# text_labels[i] = np.array([1,-1,-1,1])
			# text_labels[i][-1] *= random
			# text_labels[i][-2] *= random
			for r in range(2):
				for j in range(3):
					batch[i,34-(random*r):62-(random*r),34-(random*r):62-(random*r),j+(3*r)] = batch1[i]*l[j]
			for r in range(frames):
				for j in range(3):
					batch_gen[i, 26-(random*r):54-(random*r),26-(random*r):54-(random*r),j+(3*r)] = batch1[i]*l[j]
		elif t==2 :
			# text_labels[i] = np.array([-1,-1,1,1])
			# text_labels[i][-1] *= random
			# text_labels[i][-2] *= random
			for r in range(2):
				for j in range(3):
					batch[i,34-(random*r):62-(random*r),2+(random*r):30+(random*r),j+(3*r)] = batch1[i]*l[j]
			for r in range(frames):
				for j in range(3):
					batch_gen[i, 26-(random*r):54-(random*r),10+(random*r):38+(random*r),j+(3*r)] = batch1[i]*l[j]
		else :
			# text_labels[i] = np.array([1,1,-1,-1])
			# text_labels[i][-1] *= random
			# text_labels[i][-2] *= random
			for r in range(2):
				for j in range(3):
					batch[i,2+(random*r):30+(random*r),34-(random*r):62-(random*r),j+(3*r)] = batch1[i]*l[j]
			for r in range(frames):
				for j in range(3):
					batch_gen[i, 10+(random*r):38+(random*r),26-(random*r):54-(random*r),j+(3*r)] = batch1[i]*l[j]
	return batch, batch_gen, batch_labels, # text_labels
