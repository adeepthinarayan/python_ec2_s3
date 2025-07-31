from flask import Flask, render_template, request
import boto3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# S3 Configuration
S3_BUCKET = "your-bucket-name"  # ← Set your bucket name here
S3_REGION = "ap-south-1"  # Replace with your region
s3 = boto3.client("s3", region_name=S3_REGION)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        baby_name = request.form.get('baby_name')
        baby_age = request.form.get('baby_age')
        parent_name = request.form.get('parent_name')
        contact = request.form.get('contact')

        # Upload image to S3
        image = request.files.get('baby_image')
        image_url = None

        if image and image.filename:
            filename = secure_filename(image.filename)
            s3.upload_fileobj(
                image,
                S3_BUCKET,
                filename,
                ExtraArgs={'ACL': 'public-read'}  # Make it publicly accessible
            )
            image_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"

        return render_template(
            'form.html',
            submitted=True,
            baby_name=baby_name,
            baby_age=baby_age,
            parent_name=parent_name,
            contact=contact,
            image_url=image_url
        )

    return render_template('form.html', submitted=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
