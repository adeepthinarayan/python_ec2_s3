import logging
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Set up logging
log_file = 'app.log'
logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

@app.route('/', methods=['GET', 'POST'])
def baby_form():
    if request.method == 'POST':
        baby_name = request.form['baby_name']
        baby_age = request.form['baby_age']
        parent_name = request.form['parent_name']
        contact = request.form['contact']

        logging.info(f"New submission: Baby='{baby_name}', Age='{baby_age}', Parent='{parent_name}', Contact='{contact}'")

        return render_template('form.html', submitted=True,
                               baby_name=baby_name,
                               baby_age=baby_age,
                               parent_name=parent_name,
                               contact=contact)

    return render_template('form.html', submitted=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
