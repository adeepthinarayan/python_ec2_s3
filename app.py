from flask import Flask, render_template, request
import boto3
import os
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'

# ---------- AWS S3 CONFIG ----------
S3_BUCKET = 'ihtpeed'  # Replace with your bucket name
S3_REGION = 'ap-south-1'  # Replace with your region
s3 = boto3.client('s3', region_name=S3_REGION)

# ---------- MYSQL RDS CONFIG ----------
DB_CONFIG = {
    'host': 'deepthi.cbmwd77sfjx4.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'deepthi123!',
    'database': 'baby_contest'
}

def insert_to_db(baby_name, baby_age, parent_name, contact, image_url):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS baby_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                baby_name VARCHAR(100),
                baby_age INT,
                parent_name VARCHAR(100),
                contact VARCHAR(100),
                image_url TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO baby_entries (baby_name, baby_age, parent_name, contact, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """, (baby_name, baby_age, parent_name, contact, image_url))
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print("Database error:", e)

@app.route('/', methods=['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        # Get form fields
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
            try:
                s3.upload_file(local_path, S3_BUCKET, filename)
                image_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
            except Exception as e:
                return f"Upload failed: {str(e)}"

            # Insert into DB
            insert_to_db(baby_name, baby_age, parent_name, contact, image_url)

            return render_template('form.html',
                                   submitted=True,
                                   baby_name=baby_name,
                                   baby_age=baby_age,
                                   parent_name=parent_name,
                                   contact=contact,
                                   image_url=image_url)

    return render_template('form.html', submitted=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
