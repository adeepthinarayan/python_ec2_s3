from flask import Flask, render_template, request, redirect, url_for
import boto3
import os
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'

# ---------- AWS S3 CONFIG ----------
S3_BUCKET = 'ihtpeed'
S3_REGION = 'ap-south-1'
s3 = boto3.client('s3', region_name=S3_REGION)

# ---------- MYSQL RDS CONFIG ----------
DB_CONFIG = {
    'host': 'deepthi.cbmwd77sfjx4.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'deepthi123!',
    'database': 'babycontest'
}

@app.route('/', methods=['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        baby_name = request.form['baby_name']
        baby_age = request.form['baby_age']
        parent_name = request.form['parent_name']
        contact = request.form['contact']
        file = request.files['baby_image']

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(local_path)

            # Upload to S3
            s3.upload_file(local_path, S3_BUCKET, filename)
            image_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"

            # Save to DB
            try:
                connection = mysql.connector.connect(**DB_CONFIG)
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO entries (baby_name, baby_age, parent_name, contact, s3_image_url)
                    VALUES (%s, %s, %s, %s, %s)
                """, (baby_name, baby_age, parent_name, contact, image_url))
                connection.commit()
                cursor.close()
                connection.close()
            except Error as e:
                return f"Database error: {str(e)}"

            return redirect(url_for('submission_success', baby_name=baby_name, baby_age=baby_age,
                                    parent_name=parent_name, contact=contact, image_url=image_url))
    return render_template('form.html')


@app.route('/success')
def submission_success():
    return render_template('success.html',
                           baby_name=request.args.get('baby_name'),
                           baby_age=request.args.get('baby_age'),
                           parent_name=request.args.get('parent_name'),
                           contact=request.args.get('contact'),
                           image_url=request.args.get('image_url'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
