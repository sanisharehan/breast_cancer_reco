'''
This file keeps the code for using the newly uploaded file from the GUI, test and send the result to the gui backend.
'''
import os
import sys
from PIL import Image


OUTPUT_FILE = "/home/msprj_bcr/Breast_cancer_recognition_using_CNN/breast_cancer_reco/website/output.txt"

def splitFilenameExtension(filepath):
	"""
	"""
	file_split = filepath.split('.')
	filename = file_split[len(file_split)-2]
	extension = file_split[len(file_split)-1]
	return filename, extension



def predictBCRClassification(filepath):
	"""
	"""
	# Resize the image to 256 x 256
	filename, ext = splitFilenameExtension(filepath)
	print ("Filepath: %s, extension: %s" % (filename, ext))
	img = Image.open(filepath)
	img = img.resize((256, 256), Image.ANTIALIAS)
	filepath = filename + '_resize.' + ext
	img.save(filepath, quality=100)
	benignProb = 0
	malignProb = 0
	sys.stdout.flush()
	os.system('~/caffe/build/examples/cpp_classification/classification.bin ~/caffe/models/bvlc_alexnet/BreaKHis_cnn4_deploy.prototxt ~/caffe/models/bvlc_alexnet/BreaKHis_cnn4_400x_only_oct12_iter_10000.caffemodel ~/Breast_cancer_recognition_using_CNN/train_400//imagenet_bcr_train_mean.binaryproto ~/Breast_cancer_recognition_using_CNN/synset_bcr.txt ' + filepath + ' > ' + OUTPUT_FILE)
	filePtr = open(OUTPUT_FILE, 'r')
	for line in filePtr:
		print line
		if "benign" in line:
			benignProb = float(line.split(' - ')[0])
		elif "malign" in line:
			malignProb = float(line.split(' - ')[0])
		else:
			pass

	print ("Probabilities: Benign: %.3f Malign: %.5f" % (benignProb, malignProb))
	return (benignProb, malignProb)	
	

if __name__ == "__main__":
	filepath = sys.argv[1]
	(bProb, mProb) = predictBCRClassification(filepath)
				
