from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Directory to store uploaded images
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        baby_name = request.form.get('baby_name')
        baby_age = request.form.get('baby_age')
        parent_name = request.form.get('parent_name')
        contact = request.form.get('contact')

        # Handle image upload
        image = request.files.get('baby_image')
        image_url = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f"/static/uploads/{filename}"

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
