from flask import Flask, render_template, request
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'  # Temporary storage before S3 upload

S3_BUCKET = 'mihtpeed'

# Initialize boto3 client (ensure IAM role is attached with proper S3 permissions)
s3 = boto3.client('s3')

@app.route('/', methods=['GET', 'POST'])
def baby_form():
    if request.method == 'POST':
        baby_name = request.form.get('baby_name')
        baby_age = request.form.get('baby_age')
        parent_name = request.form.get('parent_name')
        contact = request.form.get('contact')
        baby_image = request.files.get('baby_image')

        if not (baby_name and baby_age and parent_name and contact and baby_image):
            return "Missing required fields", 400

        # Save file temporarily
        filename = secure_filename(baby_image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        baby_image.save(filepath)

        try:
            # Upload to S3 (public-read so we can show the image back)
            s3.upload_file(filepath, S3_BUCKET, filename, ExtraArgs={'ACL': 'public-read'})

            image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

            return render_template(
                'form.html',
                submitted=True,
                baby_name=baby_name,
                baby_age=baby_age,
                parent_name=parent_name,
                contact=contact,
                image_url=image_url
            )
        except Exception as e:
            return f"Upload failed: {str(e)}", 500

    return render_template('form.html', submitted=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
