from flask import Flask, render_template, request, redirect
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'

# Set your S3 details
S3_BUCKET = 'mihtpeed'
s3 = boto3.client('s3')

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        s3.upload_file(filepath, S3_BUCKET, filename)
        return f'Image uploaded successfully to S3 bucket: {S3_BUCKET}/{filename}'

    return 'File upload failed'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
