#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename




import importlib.util
  
# specify the module that needs to be 
# imported relative to the path of the 
# module
spec=importlib.util.spec_from_file_location("gfpgan","inference_gfpgan.py")
  
# creates a new module based on spec
foo = importlib.util.module_from_spec(spec)
  
# executes the module in its own namespace
# when a module is imported or reloaded.
spec.loader.exec_module(foo)










app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "check"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        # flash('Image successfully uploaded and displayed below')
        foo.main(test_path = os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/restore/<filename>')
def display_image(filename):
    flash('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/restore/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()
