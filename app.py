from flask import Flask, render_template, request
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'

# S3 Configuration
S3_BUCKET = 'ihtpeed'  # Replace with your actual bucket name
s3 = boto3.client('s3')  # Assumes IAM role/instance profile for credentials

@app.route('/')
def upload_form():
    return render_template('form.html', submitted=False)

@app.route('/', methods=['POST'])
def upload_image():
    if 'baby_image' not in request.files:
        return 'No file part'

    file = request.files['baby_image']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Upload to S3 (bucket must not require ACLs)
            s3.upload_file(filepath, S3_BUCKET, filename)
        except Exception as e:
            return f'Upload failed: Failed to upload {filepath} to {S3_BUCKET}/{filename}: {str(e)}'

        # Generate a pre-signed URL for image display
        try:
            image_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET, 'Key': filename},
                ExpiresIn=3600  # 1 hour
            )
        except Exception as e:
            image_url = None

        # Form fields
        baby_name = request.form.get('baby_name')
        baby_age = request.form.get('baby_age')
        parent_name = request.form.get('parent_name')
        contact = request.form.get('contact')

        return render_template('form.html',
                               submitted=True,
                               baby_name=baby_name,
                               baby_age=baby_age,
                               parent_name=parent_name,
                               contact=contact,
                               image_url=image_url)

    return 'File upload failed'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
