Use this in User Data:
=============
#!/bin/bash

# Update and install dependencies
apt update -y
apt install -y git python3-pip python3-venv

# Clone the repo
cd /opt
git clone https://github.com/adeepthinarayan/python_ec2_s3.git
cd python_ec2_s3

# Set up a virtual environment (clean & isolated)
python3 -m venv venv
source venv/bin/activate

# Install Flask inside the virtual environment
pip install flask

# Run the app using virtual environment's python
nohup venv/bin/python app.py > output.log 2>&1 &
