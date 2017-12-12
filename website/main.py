import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
from bcrCnnValidation import predictBCRClassification

UPLOAD_FOLDER = '/home/msprj_bcr/Breast_cancer_recognition_using_CNN/breast_cancer_reco/website/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	"""
	"""
	return '.' in filename and \
		filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

'''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	"""
	"""
	print ("Checking the uploaded file")
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
'''

def classifyBrImage(filepath):
	belignProb, malignProb = predictBCRClassification(filepath)
	return belignProb, malignProb

@app.route("/results", methods=["GET"])
def result_charts():
    try:
	filepath=""
	mProb=1
	bProb=1
	return render_template("result.html", path=filepath, mal=mProb, ben=bProb)
    except Exception as e:
	print("Exception: %s" %(e))

@app.route("/", methods=["GET", "POST"])
def hello():
    filepath=None
    mProb, bProb = None, None
    if request.method == "POST":
	print ("Request File object: %s" % str(request.files))
	app.logger.info("Request details: %s" % str(request.files))
	
	# Check if the post request contains the file.
	if 'file' not in request.files:
		print ("No file part")
		return redirect(request.url)
	
	file = request.files['file']
	print ("File object: %s" % str(file))

	# Check if user selected a file or not.
	if (file.filename == ""):
		print("No file selected")
		return redirect(request.url)

	# If everything is fine.
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		print os.path.join(app.config['UPLOAD_FOLDER'],filename)
		try:
			file_loc = os.path.join(app.config['UPLOAD_FOLDER'],filename)
			file.save(file_loc)
			print ("File uploaded at %s" %(file_loc))
			filepath = "static/uploads/" + filename
			bProb, mProb = classifyBrImage(file_loc)
		except Exception as e:
			print ("Error in server: %s" %e)
    try:
    	return render_template("index.html", path=filepath, mal=mProb, ben=bProb)
    except Exception as e:
	print e

if __name__ == "__main__":
    app.run(host='0.0.0.0')
