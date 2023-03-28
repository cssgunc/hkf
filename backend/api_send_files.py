from flask import Flask, flash, request, redirect, send_from_directory
import os
from werkzeug.utils import secure_filename

# Currently using local directory
UPLOAD_FOLDER = 'C:\\some_directory'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

# Location that file will download to
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Checking if file is csv
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Includes a mock front-end that I used for testing
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.stream.seek(0)
            f = file.read().decode()
            
            # Testing mutating data in the file
            f = f.replace("A", "B")
    
            filename_to_save = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filename_to_save, "w", newline='') as file_to_save:
                file_to_save.write(f)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Downloads the csv file that was uploaded to specified folder
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000, threaded = True, debug = True)