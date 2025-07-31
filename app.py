from flask import Flask, render_template, request
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'

# S3 details
S3_BUCKET = 'my-image-upload-bucket'
s3 = boto3.client('s3', region_name='us-east-1')  # specify your region

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    baby_name = request.form.get('baby_name')
    baby_age = request.form.get('baby_age')
    baby_country = request.form.get('baby_country')

    file = request.files.get('file')
    if not file or file.filename == '':
        return 'No file selected'

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Optional: make filename unique by prepending baby name or timestamp
    s3_key = f"{baby_name}_{filename}"
    s3.upload_file(filepath, S3_BUCKET, s3_key)

    # You can print form details for now (will save to RDS later)
    print(f"Received: {baby_name}, {baby_age}, {baby_country}, image: {s3_key}")

    return f'Baby {baby_name}\'s image uploaded successfully to S3 bucket: {S3_BUCKET}/{s3_key}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
